from pydub import AudioSegment
import io
import simpleaudio as sa
import base64


import requests
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='D:/yogi/LLM/sarvam/llm_app/backend/.env')
SARVAM_API_KEY= os.getenv("SARVAM_API_KEY")



def VoiceAgent(text):

    """Function that converts text to speech"""

    url = "https://api.sarvam.ai/text-to-speech"

    print(f'text for conversion: {text}')
    print(f'text type for conversion: {type(text)}')
    print(f'text output: {text['output']}')


    input_text = [text['output']]

    print(f'text for conversion: {input_text}')
    print(f'text type for conversion: {type(input_text)}')



    payload = {
        "inputs": input_text,
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "pitch": 0,
        "pace": 1.65,
        "loudness": 2,
        "speech_sample_rate": 16000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }
    headers = {"Content-Type": "application/json",
            'API-Subscription-Key': SARVAM_API_KEY}

    response = requests.request("POST", url, json=payload, headers=headers)

    data = response.json()
    audios = data.get('audios', [])

    print(f'response check of voice agent: {response}')

    if not audios:
        print("No audio data found in the response.")
        return
        # logger.warning("No audio data found in the response.")
        # return text
    


    audio_base64= audios[0]

    try:

        try:
            audio_data = base64.b64decode(audio_base64)
            audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            play_obj = sa.play_buffer(
                audio_segment.raw_data,
                num_channels=audio_segment.channels,
                bytes_per_sample=audio_segment.sample_width,
                sample_rate=audio_segment.frame_rate
            )
            return 
            # play_obj.wait_done()               # Wait for the audio to finish playing

        except Exception as e:
            print(f"An error occurred while streaming the audio: {e}")
            return
        

        # print(f"text inside tool: {text}")
        # return text
        
    except Exception as e:
        print(f"An error occurred while processing the audio: {e}")
        return
        # return text  # Return text even if an error occurs
