import json
import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
from datetime import datetime

def generate_html_report(analysis_results):
    """Generate HTML report from analysis results"""
    try:
        original_data = analysis_results.get('original_data', {})
        processed_data = analysis_results.get('processed_data', {})
        
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        color: #333;
                    }}
                    .header {{
                        background-color: #1a237e;
                        color: white;
                        padding: 20px;
                        margin-bottom: 30px;
                    }}
                    .section {{
                        margin: 20px 0;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 15px 0;
                    }}
                    th, td {{
                        padding: 12px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f8f9fa;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>AutoEDA Analysis Report</h1>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
        """
        
        # Original Data Section
        if original_data:
            html_content += """
                <div class="section">
                    <h2>Original Dataset Analysis</h2>
            """
            
            # Dataset Overview
            html_content += f"""
                    <h3>Dataset Overview</h3>
                    <table>
                        <tr><td>Total Rows</td><td>{original_data.get('total_rows', 0)}</td></tr>
                        <tr><td>Total Columns</td><td>{original_data.get('total_columns', 0)}</td></tr>
                        <tr><td>Numerical Columns</td><td>{', '.join(original_data.get('numerical_columns', []))}</td></tr>
                        <tr><td>Categorical Columns</td><td>{', '.join(original_data.get('categorical_columns', []))}</td></tr>
                    </table>
            """
            
            # Missing Values
            if 'missing_values' in original_data:
                missing_data = {k: v for k, v in original_data['missing_values'].items() if v > 0}
                if missing_data:
                    html_content += """
                        <h3>Missing Values</h3>
                        <table>
                            <tr><th>Column</th><th>Missing Count</th></tr>
                    """
                    for col, count in missing_data.items():
                        html_content += f"<tr><td>{col}</td><td>{count}</td></tr>"
                    html_content += "</table>"
            
            # Numerical Statistics
            if 'numerical_stats' in original_data:
                html_content += """
                    <h3>Numerical Column Statistics</h3>
                    <table>
                        <tr><th>Column</th><th>Mean</th><th>Std</th><th>Min</th><th>Max</th></tr>
                """
                for col, stats in original_data['numerical_stats'].items():
                    html_content += f"""
                        <tr>
                            <td>{col}</td>
                            <td>{stats['mean']:.2f}</td>
                            <td>{stats['std']:.2f}</td>
                            <td>{stats['min']:.2f}</td>
                            <td>{stats['max']:.2f}</td>
                        </tr>
                    """
                html_content += "</table>"
            
            # Categorical Statistics
            if 'categorical_stats' in original_data:
                html_content += "<h3>Categorical Column Value Counts (Top 5)</h3>"
                for col, counts in original_data['categorical_stats'].items():
                    html_content += f"""
                        <h4>{col}</h4>
                        <table>
                            <tr><th>Value</th><th>Count</th></tr>
                    """
                    for val, count in counts.items():
                        html_content += f"<tr><td>{val}</td><td>{count}</td></tr>"
                    html_content += "</table>"
            
            html_content += "</div>"
        
        # Processed Data Section
        if processed_data:
            html_content += """
                <div class="section">
                    <h2>Processed Dataset Analysis</h2>
            """
            
            # Dataset Overview
            html_content += f"""
                    <h3>Dataset Overview</h3>
                    <table>
                        <tr><td>Total Rows</td><td>{processed_data.get('total_rows', 0)}</td></tr>
                        <tr><td>Total Columns</td><td>{processed_data.get('total_columns', 0)}</td></tr>
                        <tr><td>Numerical Columns</td><td>{', '.join(processed_data.get('numerical_columns', []))}</td></tr>
                        <tr><td>Categorical Columns</td><td>{', '.join(processed_data.get('categorical_columns', []))}</td></tr>
                    </table>
            """
            
            # Changes in Structure
            if original_data:
                added_cols = set(processed_data.get('column_types', {}).keys()) - set(original_data.get('column_types', {}).keys())
                removed_cols = set(original_data.get('column_types', {}).keys()) - set(processed_data.get('column_types', {}).keys())
                
                if added_cols or removed_cols:
                    html_content += "<h3>Changes in Structure</h3><table>"
                    if added_cols:
                        html_content += f"<tr><td>Added Columns</td><td>{', '.join(added_cols)}</td></tr>"
                    if removed_cols:
                        html_content += f"<tr><td>Removed Columns</td><td>{', '.join(removed_cols)}</td></tr>"
                    html_content += "</table>"
            
            html_content += "</div>"
        
        html_content += """
            </body>
        </html>
        """
        
        return html_content
    except Exception as e:
        return f"<p>Error generating report: {str(e)}</p>"

def send_email(recipient, subject, html_content, pdf_url):
    """Send email using Amazon SES"""
    try:
        ses_client = boto3.client('ses')
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = os.environ['SES_SENDER_EMAIL']
        msg['To'] = recipient
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Download and attach PDF
        if pdf_url:
            response = requests.get(pdf_url)
            if response.status_code == 200:
                pdf_attachment = MIMEApplication(response.content, _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename='analysis_report.pdf')
                msg.attach(pdf_attachment)
        
        # Send email
        response = ses_client.send_raw_email(
            Source=os.environ['SES_SENDER_EMAIL'],
            Destinations=[recipient],
            RawMessage={'Data': msg.as_string()}
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def lambda_handler(event, context):
    try:
        # Parse the event body
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        # Extract data
        email = body['email']
        analysis_results = body['analysis_results']
        pdf_url = body.get('pdf_url')
        
        # Generate report
        html_content = generate_html_report(analysis_results)
        
        # Send email
        success = send_email(
            recipient=email,
            subject="Your AutoEDA Analysis Report",
            html_content=html_content,
            pdf_url=pdf_url
        )
        
        return {
            'statusCode': 200 if success else 500,
            'body': json.dumps({
                'message': 'Report sent successfully!' if success else 'Failed to send report'
            })
        }
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 