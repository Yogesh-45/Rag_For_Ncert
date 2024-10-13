# Rag_For_Ncert
Rag_For_Ncert is a Retrieval-Augmented Generation (RAG) application designed to assist users with queries related to the NCERT Sound topic. The application offers two primary endpoints:

**/rag:** Provides RAG-based textual answers to user queries about sound.  
**/rag_agent:** Delivers both text and voice responses to user queries using Large Language Model (LLM) agents.


# Table of Contents
Installation
Configuration
Running the Application
Integration Details


# Installation
Follow these steps to clone the repository and set up the development environment.

1. Clone the Repository  
git clone https://github.com/Yogesh-45/Rag_For_Ncert.git  
cd Rag_For_Ncert  
2. Create a Virtual Environment  
It's recommended to use a virtual environment to manage project dependencies.  
3. Install Dependencies  
pip install -r requirements.txt


# Configuration
Create a .env File &  add API Keys to .env. The application requires API keys for OpenAI, Sarvam, and Weaviate.
Replace the placeholder text with your actual API keys:

**OPENAI_API_KEY=**   your_openai_api_key  
**SARVAM_API_KEY=**   your_sarvam_api_key  
**WEAVIATE_API_KEY=** your_weaviate_api_key


# Running the Application
Once the setup is complete, you can run the application using the following command:  
**python main.py**  
This command will start the FastAPI server and the Gradio interface. By default, the application will be accessible at http://127.0.0.1:7860/.


# Integration Details
The Rag_For_Ncert application integrates several powerful libraries and frameworks to deliver its functionality:

**LangChain:** Manages the retrieval and language models, facilitating the RAG process.  
**FastAPI:** Serves as the web framework to handle API requests and responses efficiently.  
**Gradio:** Provides an interactive user interface for testing and demonstrating the application's capabilities.  
Additional Libraries:  
**OpenAI:** Interfaces with OpenAI's GPT models for generating responses.  
**Weaviate:** Serves as the vector database for document retrieval.  
**Sarvam:** Provides Text-To-Speech (TTS) models
