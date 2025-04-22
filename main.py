from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import gradio as gr
import uvicorn
import os
from dotenv import load_dotenv

from generate_llm_response import generate_llm_response
from voice_agent import VoiceAgent

load_dotenv(dotenv_path='D:/yogi/LLM/sarvam/llm_app/rag_for_ncert/.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: Optional[str] = None

@app.post("/api/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    try:
        response = generate_llm_response(request.query)
        return QueryResponse(response=response['output'])
    except Exception as e:
        return QueryResponse(response=str(e))


def gradio_wrapper(user_input, history):
    # Convert chat history into format required by LangChain
    chat_history = []
    for human, ai in history:
        chat_history.append({"type": "human", "content": human})
        chat_history.append({"type": "ai", "content": ai})

    response = generate_llm_response(user_input, chat_history)
    audio_path = VoiceAgent(response) or ""
    updated_history = history + [[user_input, response["output"]]]
    return updated_history, audio_path

with gr.Blocks() as demo:
    gr.Markdown("### 🎧 NCERT RAG with Conversational Audio Responses")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask a question or follow up...", show_label=False)
    audio_output = gr.Audio(label="🔊 Listen", type="filepath")

    msg.submit(gradio_wrapper, [msg, chatbot], [chatbot, audio_output])
    gr.ClearButton([msg, chatbot, audio_output])

app = gr.mount_gradio_app(app, demo, path="/rag_agent")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7860, reload=True)