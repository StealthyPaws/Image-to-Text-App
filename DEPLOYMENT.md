# 🚀 Deployment Guide - Streamlit Cloud

## Quick Deployment Steps

### Step 1: Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Upload these files to your repository:
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `.streamlit/config.toml`
   - `README.md`
   - `.gitignore`

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your GitHub repository
   - Choose the branch (usually `main` or `master`)
   - Set main file path: `app.py`

3. **Advanced Settings (Optional)**
   - You can customize the app URL
   - Set environment variables if needed
   - Configure secrets (not required for this app)

4. **Deploy**
   - Click "Deploy!" button
   - Wait 2-5 minutes for deployment
   - Your app will be live at: `https://[your-app-name].streamlit.app`

## Important Notes

### System Dependencies
The `packages.txt` file is CRITICAL for this app because it installs Tesseract OCR on the Streamlit Cloud server:
```
tesseract-ocr
tesseract-ocr-eng
libtesseract-dev
```

Without this file, the OCR functionality won't work!

### Python Dependencies
All required Python packages are in `requirements.txt`. Streamlit Cloud will automatically install them.

### Free Tier Limitations
- 1 GB RAM (sufficient for this app)
- Limited compute resources
- Apps sleep after inactivity (wake up automatically)
- Public apps only (private apps require paid plan)

## Testing Your Deployment

1. **Access the App**
   - Open the provided URL
   - App should load within 10-20 seconds

2. **Test Upload**
   - Try uploading a sample image
   - Check if preview displays correctly

3. **Test Conversion**
   - Click "Convert to Word"
   - Verify processing completes
   - Download and check the Word document

4. **Check Logs**
   - In Streamlit Cloud dashboard, click "Manage app"
   - View logs for any errors
   - Monitor resource usage

## Troubleshooting

### Deployment Fails
- Check all files are committed to GitHub
- Verify `packages.txt` is in root directory
- Check `requirements.txt` has correct versions
- Review deployment logs in Streamlit Cloud

### App Crashes
- Check file sizes (max 10MB for uploads)
- Monitor RAM usage in logs
- Ensure images are valid formats
- Check Tesseract installation in logs

### OCR Not Working
- Verify `packages.txt` deployed correctly
- Check logs for Tesseract errors
- Try with simpler, clearer images first

## Alternative Deployment Options

### 1. Hugging Face Spaces
```bash
# requirements.txt stays the same
# Add a Dockerfile:
FROM python:3.9
RUN apt-get update && apt-get install -y tesseract-ocr
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### 2. Heroku
```bash
# Add Procfile:
web: sh setup.sh && streamlit run app.py

# Add setup.sh:
mkdir -p ~/.streamlit/
echo "[server]
port = $PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml

# Add Aptfile for Tesseract:
tesseract-ocr
tesseract-ocr-eng
```

### 3. Google Cloud Run
- Build Docker image with Tesseract
- Deploy to Cloud Run
- More control but requires more setup

## Sharing Your App

Once deployed, share your app:
1. Copy the app URL (e.g., `https://image-to-word.streamlit.app`)
2. Share via WhatsApp as required
3. Share GitHub repository link
4. Both links should be included in your submission

## Monitoring and Maintenance

- **Check Analytics**: Streamlit Cloud provides usage analytics
- **Update Code**: Push to GitHub, app auto-redeploys
- **Monitor Performance**: Watch for slow load times
- **User Feedback**: Add feedback mechanism if needed

## Cost Considerations

**Streamlit Cloud Free Tier:**
- ✅ Sufficient for this MVP
- ✅ Unlimited public apps
- ✅ Auto-deployment from GitHub
- ❌ Limited resources per app
- ❌ Apps sleep after inactivity

**Paid Options (if needed later):**
- More resources
- Private apps
- Custom domains
- Priority support

## Success Checklist

Before submitting:
- [ ] App deploys successfully
- [ ] Image upload works
- [ ] OCR conversion works
- [ ] Word document downloads
- [ ] App URL is accessible
- [ ] GitHub repository is public
- [ ] README is complete
- [ ] All files are committed

## Support Resources

- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- Tesseract Documentation: https://tesseract-ocr.github.io
- Python-docx Documentation: https://python-docx.readthedocs.io

---

**Good luck with your deployment! 🚀**
