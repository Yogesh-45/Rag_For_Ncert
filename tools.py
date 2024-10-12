import os
from dotenv import load_dotenv


import weaviate
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
import json

import requests
from pydub import AudioSegment
import io
import simpleaudio as sa
import base64
import threading
import logging
from functools import partial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv(dotenv_path='D:/yogi/LLM/sarvam/llm_app/backend/.env')
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
WEAVIATE_API_KEY= os.getenv("WEAVIATE_API_KEY")
SARVAM_API_KEY= os.getenv("SARVAM_API_KEY")


WEAVIATE_URL = 'https://npoxyaaxr5k1km0njkybta.c0.asia-southeast1.gcp.weaviate.cloud'

client = weaviate.Client(
    url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY)
)


# embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
# embedding_model = HuggingFaceEmbeddings( model_name=embedding_model_name,)
embedding_model = OpenAIEmbeddings(api_key= OPENAI_API_KEY)


loader = PyPDFLoader("D:/yogi/LLM/sarvam/iesc111.pdf")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs = text_splitter.split_documents(pages)
vector_db = Weaviate.from_documents(docs, embedding_model, client=client, by_text=False)



@tool
def call_vectordb(query):
    """Function that calls vector database and returns most semantically similar output to the input query"""
    retriever = vector_db.as_retriever()
    retrieved_documents= retriever.get_relevant_documents(query)

    # Convert documents to a JSON-serializable format
    retrieved_chunk = [
        {
            "content": doc.page_content,  # or doc.text in some cases
            "metadata": doc.metadata  # You can include metadata if necessary
        }
        for doc in retrieved_documents
    ]

    return json.dumps({"retrived_chunk": retrieved_chunk})


def play_audio(audio_data):
    """
    Function to play audio data in a separate thread.
    """
    try:
        audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
        play_obj = sa.play_buffer(
            audio_segment.raw_data,
            num_channels=audio_segment.channels,
            bytes_per_sample=audio_segment.sample_width,
            sample_rate=audio_segment.frame_rate
        )
        play_obj.wait_done()  # Wait until playback is finished
    except Exception as e:
        logger.error(f"An error occurred during audio playback: {e}")


@tool
def voice_agent(text):

    """Function that converts text to speech"""

    url = "https://api.sarvam.ai/text-to-speech"


    # text = [text]

    print(f'text for conversion: {text}')
    print(f'text type for conversion: {type(text)}')


    payload = {
        "inputs": [text],
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

    if not audios:
        # print("No audio data found in the response.")
        logger.warning("No audio data found in the response.")
        return text
    


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
            # play_obj.wait_done()               # Wait for the audio to finish playing

        except Exception as e:
            print(f"An error occurred while streaming the audio: {e}")
        

        print(f"text inside tool: {text}")
        return text
        
    except Exception as e:
        print(f"An error occurred while processing the audio: {e}")
        return text  # Return text even if an error occurs