import boto3
import json
import streamlit as st
from botocore.exceptions import ClientError
from screenshot_service import screenshot_service
import os
from dotenv import load_dotenv
import pandas as pd
import uuid

# Load environment variables
load_dotenv()

class ReportService:
    def __init__(self):
        # Get AWS credentials and region from environment variables
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        # Initialize boto3 clients
        self.lambda_client = boto3.client(
            'lambda',
            region_name=self.aws_region,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.s3_client = boto3.client(
            's3',
            region_name=self.aws_region,
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        self.lambda_function_name = 'autoeda-report-generator'
        self.s3_bucket = os.getenv('S3_BUCKET_NAME', 'autoeda-reports')
    
    def _convert_to_serializable(self, obj):
        """Convert DataFrame and other non-serializable objects to JSON-serializable format"""
        if isinstance(obj, pd.DataFrame):
            return {
                'data': obj.to_dict(orient='records'),
                'columns': obj.columns.tolist(),
                'index': obj.index.tolist()
            }
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, (pd.Timestamp, pd.Timedelta)):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        return obj
    
    def _upload_to_s3(self, file_path, content_type='application/pdf'):
        """Upload a file to S3 and return its URL"""
        try:
            # Generate a unique filename
            file_name = f"report_{uuid.uuid4()}.pdf"
            
            # Upload file to S3
            with open(file_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    self.s3_bucket,
                    file_name,
                    ExtraArgs={
                        'ContentType': content_type,
                        'ACL': 'private'
                    }
                )
            
            # Generate a presigned URL that expires in 1 hour
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.s3_bucket,
                    'Key': file_name
                },
                ExpiresIn=3600
            )
            
            return url
        except Exception as e:
            st.error(f"Error uploading to S3: {str(e)}")
            return None
    
    def generate_and_email_report(self, email, analysis_results):
        """
        Captures screenshot, converts to PDF, uploads to S3, and sends via email
        
        Args:
            email (str): Recipient email address
            analysis_results (dict or DataFrame): Analysis results to include in the report
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Convert analysis results to serializable format
            serializable_results = self._convert_to_serializable(analysis_results)
            
            # Capture screenshot
            screenshot = screenshot_service.capture_streamlit_screen()
            if screenshot is None:
                return False, "Failed to capture screenshot"
            
            # Convert to PDF
            pdf_path = screenshot_service.create_pdf_from_screenshot(screenshot)
            if pdf_path is None:
                return False, "Failed to create PDF"
            
            # Upload PDF to S3
            pdf_url = self._upload_to_s3(pdf_path)
            if pdf_url is None:
                return False, "Failed to upload PDF to S3"
            
            # Clean up the local PDF file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            
            # Prepare the payload for Lambda
            payload = {
                'body': json.dumps({
                    'email': email,
                    'analysis_results': serializable_results,
                    'pdf_url': pdf_url
                })
            }
            
            # Invoke Lambda function asynchronously
            response = self.lambda_client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType='Event',
                Payload=json.dumps(payload)
            )
            
            if response['StatusCode'] == 202:
                return True, "Report generation started. You will receive an email shortly."
            else:
                return False, "Failed to start report generation. Please try again."
                
        except ClientError as e:
            return False, f"Error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

# Initialize the service
report_service = ReportService() 