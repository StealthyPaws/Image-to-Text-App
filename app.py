import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import re
import tempfile
import os

# Configure page
st.set_page_config(
    page_title="Image to Word Converter",
    page_icon="📄",
    layout="wide"
)

# Title and description
st.title("📄 Image to Word Converter")
st.markdown("""
Convert scanned documents or images to editable Word format while preserving basic formatting.
Supports JPG, PNG, and other common image formats.
""")

def preprocess_image(image):
    """
    Preprocess the image for better OCR results
    """
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Apply thresholding to get binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
    
    # Dilation and erosion to remove noise
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.dilate(denoised, kernel, iterations=1)
    processed = cv2.erode(processed, kernel, iterations=1)
    
    return processed

def detect_formatting(text, confidence):
    """
    Detect basic formatting from OCR results
    Returns formatting attributes for text
    """
    formatting = {
        'is_bold': False,
        'is_italic': False,
        'is_heading': False,
        'alignment': 'left'
    }
    
    # Simple heuristics for formatting detection
    # Check if text is all uppercase (likely heading)
    if text.isupper() and len(text.split()) <= 10:
        formatting['is_heading'] = True
        formatting['is_bold'] = True
    
    # Check if text starts with common heading patterns
    heading_patterns = [r'^Chapter \d+', r'^Section \d+', r'^\d+\.', r'^[A-Z][A-Z\s]+$']
    for pattern in heading_patterns:
        if re.match(pattern, text.strip()):
            formatting['is_heading'] = True
            formatting['is_bold'] = True
            break
    
    # Check for centered text (short lines, common in titles)
    if len(text.strip()) < 50 and len(text.strip().split()) <= 8:
        words = text.strip().split()
        if len(words) > 0 and words[0][0].isupper():
            formatting['alignment'] = 'center'
    
    return formatting

def extract_text_with_formatting(image):
    """
    Extract text from image using Tesseract with formatting information
    """
    # Preprocess image
    processed_img = preprocess_image(image)
    
    # Convert to PIL Image for pytesseract
    pil_img = Image.fromarray(processed_img)
    
    # Get detailed OCR data
    ocr_data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
    
    # Group text by lines
    lines = []
    current_line = {
        'text': '',
        'confidence': [],
        'block_num': -1,
        'line_num': -1
    }
    
    n_boxes = len(ocr_data['text'])
    for i in range(n_boxes):
        text = ocr_data['text'][i].strip()
        conf = int(ocr_data['conf'][i])
        block_num = ocr_data['block_num'][i]
        line_num = ocr_data['line_num'][i]
        
        if conf > 0 and text:  # Only consider confident detections
            # New line detected
            if current_line['line_num'] != line_num or current_line['block_num'] != block_num:
                if current_line['text']:
                    lines.append(current_line)
                current_line = {
                    'text': text,
                    'confidence': [conf],
                    'block_num': block_num,
                    'line_num': line_num
                }
            else:
                current_line['text'] += ' ' + text
                current_line['confidence'].append(conf)
    
    # Add last line
    if current_line['text']:
        lines.append(current_line)
    
    return lines

def create_word_document(lines_data):
    """
    Create a Word document with formatting preserved
    """
    doc = Document()
    
    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    prev_block = -1
    
    for line_data in lines_data:
        text = line_data['text'].strip()
        if not text:
            continue
        
        avg_confidence = sum(line_data['confidence']) / len(line_data['confidence']) if line_data['confidence'] else 0
        
        # Detect formatting
        formatting = detect_formatting(text, avg_confidence)
        
        # Add spacing between blocks
        if prev_block != -1 and line_data['block_num'] != prev_block:
            doc.add_paragraph()
        
        # Add paragraph
        paragraph = doc.add_paragraph()
        run = paragraph.add_run(text)
        
        # Apply formatting
        if formatting['is_bold']:
            run.bold = True
        
        if formatting['is_italic']:
            run.italic = True
        
        # Set font size
        if formatting['is_heading']:
            run.font.size = Pt(16)
        else:
            run.font.size = Pt(11)
        
        # Set alignment
        if formatting['alignment'] == 'center':
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif formatting['alignment'] == 'right':
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        prev_block = line_data['block_num']
    
    return doc

def main():
    # Sidebar for information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Features:**
        - Image preprocessing for better OCR
        - Text extraction with Tesseract OCR
        - Automatic formatting detection
        - Preserves bold, italic, headings
        - Detects text alignment
        - Generates formatted .docx files
        
        **Supported Formats:**
        - JPG, JPEG, PNG, BMP, TIFF
        
        **Tips:**
        - Use clear, high-resolution images
        - Ensure good lighting and contrast
        - Avoid skewed or rotated images
        """)
        
        st.header("🎯 Project Info")
        st.markdown("""
        **Task 1: Image-to-Word Converter (MVP)**
        
        A desktop application that extracts text from images 
        while preserving basic formatting.
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload a clear image of a document"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Show image info
            st.info(f"📏 Image Size: {image.size[0]} x {image.size[1]} pixels")
    
    with col2:
        st.header("⚙️ Processing")
        
        if uploaded_file is not None:
            process_button = st.button("🚀 Convert to Word", type="primary", use_container_width=True)
            
            if process_button:
                with st.spinner("Processing image... This may take a moment."):
                    try:
                        # Load image
                        image = Image.open(uploaded_file)
                        
                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Step 1: Preprocess
                        status_text.text("Step 1/3: Preprocessing image...")
                        progress_bar.progress(33)
                        
                        # Step 2: Extract text
                        status_text.text("Step 2/3: Extracting text with OCR...")
                        lines_data = extract_text_with_formatting(image)
                        progress_bar.progress(66)
                        
                        # Step 3: Create document
                        status_text.text("Step 3/3: Creating Word document...")
                        doc = create_word_document(lines_data)
                        progress_bar.progress(100)
                        
                        # Save to bytes
                        doc_bytes = io.BytesIO()
                        doc.save(doc_bytes)
                        doc_bytes.seek(0)
                        
                        status_text.text("✅ Conversion complete!")
                        
                        # Success message
                        st.success("🎉 Document created successfully!")
                        
                        # Display extracted text preview
                        with st.expander("📝 Preview Extracted Text"):
                            preview_text = "\n\n".join([line['text'] for line in lines_data[:10]])
                            st.text_area("First 10 lines:", preview_text, height=200)
                            if len(lines_data) > 10:
                                st.info(f"... and {len(lines_data) - 10} more lines")
                        
                        # Statistics
                        total_words = sum([len(line['text'].split()) for line in lines_data])
                        avg_confidence = sum([sum(line['confidence'])/len(line['confidence']) for line in lines_data if line['confidence']]) / len(lines_data) if lines_data else 0
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Lines", len(lines_data))
                        col_b.metric("Words", total_words)
                        col_c.metric("Confidence", f"{avg_confidence:.1f}%")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Word Document",
                            data=doc_bytes,
                            file_name="converted_document.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error during conversion: {str(e)}")
                        st.info("💡 Try uploading a clearer image or check if Tesseract OCR is properly installed.")
        else:
            st.info("👈 Please upload an image to begin conversion")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit, OpenCV, and Tesseract OCR</p>
        <p><small>Image-to-Word Converter MVP v1.0</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
