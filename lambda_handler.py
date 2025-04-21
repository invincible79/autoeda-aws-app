import json
import boto3
import pandas as pd
import io
import base64
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def generate_report(data_analysis_results):
    """Generate HTML report from analysis results"""
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #1a237e; color: white; padding: 20px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; }}
                .plot {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>AutoEDA Analysis Report</h1>
            </div>
            {data_analysis_results}
        </body>
    </html>
    """
    return html_content

def send_email(recipient, subject, html_content, sender="your-verified-email@domain.com"):
    """Send email using Amazon SES"""
    ses_client = boto3.client('ses')
    
    # Create message container
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    # Create the HTML part
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        response = ses_client.send_raw_email(
            Source=sender,
            Destinations=[recipient],
            RawMessage={'Data': msg.as_string()}
        )
        return True, "Email sent successfully!"
    except ClientError as e:
        return False, f"Error sending email: {str(e)}"

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        # Parse the incoming event
        body = json.loads(event['body'])
        recipient_email = body['email']
        analysis_results = body['analysis_results']
        
        # Generate the report
        report_html = generate_report(analysis_results)
        
        # Send email
        success, message = send_email(
            recipient=recipient_email,
            subject="Your AutoEDA Analysis Report",
            html_content=report_html
        )
        
        return {
            'statusCode': 200 if success else 500,
            'body': json.dumps({
                'message': message
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        } 