# services/voice_agent.py
import requests
from twilio.rest import Client
import tempfile
import os
import base64
import json
from datetime import datetime

def call_summary_with_voice(elevenlabs_api_key, from_number, to_number, text):
    """
    Enhanced voice calling function with better error handling and user feedback
    """
    try:
        # Validate inputs
        if not elevenlabs_api_key or elevenlabs_api_key == "your_elevenlabs_key":
            raise Exception("Please configure your ElevenLabs API key in config.py")
        
        if not from_number or from_number == "your_twilio_number":
            raise Exception("Please configure your Twilio phone number in config.py")
        
        if not to_number:
            raise Exception("Please provide a valid phone number to call")
        
        # 1. Generate speech with better error handling
        print(f"🎤 Generating speech for: {text[:50]}...")
        tts_response = requests.post(
            "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
            headers={"xi-api-key": elevenlabs_api_key},
            json={
                "text": text, 
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
            },
            timeout=30
        )
        
        if tts_response.status_code != 200:
            error_msg = f"ElevenLabs API error: {tts_response.status_code} - {tts_response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        
        audio = tts_response.content
        print("✅ Speech generated successfully")
        
        # 2. Create a temporary file for the audio
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio.write(audio)
        temp_audio.close()
        
        # 3. For demo purposes, we'll use a simple approach
        # In production, you'd upload this to a cloud storage service
        print("📞 Initiating Twilio call...")
        
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
        
        # 4. Create Twilio client and make call
        client = Client(twilio_sid, twilio_auth_token)
        
        # For demo purposes, we'll use a simple message instead of audio file
        # This avoids the need to host audio files
        demo_message = f"""
        <Response>
            <Say voice="alice" language="en-US">
                {text}
            </Say>
            <Pause length="2"/>
            <Say voice="alice" language="en-US">
                Thank you for using our AI Railway Assistant. Goodbye!
            </Say>
        </Response>
        """
        
        call = client.calls.create(
            twiml=demo_message,
            to=to_number,
            from_=from_number
        )
        
        # Clean up temporary file
        try:
            os.unlink(temp_audio.name)
        except:
            pass
        
        print(f"✅ Call initiated successfully! Call SID: {call.sid}")
        
        return {
            "call_sid": call.sid, 
            "status": "initiated",
            "message": "Call initiated successfully! Check your phone.",
            "timestamp": datetime.now().isoformat(),
            "to_number": to_number,
            "from_number": from_number
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "status": "error",
            "message": error_msg,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        error_msg = f"Voice call error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "status": "error", 
            "message": error_msg,
            "timestamp": datetime.now().isoformat()
        }

def test_voice_integration():
    """
    Test function to verify voice integration is working
    """
    try:
        from config import ELEVENLABS_API_KEY, TWILIO_FROM_NUMBER, TO_NUMBER
        
        print("🧪 Testing voice integration...")
        print(f"ElevenLabs API Key: {'✅ Configured' if ELEVENLABS_API_KEY != 'your_elevenlabs_key' else '❌ Not configured'}")
        print(f"Twilio From Number: {'✅ Configured' if TWILIO_FROM_NUMBER != 'your_twilio_number' else '❌ Not configured'}")
        print(f"Test Phone Number: {'✅ Configured' if TO_NUMBER else '❌ Not configured'}")
        
        # Test with a simple message
        test_message = "Hello! This is a test call from your AI Railway Assistant. If you hear this message, the voice integration is working correctly!"
        
        result = call_summary_with_voice(
            elevenlabs_api_key=ELEVENLABS_API_KEY,
            from_number=TWILIO_FROM_NUMBER,
            to_number=TO_NUMBER,
            text=test_message
        )
        
        print(f"Test Result: {result}")
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return {"status": "error", "message": str(e)}
