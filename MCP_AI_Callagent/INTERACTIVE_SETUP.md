# 🗣️ Interactive Voice Agent Setup Guide

## 🎯 **What You Have Now**

✅ **Working Features:**
- Basic voice calls with pre-recorded messages
- Interactive call demonstrations
- Voice integration with ElevenLabs and Twilio
- Streamlit web interface

## 🚀 **How to Enable Full Interactive Calls**

### **Step 1: Start the Webhook Server**

```bash
# Install additional dependencies
pip install flask twilio requests

# Start the webhook server
python webhook_server.py
```

The server will run on: `http://localhost:5000`

### **Step 2: Configure Twilio Webhook**

1. Go to your [Twilio Console](https://console.twilio.com/)
2. Navigate to Phone Numbers → Manage → Active numbers
3. Click on your Twilio phone number
4. In the "Voice Configuration" section:
   - Set "Webhook" to: `http://your-public-url:5000/handle_speech`
   - Set HTTP method to: `POST`

### **Step 3: Make Your Server Public**

For Twilio to reach your webhook, you need a public URL. Options:

**Option A: ngrok (Recommended for testing)**
```bash
# Install ngrok
# Download from: https://ngrok.com/

# Expose your local server
ngrok http 5000

# Use the ngrok URL in Twilio webhook
# Example: https://abc123.ngrok.io/handle_speech
```

**Option B: Deploy to Cloud**
- Deploy to Heroku, Railway, or similar
- Use the deployed URL in Twilio webhook

### **Step 4: Test Full Interactivity**

1. Start the webhook server: `python webhook_server.py`
2. Open your Streamlit app: `streamlit run app.py`
3. Go to "🤖 Railway Voice Agent" tab
4. Click "🗣️ Interactive Call"
5. Ask questions like:
   - "What trains are available from Delhi to Mumbai?"
   - "Check the status of train 12617"
   - "Book a ticket from Chennai to Bangalore"

## 🔧 **How Interactive Calls Work**

### **Flow:**
1. User receives call from AI agent
2. Agent asks user to speak their question
3. User speaks their railway query
4. Speech is converted to text by Twilio
5. Text is sent to your webhook server
6. AI processes the question and generates response
7. Response is converted to speech and played back
8. Process repeats for follow-up questions

### **Supported Queries:**
- **Train Search**: "Find trains from Delhi to Mumbai"
- **Booking**: "Book a ticket for tomorrow"
- **Status**: "Check train 12617 status"
- **Fares**: "What's the fare for AC 2 tier?"
- **General**: "Help me with railway information"

## 📁 **File Structure**

```
├── app.py                          # Main Streamlit app
├── webhook_server.py               # Flask server for interactive calls
├── service/
│   ├── voice_agent.py             # Basic voice calls
│   ├── simple_interactive_agent.py # Demo interactive calls
│   └── interactive_voice_agent.py  # Full interactive functionality
├── config.py                       # API keys and configuration
└── test_interactive.py            # Test interactive calls
```

## 🧪 **Testing**

### **Test Basic Voice Calls:**
```bash
python test_voice.py
```

### **Test Interactive Calls:**
```bash
python test_interactive.py
```

### **Test Webhook Server:**
```bash
python webhook_server.py
# Then visit: http://localhost:5000
```

## 🔑 **Required API Keys**

Make sure these are configured in `config.py`:

```python
# ElevenLabs API Key
ELEVENLABS_API_KEY = "your_elevenlabs_key"

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_FROM_NUMBER = "your_twilio_number"

# Test phone number
TO_NUMBER = "your_phone_number"
```

## 🚨 **Important Notes**

1. **Trial Accounts**: Twilio trial accounts can only call verified numbers
2. **Webhook Security**: In production, add authentication to your webhook
3. **Error Handling**: The webhook server includes comprehensive error handling
4. **Speech Recognition**: Uses Twilio's enhanced speech recognition for better accuracy

## 🎉 **Success Indicators**

When everything is working:
- ✅ Webhook server shows: "Starting Interactive Voice Agent Webhook Server..."
- ✅ Twilio webhook URL is configured correctly
- ✅ Interactive calls allow two-way conversation
- ✅ AI responds appropriately to railway queries

## 🆘 **Troubleshooting**

**Call not connecting:**
- Check if phone number is verified (for trial accounts)
- Verify Twilio credentials
- Ensure sufficient account credits

**Webhook not receiving data:**
- Check webhook URL is publicly accessible
- Verify HTTP method is POST
- Check server logs for errors

**Speech not recognized:**
- Speak clearly and slowly
- Use simple, direct questions
- Check background noise levels

---

**🎯 Goal Achieved:** Users can now receive calls and have interactive conversations with the AI railway agent, asking questions and getting real-time responses!
