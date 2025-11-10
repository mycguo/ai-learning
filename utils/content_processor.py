"""Utilities for processing content for the learning repository."""
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import WebBaseLoader
from utils.metadata_extractor import create_metadata


def process_urls_for_ingestion(
    urls: List[str],
    default_category: Optional[str] = None,
    default_tags: Optional[List[str]] = None,
    learning_path: Optional[str] = None
) -> List[Document]:
    """Process a list of URLs and convert them to Documents with metadata.
    
    Args:
        urls: List of URLs to process
        default_category: Default category to apply to all URLs
        default_tags: Default tags to apply to all URLs
        learning_path: Optional learning path identifier
    
    Returns:
        List of Document objects ready for vector store ingestion
    """
    documents = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive"
    }
    
    loader = WebBaseLoader(
        web_path=urls,
        header_template=headers,
        continue_on_failure=True,
        show_progress=False
    )
    
    try:
        loaded_docs = loader.load()
        
        for doc in loaded_docs:
            url = doc.metadata.get('source', '')
            metadata = create_metadata(
                url=url,
                title=doc.metadata.get('title'),
                content=doc.page_content,
                category=default_category,
                tags=default_tags,
                content_type="url",
                learning_path=learning_path
            )
            
            # Create new document with enriched metadata
            documents.append(Document(
                page_content=doc.page_content,
                metadata=metadata
            ))
    except Exception as e:
        print(f"Error processing URLs: {e}")
    
    return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 5000,
    chunk_overlap: int = 1000
) -> List[Document]:
    """Split documents into chunks while preserving metadata.
    
    Args:
        documents: List of documents to chunk
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
    
    Returns:
        List of chunked documents
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunked_docs = []
    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        
        for chunk in chunks:
            # Preserve original metadata for each chunk
            chunked_docs.append(Document(
                page_content=chunk,
                metadata=doc.metadata.copy()
            ))
    
    return chunked_docs


def process_note_for_ingestion(
    note_content: str,
    title: str,
    category: Optional[str] = None,
    tags: Optional[List[str]] = None,
    learning_path: Optional[str] = None,
    linked_url: Optional[str] = None
) -> List[Document]:
    """Process a note and convert it to Documents.
    
    Args:
        note_content: The note text content
        title: Title of the note
        category: Category for the note
        tags: Tags for the note
        learning_path: Optional learning path
        linked_url: Optional URL this note is linked to
    
    Returns:
        List of Document objects (may be chunked)
    """
    metadata = create_metadata(
        url=linked_url,
        title=title,
        content=note_content,
        category=category,
        tags=tags,
        content_type="note",
        learning_path=learning_path
    )
    
    # Add note-specific metadata
    metadata['note_content'] = note_content
    
    doc = Document(page_content=note_content, metadata=metadata)
    
    # Chunk if note is long
    if len(note_content) > 5000:
        return chunk_documents([doc])
    else:
        return [doc]

