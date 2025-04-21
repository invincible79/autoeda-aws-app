import streamlit as st
import pyautogui
import tempfile
import os
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import base64
from reportlab.lib.utils import ImageReader

class ScreenshotService:
    @staticmethod
    def capture_streamlit_screen():
        """
        Captures the current Streamlit app screen
        """
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            st.error(f"Error capturing screenshot: {str(e)}")
            return None

    @staticmethod
    def create_pdf_from_screenshot(screenshot):
        """
        Converts a screenshot to PDF
        """
        try:
            # Create a temporary file for the PDF
            pdf_path = tempfile.mktemp(suffix='.pdf')
            
            # Create PDF
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Save screenshot to a temporary file
            temp_img_path = tempfile.mktemp(suffix='.png')
            screenshot.save(temp_img_path, format='PNG')
            
            # Calculate dimensions
            img_width, img_height = screenshot.size
            aspect = img_height / float(img_width)
            
            # Scale image to fit page
            width, height = letter
            pdf_width = width - 40  # 20pt margins
            pdf_height = pdf_width * aspect
            
            # Add image to PDF using the temporary file
            c.drawImage(temp_img_path, 20, height - pdf_height - 20,
                       width=pdf_width, height=pdf_height)
            c.save()
            
            # Clean up temporary image file
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
            return pdf_path
        except Exception as e:
            st.error(f"Error creating PDF: {str(e)}")
            return None

    @staticmethod
    def get_pdf_as_base64(pdf_path):
        """
        Converts PDF file to base64 string
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_bytes = file.read()
            return base64.b64encode(pdf_bytes).decode('utf-8')
        except Exception as e:
            st.error(f"Error converting PDF to base64: {str(e)}")
            return None
        finally:
            # Clean up temporary file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

# Initialize the service
screenshot_service = ScreenshotService() 