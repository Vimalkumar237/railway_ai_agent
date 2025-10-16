# services/simple_interactive_agent.py
import requests
from twilio.rest import Client
import os
from datetime import datetime

def create_simple_interactive_call(to_number, from_number):
    """
    Create a simple interactive call that demonstrates the concept
    This version uses a pre-recorded message that explains how interactive calls work
    """
    try:
        # Get Twilio credentials
        try:
            from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
            twilio_sid = TWILIO_ACCOUNT_SID
            twilio_auth_token = TWILIO_AUTH_TOKEN
        except ImportError:
            twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "your_twilio_sid")
            twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "your_twilio_auth_token")
        
        if twilio_sid == "your_twilio_sid" or twilio_auth_token == "your_twilio_auth_token":
            raise Exception("Please configure your Twilio credentials in config.py")
        
        client = Client(twilio_sid, twilio_auth_token)
        
        # Create an interactive message that explains the concept
        interactive_message = """
        <Response>
            <Say voice="alice" language="en-US">
                Hello! Welcome to your Interactive AI Railway Assistant!
                
                This is a demonstration of how interactive voice calls work. In a full implementation, you would be able to ask me questions like:
                
                "What trains are available from Delhi to Mumbai?"
                "Check the status of train 12617"
                "Book a ticket from Chennai to Bangalore"
                "What's the fare for AC 2 tier?"
                
                And I would respond with real-time information and help you with your railway queries.
                
                To enable full interactive functionality, you would need to:
                1. Set up a webhook server
                2. Configure Twilio to send speech input to your server
                3. Process the speech and generate AI responses
                
                For now, this is a demonstration call. Thank you for trying our Interactive Railway Assistant!
            </Say>
            <Pause length="2"/>
            <Say voice="alice" language="en-US">
                To experience full interactive calls, please run the webhook server and configure your Twilio webhook URL.
            </Say>
        </Response>
        """
        
        call = client.calls.create(
            twiml=interactive_message,
            to=to_number,
            from_=from_number
        )
        
        return {
            "call_sid": call.sid,
            "status": "initiated",
            "message": "Interactive demo call initiated! Check your phone for the demonstration.",
            "timestamp": datetime.now().isoformat(),
            "note": "This is a demo. For full interactivity, run webhook_server.py"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Interactive call error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def get_interactive_features():
    """Return information about interactive features"""
    return {
        "features": [
            "Real-time speech recognition",
            "AI-powered responses to railway queries",
            "Multi-turn conversations",
            "Train search and booking assistance",
            "Fare inquiries and status checks"
        ],
        "example_questions": [
            "What trains are available from Delhi to Mumbai?",
            "Check the status of train 12617",
            "Book a ticket from Chennai to Bangalore",
            "What's the fare for AC 2 tier?",
            "Tell me about train schedules",
            "Help me with ticket cancellation"
        ],
        "setup_required": [
            "Run webhook server: python webhook_server.py",
            "Configure Twilio webhook URL",
            "Ensure phone number is verified (for trial accounts)"
        ]
    }
