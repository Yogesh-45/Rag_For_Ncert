import base64
import io
import os
import requests
import textwrap
from dotenv import load_dotenv
from pydub import AudioSegment
import uuid

load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def VoiceAgent(text):
    if isinstance(text, dict) and "output" in text:
        input_text = text["output"]
    elif isinstance(text, str):
        input_text = text
    else:
        print("Unsupported input type.")
        return None

    input_chunks = textwrap.wrap(input_text, width=500)

    payload = {
        "inputs": input_chunks,
        "target_language_code": "en-IN",
        "speaker": "meera",
        "pitch": 0,
        "pace": 1.65,
        "loudness": 2,
        "speech_sample_rate": 16000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    headers = {
        "Content-Type": "application/json",
        "API-Subscription-Key": SARVAM_API_KEY
    }

    response = requests.post("https://api.sarvam.ai/text-to-speech", json=payload, headers=headers)

    try:
        data = response.json()
        audios = data.get("audios", [])
        if not audios:
            return None
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None

    combined_audio = AudioSegment.empty()
    for audio_base64 in audios:
        audio_data = base64.b64decode(audio_base64)
        audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
        combined_audio += audio_segment

    file_name = f"output_{uuid.uuid4().hex[:8]}.wav"
    file_path = os.path.join("temp_audio", file_name)
    os.makedirs("temp_audio", exist_ok=True)
    with open(file_path, "wb") as f:
        combined_audio.export(f, format="wav")

    return file_path