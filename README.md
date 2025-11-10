# AI Learning Repository

A comprehensive RAG-based learning repository for managing AI/ML learning materials, notes, and resources. Build your personal knowledge base with URLs, notes, documents, and multimedia content, then search and discover content using AI-powered semantic search.

## Features

- 📚 **Bulk URL Import**: Import multiple URLs at once with automatic metadata extraction
- 📝 **Notes Management**: Create and manage learning notes with markdown support
- 🔍 **Smart Search**: AI-powered semantic search across all your content
- 📂 **Content Organization**: Categorize and tag content for easy discovery
- 📄 **Document Support**: PDF, Word, Excel, and text documents
- 🎥 **Multimedia**: Audio and video transcription support
- 🏷️ **Categorization**: Pre-defined categories for AI/ML topics
- 🔗 **Learning Paths**: Organize content into learning paths
- 👤 **Per-User Storage**: Each user has their own isolated vector database
- 🔐 **Authentication**: Secure access with user authentication

## Quick Start

### Run Locally

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Pages

- **Main App** (`app.py`): Search and query your knowledge base
- **Bulk Import** (`pages/bulk_import.py`): Import multiple URLs at once
- **Notes Manager** (`pages/notes_manager.py`): Create and manage notes
- **Content Browser** (`pages/content_browser.py`): Browse and filter content
- **Admin** (`pages/app_admin.py`): Manage documents, PDFs, audio, video

## Tech Stack

- **Web Framework**: [Streamlit](https://streamlit.io/)
- **Vector Store**: Milvus (local or cloud)
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: OpenAI text-embedding-3-large
- **Framework**: LangChain for RAG, memory, and reasoning
- **Document Processing**: PyPDF2, python-docx
- **Audio/Video**: AssemblyAI, MoviePy

## Usage

### Adding URLs

1. Navigate to **Bulk Import** page
2. Choose input method (paste URLs, CSV file, or text file)
3. Select category and tags
4. Click "Import URLs"

### Adding Notes

1. Navigate to **Notes Manager** page
2. Choose a template (optional)
3. Fill in title, category, tags, and content
4. Save your note

### Searching Content

1. Use the main search interface or Content Browser
2. Enter your query
3. Filter by category, type, or tags
4. Browse results with metadata

## Design

See [DESIGN.md](DESIGN.md) for detailed architecture and design documentation.

## Requirements

See `requirements.txt` for all dependencies.

## Configuration

Set up your secrets in `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "your-google-api-key"
GENAI_API_KEY = "your-genai-api-key"
ASSEMBLYAI_API_KEY = "your-assemblyai-api-key"
NVIDIA_API_KEY = "your-nvidia-api-key"  # Optional
```

## License

See LICENSE file for details.