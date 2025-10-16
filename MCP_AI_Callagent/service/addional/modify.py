from service.elevenlap import text_to_speech
from service.twilio_service import send_sms, make_call
import streamlit as st

def add_communication_options(result):
    """Add communication options to the app"""
    # Optional communication method
    st.subheader("Want to receive this as voice or SMS?")
    contact_method = st.radio("Choose Method:", ["None", "SMS", "Voice Call"])
    recipient_phone = st.text_input("Recipient Phone (+91...)", max_chars=15)

    if contact_method != "None" and recipient_phone and result and "messages" in result:
        combined_text = "\n".join(msg.content for msg in result["messages"])
        
        # Check if API keys are configured
        if contact_method == "SMS":
            if st.button("Send as SMS"):
                try:
                    from service.twilio_service import TWILIO_SID, TWILIO_AUTH_TOKEN
                    if TWILIO_SID == "your_twilio_sid" or TWILIO_AUTH_TOKEN == "your_twilio_auth_token":
                        st.error("Please configure your Twilio credentials in environment variables or service file.")
                        return
                    sms_sid = send_sms(recipient_phone, combined_text)
                    st.success(f"SMS sent! SID: {sms_sid}")
                except Exception as e:
                    st.error(f"Failed to send SMS: {str(e)}")

        elif contact_method == "Voice Call":
            if st.button("Send as Voice Call"):
                try:
                    from service.elevenlap import ELEVENLABS_API_KEY
                    if ELEVENLABS_API_KEY == "your_elevenlabs_api_key_here":
                        st.error("Please configure your ElevenLabs API key in environment variables or service file.")
                        return
                    audio_file = text_to_speech(combined_text)
                    # Note: you must upload this audio file to a public URL
                    public_audio_url = "https://yourdomain.com/output.mp3"
                    call_sid = make_call(recipient_phone, public_audio_url)
                    st.success(f"Call initiated! SID: {call_sid}")
                except Exception as e:
                    st.error(f"Failed to make call: {str(e)}")
