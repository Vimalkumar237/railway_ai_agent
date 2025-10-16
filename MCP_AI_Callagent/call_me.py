#!/usr/bin/env python3
"""
Simple script to make a voice call using the voice agent
"""

import os
from service.voice_agent import call_summary_with_voice

def make_call(message=None):
    try:
        from config import ELEVENLABS_API_KEY, TWILIO_FROM_NUMBER, TO_NUMBER, DEFAULT_MESSAGE
    except ImportError:
        print("❌ Configuration file not found or incomplete!")
        print("Please create a config.py file with your API keys and phone numbers.")
        return None
    
    # Use provided message or default
    if message is None:
        message = DEFAULT_MESSAGE
    
    try:
        print("📞 Making call...")
        print(f"From: {TWILIO_FROM_NUMBER}")
        print(f"To: {TO_NUMBER}")
        print(f"Message: {message}")
        
        result = call_summary_with_voice(
            ELEVENLABS_API_KEY,
            TWILIO_FROM_NUMBER,
            TO_NUMBER,
            message
        )
        
        print("✅ Call initiated successfully!")
        print(f"Call SID: {result['call_sid']}")
        print(f"Status: {result['status']}")
        return result
        
    except Exception as e:
        print(f"❌ Error making call: {e}")
        return None

if __name__ == "__main__":
    print("🎯 Voice Call Script")
    print("===================")
    print()
    
    # Check if config exists
    try:
        from config import ELEVENLABS_API_KEY, TWILIO_FROM_NUMBER, TO_NUMBER
        print("✅ Configuration loaded successfully!")
    except ImportError:
        print("❌ Configuration not found!")
        print("\n📋 Setup Instructions:")
        print("1. Create a config.py file with your API keys")
        print("2. Get ElevenLabs API key from: https://elevenlabs.io/")
        print("3. Get Twilio credentials from: https://www.twilio.com/")
        print("4. Update the phone numbers in config.py")
        print("\nExample config.py:")
        print("ELEVENLABS_API_KEY = 'your_key_here'")
        print("TWILIO_ACCOUNT_SID = 'your_sid_here'")
        print("TWILIO_AUTH_TOKEN = 'your_token_here'")
        print("TWILIO_FROM_NUMBER = '+1234567890'")
        print("TO_NUMBER = '+1234567890'")
        exit(1)
    
    # Check if credentials are set
    if (ELEVENLABS_API_KEY == "your_elevenlabs_api_key_here" or 
        TWILIO_FROM_NUMBER == "+1234567890" or 
        TO_NUMBER == "+1234567890"):
        print("❌ Please update the configuration in config.py with your actual credentials!")
        exit(1)
    
    # Make the call
    print("🚀 Ready to make call!")
    custom_message = input("Enter custom message (or press Enter for default): ").strip()
    
    if custom_message:
        make_call(custom_message)
    else:
        make_call()
