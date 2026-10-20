# 🎬 AI Video Assistant — RAG-Powered Video Understanding

An AI-powered video assistant that transforms video content into searchable knowledge. It transcribes audio, generates summaries, extracts key insights, and answers questions using **Retrieval-Augmented Generation (RAG)**.

Built with **Python, FastAPI, Streamlit, LangChain, Ollama, and Llama 3.2**, this project allows users to interact with video content through natural-language questions.

## ✨ Features

- **🎥 Video Input:** Process YouTube videos and supported local media files.
- **🎙️ Audio Processing:** Prepare audio chunks for transcription.
- **📝 Automatic Transcription:** Convert video audio into text using your configured transcription model.
- **📋 AI Summarization:** Generate concise summaries of video content.
- **🏷️ Title Generation:** Automatically generate a descriptive title.
- **✅ Action Item Extraction:** Identify tasks and follow-up actions discussed in the video.
- **🔑 Key Decision Extraction:** Extract important decisions.
- **❓ Open Question Extraction:** Identify unresolved questions.
- **💬 Interactive RAG Chat:** Ask questions and receive answers grounded in relevant transcript sections.
- **🦙 Local LLM Inference:** Use Ollama with Llama 3.2 to generate responses locally.
- **🧠 Semantic Search:** Use Ollama embeddings to retrieve relevant transcript chunks.
- **⚡ FastAPI Backend:** Expose processing functionality through REST APIs.
- **🖥️ Streamlit Interface:** Provide an interactive interface for processing videos and chatting with them.

## 🏗️ System Architecture

```text
YouTube URL / Local Media
          |
          v
    Audio Processing
          |
          v
    Audio Chunking
          |
          v
      Transcription
          |
          v
   Complete Transcript
          |
          +----------------------+
          |                      |
          v                      v
  Summarization &          Text Chunking
  Insight Extraction             |
                                 v
                         Ollama Embeddings
                                 |
                                 v
                          Vector Store
                                 |
User Question ------------------+
          |
          v
   Retriever (Top-K)
          |
          v
 Relevant Transcript Chunks
          |
          v
    Prompt + Llama 3.2
          |
          v
      Final Answer
```

## 🛠️ Tech Stack

| Technology       | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| Python           | Core application logic                             |
| FastAPI          | Backend API development                            |
| Streamlit        | Interactive user interface                         |
| LangChain        | LLM orchestration and RAG pipeline                 |
| Ollama           | Local model runtime                                |
| Llama 3.2        | Local language model for summaries and answers     |
| OllamaEmbeddings | Convert transcript chunks into vector embeddings   |
| Vector Store     | Store and retrieve semantically relevant chunks    |
| Pydantic         | Request validation and data schemas                |
| FFmpeg / Pydub   | Audio processing, depending on your implementation |
| yt-dlp           | YouTube media downloading, if configured           |
| Whisper          | Speech-to-text transcription, if configured        |

## 📂 Project Structure

```text
chat-with-video/
├── app/
│   ├── core/
│   │   ├── rag_engine.py
│   │   ├── vector_store.py
│   │   ├── transcriber.py
│   │   ├── transcript_summarizer.py
│   │   └── meetings_extractor.py
│   ├── utils/
│   │   └── media_processor.py
│   ├── api/
│   │   └── routes/
│   └── schemas/
├── storages/
├── streamlit_app.py
├── main.py
├── pipeline.py
├── test_pipeline.py
├── requirements.txt
└── README.md
```

*The structure above is illustrative; adjust it to match the files in your repository.*

## ⚙️ Prerequisites

Before running the project, install:

- Python 3.10 or a compatible version supported by your dependencies
- [Ollama](https://ollama.com/)
- FFmpeg, if required by your media-processing pipeline
- Git

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/milanrai14/ai-video-assistant-fastapi.git
cd ai-video-assistant-fastapi
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you do not yet have a `requirements.txt`, generate one from your working virtual environment:

```bash
pip freeze > requirements.txt
```

### 4. Download the Ollama language model

Make sure Ollama is installed and running, then execute:

```bash
ollama pull llama3.2
```

Verify that the model is available:

```bash
ollama list
```

### 5. Download the embedding model

```bash
ollama pull nomic-embed-text
```

Configure your embedding model in the vector-store module:

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)
```

Use the same embedding model when creating and loading the vector store.

## 🧠 RAG Configuration

The RAG pipeline uses a retriever to identify transcript chunks relevant to the user's question.

Example configuration:

```python
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="llama3.2",
    temperature=0.3,
)

output_parser = StrOutputParser()
```

The application retrieves relevant chunks and supplies them as context to the language model.

Note that prompt instructions reduce unsupported answers but cannot guarantee that the model will never hallucinate.

## ▶️ Running the Application

### Start the FastAPI backend

From the project root:

```bash
uvicorn main:app --reload
```

Open the interactive API documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Start the Streamlit interface

Open another terminal, activate the same virtual environment, and run:

```bash
streamlit run streamlit_app.py
```

Open the local URL displayed by Streamlit, usually:

[http://localhost:8501](http://localhost:8501)

The Streamlit interface can process videos, display summaries and extracted insights, and provide a chat interface for transcript-based questions.

**Note:** If Streamlit directly calls your Python pipeline, the interface can run independently of FastAPI. If you configure Streamlit to send HTTP requests to FastAPI, start both applications.

## 💬 Example Usage

1. Open the Streamlit application.
2. Paste a YouTube URL or enter a supported local media path.
3. Click **Process Video**.
4. Wait for audio processing and transcription to finish.
5. Review the summary, transcript, action items, key decisions, and open questions.
6. Enter a question in the chat input.

Example questions:

- What is the main topic of this video?
- What key decisions were discussed?
- What action items were mentioned?
- Explain the main concept discussed by the speaker.
- What challenges were identified?
- Did the speaker mention any unresolved questions?

Answers depend on the transcript content and the retrieved context.

## 🔐 Privacy and Limitations

- Llama 3.2 can run locally through Ollama, helping keep LLM inference on your machine.
- YouTube downloads require network access.
- Downloaded audio, transcripts, and vector-store data may remain on disk, depending on your implementation.
- Model downloads and speech-to-text model downloads require initial setup.
- Processing time depends on video duration, hardware, and model configuration.
- The application can only answer reliably when the relevant information is present in the transcript and retrieved context.
- Do not upload copyrighted or private content unless you have permission to process it.

## 🔮 Future Improvements

- Support video file uploads through the UI.
- Add timestamps and transcript citations to answers.
- Support multiple languages, including English and Hinglish.
- Add persistent conversation history.
- Improve error handling and background processing for long videos.
- Add user authentication and per-user video sessions.
- Add Docker deployment and automated tests.
- Add support for multiple local LLMs.
- Improve retrieval with reranking and configurable chunk sizes.
- Deploy the FastAPI backend and Streamlit interface.

## 🎯 Learning Objectives

This project demonstrates practical experience with:

- Building AI applications using local language models.
- Designing a Retrieval-Augmented Generation pipeline.
- Generating and retrieving semantic embeddings.
- Processing media and converting speech into text.
- Integrating LLM workflows into a user-facing application.
- Developing REST APIs with FastAPI.
- Building interactive AI interfaces with Streamlit.
- Structuring a modular Python project.

## 👨‍💻 Author

**Milan Rai**

AI & Machine Learning | Python | Generative AI | RAG

- GitHub: [milanrai14](https://github.com/milanrai14)

---

*If you find this project useful, consider giving the repository a ⭐ on GitHub.*
