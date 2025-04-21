import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# AWS Cognito Configuration
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')  # Default to us-east-1 if not specified

# Initialize Cognito client
cognito_client = boto3.client(
    'cognito-idp',
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
) 