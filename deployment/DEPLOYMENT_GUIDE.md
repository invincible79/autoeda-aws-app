# AutoEDA AWS Deployment Guide

This guide provides step-by-step instructions for deploying the AutoEDA application on AWS using EC2, Cognito, and S3.

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Domain name (optional but recommended)
- SSH key pair for EC2

## 1. AWS Cognito Setup

### Create User Pool
1. Go to AWS Cognito Console
2. Click "Create user pool"
3. Configure sign-in options:
   - Email
   - Username
4. Configure security requirements:
   - Password policy
   - MFA (optional)
5. Configure sign-up experience
6. Configure message delivery
7. Create app client:
   - Generate client ID and secret
   - Configure OAuth flows
   - Set callback URLs

### Identity Pool Setup
1. Create new identity pool
2. Configure authentication providers:
   - Select Cognito user pool
   - Enter user pool ID and app client ID
3. Configure IAM roles for authenticated and unauthenticated users

## 2. S3 Setup

### Create Buckets
1. Create three S3 buckets:
   - `autoeda-user-uploads`
   - `autoeda-processed-data`
   - `autoeda-assets`
2. Configure bucket policies:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:role/Cognito_AutoEDAIdentityPoolAuth_Role"
               },
               "Action": [
                   "s3:GetObject",
                   "s3:PutObject"
               ],
               "Resource": "arn:aws:s3:::autoeda-*/*"
           }
       ]
   }
   ```
3. Configure CORS:
   ```json
   [
       {
           "AllowedHeaders": ["*"],
           "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
           "AllowedOrigins": ["https://your-domain.com"],
           "ExposeHeaders": []
       }
   ]
   ```

## 3. EC2 Setup

### Launch Instance
1. Launch EC2 instance:
   - AMI: Ubuntu Server 20.04 LTS
   - Instance type: t2.medium or t2.large
   - Configure security group:
     - SSH (22)
     - HTTP (80)
     - HTTPS (443)
     - Custom TCP (8501 for Streamlit)
2. Connect to instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

### Install Dependencies
```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-dev nginx

# Install virtualenv
sudo pip3 install virtualenv

# Create virtual environment
virtualenv venv
source venv/bin/activate

# Install application dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Configure Nginx
1. Create Nginx configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/autoeda
   ```
2. Add configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. Enable site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/autoeda /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### SSL Setup
1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```
2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

## 4. Application Configuration

1. Update `config.py` with AWS credentials and settings
2. Configure environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=your_region
   export COGNITO_USER_POOL_ID=your_pool_id
   export COGNITO_CLIENT_ID=your_client_id
   export S3_BUCKET_USER_UPLOADS=autoeda-user-uploads
   export S3_BUCKET_PROCESSED_DATA=autoeda-processed-data
   ```

## 5. Start Application

1. Create systemd service:
   ```bash
   sudo nano /etc/systemd/system/autoeda.service
   ```
2. Add configuration:
   ```ini
   [Unit]
   Description=AutoEDA Streamlit Application
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/autoeda
   Environment="PATH=/home/ubuntu/autoeda/venv/bin"
   ExecStart=/home/ubuntu/autoeda/venv/bin/streamlit run main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
3. Start service:
   ```bash
   sudo systemctl start autoeda
   sudo systemctl enable autoeda
   ```

## Monitoring and Maintenance

1. Set up CloudWatch for monitoring
2. Configure automatic backups
3. Set up alerts for:
   - High CPU usage
   - Memory usage
   - Disk space
   - Application errors

## Security Considerations

1. Regular security updates
2. Monitor AWS CloudTrail
3. Regular backup of user data
4. Implement rate limiting
5. Regular security audits

## Troubleshooting

1. Check application logs:
   ```bash
   sudo journalctl -u autoeda
   ```
2. Check Nginx logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```
3. Monitor system resources:
   ```bash
   htop
   ``` 