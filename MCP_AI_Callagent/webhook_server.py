#!/usr/bin/env python3
"""
Flask webhook server for interactive voice calls
This handles the two-way conversation between users and the AI railway agent
"""

from flask import Flask, request, Response
from service.interactive_voice_agent import InteractiveRailwayAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/handle_speech', methods=['POST'])
def handle_speech():
    """Handle user speech input and return AI response"""
    try:
        # Get user's speech input from Twilio
        user_speech = request.form.get('SpeechResult', '')
        confidence = request.form.get('Confidence', 0)
        
        logger.info(f"Received speech: '{user_speech}' (confidence: {confidence})")
        
        if not user_speech:
            # No speech detected
            twiml_response = """
            <Response>
                <Say voice="alice" language="en-US">
                    I didn't hear your question clearly. Please try again.
                </Say>
                <Gather input="speech" action="/handle_speech" method="POST" 
                        speechTimeout="auto" language="en-US" 
                        speechModel="phone_call" enhanced="true">
                    <Say voice="alice">Please repeat your question.</Say>
                </Gather>
            </Response>
            """
        else:
            # Process the user's question
            agent = InteractiveRailwayAgent()
            response = agent.handle_user_question(user_speech)
            twiml_response = agent.create_response_twiml(response)
        
        return Response(twiml_response, mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error handling speech: {e}")
        error_response = """
        <Response>
            <Say voice="alice" language="en-US">
                Sorry, I encountered an error. Please try again.
            </Say>
        </Response>
        """
        return Response(error_response, mimetype='text/xml')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "interactive_voice_agent"}

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return """
    <h1>Interactive Railway Voice Agent</h1>
    <p>This server handles interactive voice calls for the Railway Assistant.</p>
    <p>Status: Running</p>
    """

if __name__ == '__main__':
    print("🚀 Starting Interactive Voice Agent Webhook Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔗 Webhook URL: http://localhost:5000/handle_speech")
    print("💡 Make sure to update your Twilio webhook URL to point to this server")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
