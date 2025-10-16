# service/simple_email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class SimpleEmailService:
    def __init__(self):
        """Initialize simple email service"""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Get Gmail credentials from config
        try:
            from config import GMAIL_USER, GMAIL_APP_PASSWORD
            self.gmail_user = GMAIL_USER
            self.gmail_password = GMAIL_APP_PASSWORD
        except ImportError:
            self.gmail_user = os.getenv("GMAIL_USER", "")
            self.gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")
    
    def send_train_info_email(self, recipient_email, train_data, call_details=None):
        """Send train information and call details to user's email"""
        try:
            if not self.gmail_user or not self.gmail_password:
                return {
                    "status": "error",
                    "message": "Gmail credentials not configured. Please add GMAIL_USER and GMAIL_APP_PASSWORD to config.py"
                }
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = recipient_email
            msg['Subject'] = f"🚆 Railway Assistant - {datetime.now().strftime('%B %d, %Y')}"
            
            # Create HTML email content
            html_content = self._create_email_content(train_data, call_details)
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email (use SSL on 465 for Gmail)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)
            
            return {
                "status": "success",
                "message": f"Email sent successfully to {recipient_email}",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _create_email_content(self, train_data, call_details):
        """Create HTML email content with train information and call details"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #667eea; background: #f8f9fa; }}
                .train-info {{ background: #e8f5e8; border-left-color: #28a745; }}
                .call-info {{ background: #e8f4fd; border-left-color: #007bff; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #fff3cd; padding: 10px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚆 Indian Railway Assistant</h1>
                <p>Your Railway Information & Call Details</p>
                <p><strong>Generated on:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        """
        
        # Add train search information
        if train_data.get('search_results'):
            html += f"""
            <div class="section train-info">
                <h2>🔍 Train Search Results</h2>
                <p><strong>From:</strong> {train_data.get('from_station', 'N/A')}</p>
                <p><strong>To:</strong> {train_data.get('to_station', 'N/A')}</p>
                <p><strong>Date:</strong> {train_data.get('date', 'N/A')}</p>
                <div class="highlight">
                    <h3>Available Trains:</h3>
                    <pre>{train_data.get('search_results', 'No trains found')}</pre>
                </div>
            </div>
            """
        
        # Add live status information
        if train_data.get('live_status'):
            html += f"""
            <div class="section train-info">
                <h2>📊 Live Train Status</h2>
                <p><strong>Train Number:</strong> {train_data.get('train_number', 'N/A')}</p>
                <p><strong>Date:</strong> {train_data.get('status_date', 'N/A')}</p>
                <div class="highlight">
                    <h3>Current Status:</h3>
                    <pre>{train_data.get('live_status', 'Status not available')}</pre>
                </div>
            </div>
            """
        
        # Add call details
        if call_details:
            html += f"""
            <div class="section call-info">
                <h2>📞 Voice Call Details</h2>
                <table>
                    <tr><th>Call Type</th><td>{call_details.get('call_type', 'N/A')}</td></tr>
                    <tr><th>Priority</th><td>{call_details.get('priority', 'N/A')}</td></tr>
                    <tr><th>Call SID</th><td>{call_details.get('call_sid', 'N/A')}</td></tr>
                    <tr><th>Status</th><td>{call_details.get('status', 'N/A')}</td></tr>
                    <tr><th>Timestamp</th><td>{call_details.get('timestamp', 'N/A')}</td></tr>
                </table>
                
                <h3>Call Message:</h3>
                <div class="highlight">
                    <p>{call_details.get('message', 'No message available')}</p>
                </div>
                
                {f'<h3>Travel Route:</h3><p><strong>From:</strong> {call_details.get("journey_from", "N/A")} → <strong>To:</strong> {call_details.get("journey_to", "N/A")}</p>' if call_details.get('journey_from') else ''}
                {f'<p><strong>Travel Date:</strong> {call_details.get("journey_date", "N/A")}</p>' if call_details.get('journey_date') else ''}
            </div>
            """
        
        # Add interactive call features
        html += f"""
            <div class="section">
                <h2>🗣️ Interactive Voice Features</h2>
                <p>You can ask the AI Railway Assistant questions like:</p>
                <ul>
                    <li>"What trains are available from Delhi to Mumbai?"</li>
                    <li>"Check the status of train 12617"</li>
                    <li>"Book a ticket from Chennai to Bangalore"</li>
                    <li>"What's the fare for AC 2 tier?"</li>
                    <li>"Help me with ticket cancellation"</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Thank you for using the Indian Railway Assistant!</p>
                <p>For support, please contact our help desk.</p>
                <p><small>This is an automated email from your AI Railway Assistant.</small></p>
            </div>
        </body>
        </html>
        """
        
        return html

def send_railway_email_simple(recipient_email, train_data=None, call_details=None):
    """Main function to send railway information email using simple SMTP"""
    try:
        email_service = SimpleEmailService()
        return email_service.send_train_info_email(recipient_email, train_data or {}, call_details or {})
    except Exception as e:
        return {
            "status": "error",
            "message": f"Simple email service error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
