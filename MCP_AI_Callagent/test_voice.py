#!/usr/bin/env python3
"""
Test script for voice integration
Run this to test if your voice calling setup is working
"""

from service.voice_agent import test_voice_integration

if __name__ == "__main__":
    print("🧪 Testing Voice Integration...")
    print("=" * 50)
    
    result = test_voice_integration()
    
    print("\n" + "=" * 50)
    if result.get("status") == "initiated":
        print("✅ Voice integration test PASSED!")
        print("📞 You should receive a test call shortly.")
    else:
        print("❌ Voice integration test FAILED!")
        print(f"Error: {result.get('message', 'Unknown error')}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API keys in config.py")
        print("2. Verify your Twilio account has credits")
        print("3. Ensure phone numbers are in correct format (+country code)")
        print("4. Check if your Twilio number is verified")
    
    print("\n📋 Test Details:")
    print(result)
