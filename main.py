from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import gradio as gr
import uvicorn


import sys
from generate_llm_response import generate_llm_response
from rag import RAG

import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='D:/yogi/LLM/sarvam/llm_app/backend/.env')
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
SARVAM_API_KEY= os.getenv("SARVAM_API_KEY")


app = FastAPI()

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for request and response

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: Optional[str] = None

# @app.post("/", response_model=QueryResponse)
@app.post("/api/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    try:
        query = request.query
        print(query)

        text_response= generate_llm_response(query)

        print(f'kya me yha tak aaya hu')

        # return # Assuming your QueryResponse expects 'input' and 'output' fields
        return QueryResponse(text_response['input'], text_response['output'])
    
    except Exception as e:
        return QueryResponse(error=str(e))
    



demo= gr.ChatInterface(
    fn= RAG,
    textbox= gr.Textbox(placeholder= "Ask me anything..."),
    title= 'NCERT GUIDE FOR SOUND',
    undo_btn= "Delete Previous",
    clear_btn= "Clear"
)

demo2= gr.ChatInterface(
    fn= generate_llm_response,
    textbox= gr.Textbox(placeholder= "Ask me anything..."),
    title= 'NCERT GUIDE FOR SOUND',
    undo_btn= "Delete Previous",
    clear_btn= "Clear"
)

app= gr.mount_gradio_app(app, demo, path="/rag")

app= gr.mount_gradio_app(app, demo2, path="/rag_agent")


if __name__ == "__main__":
    uvicorn.run(
        app= "main:app",
        host= '127.0.0.1',
        port= 7860,
        reload= True
    )

