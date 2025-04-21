#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting AutoEDA deployment...${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Update system
echo -e "${GREEN}Updating system...${NC}"
apt update
apt upgrade -y

# Install required packages
echo -e "${GREEN}Installing required packages...${NC}"
apt install -y python3-pip python3-dev nginx certbot python3-certbot-nginx

# Create application directory
echo -e "${GREEN}Creating application directory...${NC}"
mkdir -p /var/www/autoeda
chown -R ubuntu:www-data /var/www/autoeda

# Setup Python virtual environment
echo -e "${GREEN}Setting up Python virtual environment...${NC}"
cd /var/www/autoeda
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install -r requirements.txt
pip install gunicorn boto3

# Configure Nginx
echo -e "${GREEN}Configuring Nginx...${NC}"
cat > /etc/nginx/sites-available/autoeda << EOL
server {
    listen 80;
    server_name \$host;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

# Enable Nginx site
ln -sf /etc/nginx/sites-available/autoeda /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Setup SSL with Certbot
echo -e "${GREEN}Setting up SSL...${NC}"
certbot --nginx -d $(hostname) --non-interactive --agree-tos --email admin@$(hostname)

# Create systemd service
echo -e "${GREEN}Creating systemd service...${NC}"
cat > /etc/systemd/system/autoeda.service << EOL
[Unit]
Description=AutoEDA Streamlit Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/autoeda
Environment="PATH=/var/www/autoeda/venv/bin"
Environment="AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}"
Environment="AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
Environment="AWS_REGION=${AWS_REGION}"
Environment="COGNITO_USER_POOL_ID=${COGNITO_USER_POOL_ID}"
Environment="COGNITO_CLIENT_ID=${COGNITO_CLIENT_ID}"
Environment="S3_BUCKET_USER_UPLOADS=${S3_BUCKET_USER_UPLOADS}"
Environment="S3_BUCKET_PROCESSED_DATA=${S3_BUCKET_PROCESSED_DATA}"
ExecStart=/var/www/autoeda/venv/bin/streamlit run main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Start and enable service
echo -e "${GREEN}Starting AutoEDA service...${NC}"
systemctl daemon-reload
systemctl enable autoeda
systemctl start autoeda

# Setup logging
echo -e "${GREEN}Setting up logging...${NC}"
mkdir -p /var/log/autoeda
chown -R ubuntu:www-data /var/log/autoeda

# Setup backup
echo -e "${GREEN}Setting up backup...${NC}"
mkdir -p /var/backups/autoeda
chown -R ubuntu:www-data /var/backups/autoeda

# Add backup cron job
(crontab -l 2>/dev/null; echo "0 0 * * * /usr/bin/tar -czf /var/backups/autoeda/backup-\$(date +\%Y\%m\%d).tar.gz /var/www/autoeda") | crontab -

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}The application is now running at https://$(hostname)${NC}" 