import requests
import os

ELEVENLABS_API_KEY = os.getenv("sk_2edc0358e3702c75f32c22ea25bb2cb5aed0a70f4b7795ac", "your_elevenlabs_api_key_here")
VOICE_ID = os.getenv("KFNvimmuOIRv7m64kCwe", "Rachel")  # or another supported voice

def text_to_speech(text, filename="output.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        raise Exception(f"ElevenLabs error: {response.text}")
