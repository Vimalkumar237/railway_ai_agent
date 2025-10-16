#!/usr/bin/env python3
"""
Test script to show Gmail MCP API works without SMTP credentials
"""

from service.gmail_mcp_service import send_railway_email_mcp

def test_mcp_only():
    """Test the Gmail MCP API without SMTP fallback"""
    try:
        print("📧 Testing Gmail MCP API Only (No SMTP)...")
        print("=" * 60)
        
        # Test email data
        test_email = "test@example.com"  # Replace with your email for testing
        
        # Sample train data
        train_data = {
            'search_results': """
🚆 TRAINS FROM MAS TO SA (20250115)

Train    Name                Departure      Arrival        Duration  Classes  Days
---------------------------------------------------------------------------------
12617   MANGALA EXPRESS      MAS 15:20 → SA 20:02 04:42H   1A,2A,3A,SL SMTWTFS
12243   SHATABDI EXP         MAS 07:15 → SA 11:18 04:03H   EC,CC    SMWTFS
22639   ALLEPPEY EXP         MAS 20:55 → SA 01:22 04:27H   1A,2A,3A,SL SMTWTFS
12675   KOVAI EXPRESS        MAS 06:10 → SA 11:02 04:52H   CC,2S    SMTWTFS
            """,
            'from_station': 'MAS',
            'to_station': 'SA',
            'date': '20250115'
        }
        
        print(f"📧 Sending test email to: {test_email}")
        print("🔗 Using Gmail MCP API only (no SMTP fallback)")
        print("📋 Email will include train search results")
        
        result = send_railway_email_mcp(test_email, train_data)
        
        print("\n" + "=" * 60)
        if result.get("status") == "success":
            print("✅ Gmail MCP API test PASSED!")
            print(f"📧 Email sent successfully to {test_email}")
            print("📊 Gmail API Response:")
            print(result.get("gmail_response", "No response details"))
        else:
            print("❌ Gmail MCP API test FAILED!")
            print(f"Error: {result.get('message', 'Unknown error')}")
            print("\n🔧 This is expected if:")
            print("1. Network connectivity issues")
            print("2. Gmail MCP API endpoint changes")
            print("3. API rate limiting")
        
        print("\n📋 Test Details:")
        print(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    test_mcp_only()
