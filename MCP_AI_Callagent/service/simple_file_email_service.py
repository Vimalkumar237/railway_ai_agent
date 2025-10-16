# service/simple_file_email_service.py
from datetime import datetime
import os
import json

class SimpleFileEmailService:
    def __init__(self):
        """Initialize simple file-based email service"""
        self.emails_dir = "emails"
        self._ensure_emails_directory()
    
    def _ensure_emails_directory(self):
        """Create emails directory if it doesn't exist"""
        if not os.path.exists(self.emails_dir):
            os.makedirs(self.emails_dir)
    
    def send_train_info_email(self, recipient_email, train_data, call_details=None):
        """Save train information and call details to a file (simulates email sending)"""
        try:
            # Create email content
            subject = f"🚆 Railway Assistant - {datetime.now().strftime('%B %d, %Y')}"
            html_content = self._create_email_content(train_data, call_details)
            
            # Create email data
            email_data = {
                "to": recipient_email,
                "subject": subject,
                "html_content": html_content,
                "timestamp": datetime.now().isoformat(),
                "method": "file_save"
            }
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_{timestamp}_{recipient_email.replace('@', '_at_').replace('.', '_')}.json"
            filepath = os.path.join(self.emails_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(email_data, f, indent=2, ensure_ascii=False)
            
            return {
                "status": "success",
                "message": f"Email saved to file: {filename}",
                "timestamp": datetime.now().isoformat(),
                "method": "file_save",
                "filepath": filepath
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to save email: {str(e)}",
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

def send_railway_email_file(recipient_email, train_data=None, call_details=None):
    """Main function to save railway information email to file"""
    try:
        email_service = SimpleFileEmailService()
        return email_service.send_train_info_email(recipient_email, train_data or {}, call_details or {})
    except Exception as e:
        return {
            "status": "error",
            "message": f"File email service error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
