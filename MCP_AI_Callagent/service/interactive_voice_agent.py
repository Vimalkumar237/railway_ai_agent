# services/interactive_voice_agent.py
import requests
from twilio.rest import Client
from twilio.twiml import VoiceResponse
import json
import os
from datetime import datetime

class InteractiveRailwayAgent:
    def __init__(self):
        """Initialize the interactive railway voice agent"""
        try:
            from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, ELEVENLABS_API_KEY
            self.twilio_sid = TWILIO_ACCOUNT_SID
            self.twilio_auth_token = TWILIO_AUTH_TOKEN
            self.elevenlabs_key = ELEVENLABS_API_KEY
        except ImportError:
            raise Exception("Please configure your API keys in config.py")
    
    def create_interactive_call(self, to_number, from_number):
        """Create an interactive call where users can ask questions"""
        try:
            client = Client(self.twilio_sid, self.twilio_auth_token)
            
            # Create a webhook URL for handling user input
            # For demo, we'll use a simple approach with TwiML
            welcome_message = """
            <Response>
                <Say voice="alice" language="en-US">
                    Hello! Welcome to your AI Railway Assistant. I can help you with train bookings, schedules, and travel information.
                    You can ask me questions like:
                    - "What trains are available from Delhi to Mumbai?"
                    - "Check the status of train 12617"
                    - "Book a ticket from Chennai to Bangalore"
                    - "What's the fare for AC 2 tier?"
                    
                    Please speak your question after the beep.
                </Say>
                <Gather input="speech" action="/handle_speech" method="POST" 
                        speechTimeout="auto" language="en-US" 
                        speechModel="phone_call" enhanced="true">
                    <Say voice="alice">Please ask your railway question now.</Say>
                </Gather>
                <Say voice="alice">I didn't hear anything. Please call back and try again.</Say>
            </Response>
            """
            
            call = client.calls.create(
                twiml=welcome_message,
                to=to_number,
                from_=from_number
            )
            
            return {
                "call_sid": call.sid,
                "status": "initiated",
                "message": "Interactive call initiated! User can now ask questions.",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create interactive call: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def handle_user_question(self, user_speech):
        """Process user's question and generate appropriate response"""
        
        # Convert speech to text (in real implementation, this would come from Twilio)
        user_text = user_speech.lower()
        
        # Railway knowledge base and responses
        responses = {
            "train_search": {
                "keywords": ["train", "available", "schedule", "from", "to", "between"],
                "response": "I can help you find trains! Please tell me your source and destination stations. For example: 'Find trains from Delhi to Mumbai'"
            },
            "booking": {
                "keywords": ["book", "ticket", "reservation", "seat", "fare"],
                "response": "I can help you book tickets! Please provide your travel details: source, destination, date, and passenger count."
            },
            "status": {
                "keywords": ["status", "running", "delay", "on time", "train number"],
                "response": "I can check train status for you! Please provide the train number and date."
            },
            "fare": {
                "keywords": ["fare", "price", "cost", "how much"],
                "response": "I can help you check fares! Please tell me your source, destination, and travel class (AC 2 tier, sleeper, etc.)."
            },
            "general": {
                "keywords": ["help", "information", "assist"],
                "response": "I'm your AI Railway Assistant! I can help with train searches, bookings, status checks, and fare inquiries. What would you like to know?"
            }
        }
        
        # Determine the type of question
        question_type = "general"
        for category, data in responses.items():
            if any(keyword in user_text for keyword in data["keywords"]):
                question_type = category
                break
        
        return responses[question_type]["response"]
    
    def create_response_twiml(self, response_text):
        """Create TwiML response for the AI agent"""
        resp = VoiceResponse()
        
        # Add the AI response
        resp.say(response_text, voice='alice', language='en-US')
        
        # Ask if user has more questions
        resp.say("Do you have any other questions? Please speak after the beep.", voice='alice')
        
        # Gather more input
        gather = resp.gather(
            input='speech',
            action='/handle_speech',
            method='POST',
            speech_timeout='auto',
            language='en-US',
            speech_model='phone_call',
            enhanced='true'
        )
        
        # Fallback if no input
        resp.say("Thank you for using our AI Railway Assistant. Have a great journey!", voice='alice')
        
        return str(resp)

def create_interactive_railway_call(to_number, from_number):
    """Main function to create an interactive railway call"""
    try:
        agent = InteractiveRailwayAgent()
        return agent.create_interactive_call(to_number, from_number)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Interactive call error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def process_user_speech(speech_text):
    """Process user speech and return AI response"""
    try:
        agent = InteractiveRailwayAgent()
        response = agent.handle_user_question(speech_text)
        return agent.create_response_twiml(response)
    except Exception as e:
        return f"""
        <Response>
            <Say voice="alice">Sorry, I encountered an error. Please try again.</Say>
        </Response>
        """
