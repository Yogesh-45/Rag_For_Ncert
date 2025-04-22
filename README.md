# 🎧 Rag_For_Ncert

**Rag_For_Ncert** is a **Retrieval-Augmented Generation (RAG)** based intelligent assistant built to answer queries from the **"Sound" chapter** of the NCERT Class 12 Physics textbook.

It intelligently integrates **vector database search** and **Large Language Models (LLMs)** to provide:
- 📄 Text-based responses
- 🔊 Voice responses

### 🎯 Key Functionality:
- If the query **relates to the Sound chapter**, the LLM first searches the vector database for accurate content and then responds.
- If the query is **not related to Sound**, the LLM responds directly without retrieval.

---

## 📁 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Integration Details](#-integration-details)
- [API Endpoint](#-api-endpoint)
- [Demo & Screenshots (optional)](#-demo--screenshots-optional)
- [License](#-license)

---

## 🌟 Features

- ✅ RAG-based question answering for NCERT physics (Sound)
- 🔎 Integrates OpenAI GPT for reasoning and answer generation
- 🧠 Uses **Weaviate** as a vector store for retrieval
- 🗣️ Converts text answers to **voice** using Sarvam TTS
- 🌐 FastAPI backend + Gradio interface for interactive use
- 🧪 `/rag_agent` endpoint for flexible querying via API

---

## 🚀 Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Yogesh-45/Rag_For_Ncert.git
cd Rag_For_Ncert
```

### 2. Set Up a Virtual Environment
It's recommended to use venv or conda to manage dependencies.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### ⚙️ Configuration
Before running the app, create a .env file in the project root and insert your API keys like so:
```
OPENAI_API_KEY=your_openai_api_key
SARVAM_API_KEY=your_sarvam_api_key
WEAVIATE_API_KEY=your_weaviate_api_key
```
✅ Tip: Do not share or commit your .env file to version control.

### 🏃 Running the Application
To launch the FastAPI server and Gradio interface:
```
python main.py
```

By default, the application will be live at:
http://127.0.0.1:7860/rag_agent

### 🧩 Integration Details

🔗 **Frameworks & Tools Used:**

| Component     | Purpose                                         |
|---------------|-------------------------------------------------|
| **LangChain** | Orchestrates retrieval + LLM responses          |
| **OpenAI**    | Generates high-quality answers                  |
| **Weaviate**  | Stores and retrieves embedded text data         |
| **Sarvam TTS**| Converts responses to speech                    |
| **FastAPI**   | Powers the backend API                          |
| **Gradio**    | Provides an interactive front-end               |



### 🙌 Contributing
Feel free to fork the repo, raise issues, or submit PRs to help improve the tool!

### ✨ Acknowledgements
OpenAI

LangChain

Weaviate

Sarvam AI
