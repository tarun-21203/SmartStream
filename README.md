# Smart Stream - AI-Powered YouTube Video Analysis

## Introduction
Smart Stream is an innovative AI-powered application that transforms how users consume YouTube video content. Instead of watching entire videos, users can quickly get comprehensive summaries and interact with video content through an intelligent chat interface. This saves valuable time while ensuring users don't miss important information.

## Background
With video content consumption at an all-time high, users face information overload and time constraints. Smart Stream bridges this gap by converting video content into digestible summaries and enabling interactive Q&A sessions. Users can quickly understand video content and dive deeper into specific topics through natural language conversations.

## Key Features
- **🎯 Smart Transcript Extraction** - Reliable extraction from YouTube videos using yt-dlp
- **🤖 AI-Powered Summaries** - Intelligent summarization using Groq's LLM technology
- **💬 Interactive Chat Bot** - Ask questions about video content and get instant answers
- **📊 Handles Large Videos** - Smart chunking for long transcripts with comprehensive summaries

## Implementation

### 1. Transcript Extraction
We use **yt-dlp** with advanced anti-bot detection measures to reliably extract transcripts from YouTube videos. The system includes:
- Multiple language support (en, en-US, en-GB, en-CA)
- Android client emulation to bypass restrictions
- Automatic cleanup of temporary files
- Robust error handling and fallback mechanisms

### 2. AI-Powered Summarization
Using **Groq's LLaMA 3.1 8B model**, we create intelligent summaries:
- **Small videos**: Direct AI summarization with comprehensive 8-10 line summaries
- **Large videos**: Chunked processing with individual summaries combined into coherent overviews
- **Smart fallbacks**: Multiple levels of fallback for different scenarios

### 3. Interactive Q&A System
Built with **LangChain** and **FAISS** vector database:
- RAG (Retrieval-Augmented Generation) for accurate answers
- Real-time chat interface with conversation history
- Context-aware responses based on video content
- Graceful handling of API rate limits

### 4. User Experience
**Streamlit-powered** frontend with professional UX:
- Clean, intuitive interface
- Real-time processing feedback
- Mobile-responsive design

## Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### Running the Application

#### 1. Start the Flask API Server
```bash
python run.py
```
The API server will start on `http://127.0.0.1:5000`

#### 2. Launch the Web Frontend
```bash
streamlit run frontend.py
```
The web application will open in your browser at `http://localhost:8501`

### Usage
1. **Enter YouTube URL** in the sidebar
2. **Click "Fetch Video"** to get AI-generated summary
3. **Ask questions** in the chat interface about the video content
4. **Switch videos** - chat history automatically clears for new videos

## Tech Stack

### Backend
- **Flask** - REST API server
- **yt-dlp** - YouTube transcript extraction with anti-bot measures
- **LangChain** - AI orchestration and RAG implementation
- **FAISS** - Vector database for semantic search
- **Groq** - LLaMA 3.1 8B model for AI processing

### Frontend
- **Streamlit** - Interactive web interface
- **Real-time chat** - Seamless Q&A experience

### AI & ML
- **Groq LLaMA 3.1 8B** - Text summarization and question answering
- **Google Generative AI Embeddings** - Text vectorization for semantic search
- **RAG Architecture** - Retrieval-Augmented Generation for accurate responses

## Architecture
```
YouTube URL → yt-dlp → Transcript → Groq AI → Summary
                                      ↓
User Questions → LangChain + FAISS → Groq AI → Answers
```

## Project Structure
```
Smart Stream/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── transcribe.py        # YouTube transcript extraction
│   ├── query.py            # AI processing and Q&A
│   └── routes.py           # API endpoints
├── frontend.py             # Streamlit web interface
├── run.py                  # Flask server startup
├── requirements.txt        # Python dependencies
├── .env                    # API keys (create this)
└── README.md              # This file
```

## Contributing
This application demonstrates the power of combining modern AI technologies to create practical, user-friendly tools for content consumption. The clean, production-ready codebase serves as an excellent foundation for further enhancements.

---

**Smart Stream** - Transforming video consumption through AI-powered intelligence. Save time, stay informed, and interact with content like never before! 🚀