from twilio.rest import Client

try:
    from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER
except Exception:
    TWILIO_ACCOUNT_SID = ""
    TWILIO_AUTH_TOKEN = ""
    TWILIO_FROM_NUMBER = ""

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None

def send_sms(to_number: str, message: str) -> dict:
    try:
        if not client or not TWILIO_FROM_NUMBER:
            return {"status": "error", "message": "Twilio not configured"}
        sms = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_number
        )
        return {"status": "success", "sid": sms.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def make_call(to_number: str, audio_url: str) -> dict:
    try:
        if not client or not TWILIO_FROM_NUMBER:
            return {"status": "error", "message": "Twilio not configured"}
        call = client.calls.create(
            twiml=f'<Response><Play>{audio_url}</Play></Response>',
            from_=TWILIO_FROM_NUMBER,
            to=to_number
        )
        return {"status": "success", "sid": call.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}
