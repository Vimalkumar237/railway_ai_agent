#!/usr/bin/env python3
"""
Test script for interactive voice call functionality
"""

from service.simple_interactive_agent import create_simple_interactive_call, get_interactive_features

def test_interactive_call():
    """Test the interactive call functionality"""
    try:
        from config import TWILIO_FROM_NUMBER, TO_NUMBER
        
        print("🗣️ Testing Interactive Voice Call...")
        print("=" * 60)
        
        # Show interactive features
        features = get_interactive_features()
        print("📋 Interactive Features:")
        for feature in features["features"]:
            print(f"  • {feature}")
        
        print("\n💬 Example Questions:")
        for question in features["example_questions"]:
            print(f"  • '{question}'")
        
        print("\n🔧 Setup Required:")
        for step in features["setup_required"]:
            print(f"  • {step}")
        
        print("\n" + "=" * 60)
        print("📞 Initiating Interactive Call...")
        
        result = create_simple_interactive_call(TO_NUMBER, TWILIO_FROM_NUMBER)
        
        print("\n" + "=" * 60)
        if result.get("status") == "initiated":
            print("✅ Interactive call test PASSED!")
            print(f"📞 Call SID: {result.get('call_sid')}")
            print("🎯 You should receive a demonstration call shortly.")
            print("💡 This call explains how interactive voice calls work.")
        else:
            print("❌ Interactive call test FAILED!")
            print(f"Error: {result.get('message', 'Unknown error')}")
        
        print("\n📋 Test Details:")
        print(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    test_interactive_call()
