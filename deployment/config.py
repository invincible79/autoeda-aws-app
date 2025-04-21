import os
import boto3
from botocore.config import Config

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Cognito Configuration
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_REGION = os.getenv('COGNITO_REGION', AWS_REGION)

# S3 Configuration
S3_BUCKET_USER_UPLOADS = os.getenv('S3_BUCKET_USER_UPLOADS', 'autoeda-user-uploads')
S3_BUCKET_PROCESSED_DATA = os.getenv('S3_BUCKET_PROCESSED_DATA', 'autoeda-processed-data')
S3_BUCKET_ASSETS = os.getenv('S3_BUCKET_ASSETS', 'autoeda-assets')

# AWS Clients Configuration
config = Config(
    region_name=AWS_REGION,
    retries=dict(
        max_attempts=3
    )
)

# Initialize AWS Clients
cognito_client = boto3.client(
    'cognito-idp',
    region_name=COGNITO_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=config
)

s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=config
)

# Application Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Security Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://your-domain.com').split(',')
RATE_LIMIT = "100/minute"  # Adjust based on your needs

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = '/var/log/autoeda/application.log'

# Backup Configuration
BACKUP_ENABLED = True
BACKUP_FREQUENCY = 'daily'  # daily, weekly, monthly
BACKUP_RETENTION_DAYS = 30 