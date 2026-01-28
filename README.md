# 📄 Image to Word Converter - MVP

A Streamlit-based web application that converts scanned documents or images to editable Word format while preserving basic formatting like bold, italic, alignment, and paragraph structure.

## 🚀 Features

- **Image Preprocessing**: Automatic image enhancement for better OCR results
- **OCR Integration**: Uses Tesseract OCR for accurate text extraction
- **Formatting Detection**: Automatically detects and preserves:
  - Bold text (headings, titles)
  - Italic text
  - Text alignment (left, center, right)
  - Paragraph structure
- **Word Document Generation**: Creates properly formatted .docx files
- **User-Friendly Interface**: Clean, intuitive Streamlit interface
- **Support for Multiple Formats**: JPG, PNG, BMP, TIFF

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Tesseract OCR engine

### Python Dependencies
All dependencies are listed in `requirements.txt`:
- streamlit
- opencv-python-headless
- numpy
- Pillow
- pytesseract
- python-docx

## 🔧 Installation

### Local Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd image-to-word-converter
```

2. **Install Tesseract OCR**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng libtesseract-dev
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## ☁️ Deployment on Streamlit Cloud

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at [streamlit.io](https://streamlit.io))

### Deployment Steps

1. **Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Important Files for Deployment**
   - `app.py` - Main application
   - `requirements.txt` - Python dependencies
   - `packages.txt` - System packages (Tesseract)
   - `.streamlit/config.toml` - Streamlit configuration

### Configuration Notes
- The `packages.txt` file ensures Tesseract OCR is installed on Streamlit Cloud
- Maximum upload size is set to 10MB in config
- Free tier on Streamlit Cloud is sufficient for this application

## 📖 Usage Guide

1. **Upload Image**
   - Click "Choose an image file" button
   - Select a clear image of a document (JPG, PNG, etc.)
   - The image will be displayed for preview

2. **Convert to Word**
   - Click "🚀 Convert to Word" button
   - Wait for processing (may take 10-30 seconds depending on image size)
   - View the conversion progress and statistics

3. **Download Document**
   - Preview extracted text in the expandable section
   - Review conversion statistics (lines, words, confidence)
   - Click "📥 Download Word Document" to save the .docx file

## 🎯 Project Objectives

This application addresses the common problem of converting scanned documents to editable format while maintaining formatting. It serves as an MVP (Minimum Viable Product) for:

- **Problem**: Converting images to Word typically results in plain, unformatted text
- **Solution**: OCR with intelligent formatting detection and preservation
- **Scope**: Single-page, English-language documents with clear text
- **Target Users**: Students, professionals, anyone needing to digitize documents

## 🏗️ Technical Architecture

### Image Processing Pipeline
1. **Preprocessing**
   - Grayscale conversion
   - Otsu's thresholding
   - Noise reduction (Non-local Means Denoising)
   - Morphological operations (dilation/erosion)

2. **OCR Processing**
   - Tesseract OCR with detailed output
   - Line-by-line text extraction
   - Confidence scoring for each detection

3. **Formatting Detection**
   - Heading detection (uppercase, patterns)
   - Bold text identification
   - Text alignment heuristics
   - Paragraph structure preservation

4. **Document Generation**
   - python-docx for Word file creation
   - Font sizing and styling
   - Alignment and spacing
   - Block separation

## 📊 Project Deliverables

✅ **Working Prototype**
- Functional web application deployed on Streamlit Cloud
- Source code available on GitHub

✅ **Features Implemented**
- Image preprocessing
- OCR integration with Tesseract
- Formatting detection (bold, italic, alignment, paragraphs)
- Word document generation with preserved formatting
- User-friendly web interface

✅ **Documentation**
- Comprehensive README
- Inline code comments
- Usage instructions

## 🔄 Future Enhancements (Post-MVP)

- Multi-page document support
- Mathematical equation recognition
- Multi-language support
- Table detection and preservation
- Image extraction and embedding
- Batch processing
- Advanced formatting (fonts, colors, styles)
- Cloud storage integration

## 🐛 Troubleshooting

### Common Issues

**Issue: "Tesseract not found"**
- Solution: Ensure Tesseract is properly installed
- For Windows: Add Tesseract to PATH or set in code:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Issue: Poor OCR accuracy**
- Solution: Use higher resolution images (300 DPI or higher)
- Ensure good contrast and lighting
- Avoid skewed or rotated images

**Issue: Streamlit Cloud deployment fails**
- Solution: Check `packages.txt` is present
- Verify all dependencies are in `requirements.txt`
- Check logs in Streamlit Cloud dashboard

## 📝 License

This project is developed as an academic MVP for educational purposes.

## 📧 Contact

For issues, questions, or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit, OpenCV, and Tesseract OCR**

*Image-to-Word Converter MVP v1.0*
