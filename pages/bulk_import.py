"""Bulk URL import page for AI Learning Repository."""
import streamlit as st
import pandas as pd
from typing import List
from pages.app_admin import get_vector_store, get_text_chunks
from utils.content_processor import process_urls_for_ingestion, chunk_documents
from utils.duplicate_detector import detect_duplicate_urls
from langchain.docstore.document import Document

# Pre-defined categories
CATEGORIES = [
    "AI Fundamentals",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Computer Vision",
    "Reinforcement Learning",
    "LLMs & Transformers",
    "MLOps",
    "Research Papers",
    "Tutorials & Courses",
    "Tools & Frameworks",
    "General"
]

def main():
    st.title("📚 Bulk URL Import")
    st.markdown("Import multiple URLs at once to build your AI learning repository")
    
    # Category selection
    col1, col2 = st.columns(2)
    with col1:
        default_category = st.selectbox(
            "Default Category (applied to all URLs)",
            options=CATEGORIES,
            index=len(CATEGORIES) - 1  # Default to "General"
        )
    
    with col2:
        default_tags_input = st.text_input(
            "Default Tags (comma-separated)",
            placeholder="e.g., transformers, pytorch, research"
        )
        default_tags = [tag.strip() for tag in default_tags_input.split(",")] if default_tags_input else None
    
    learning_path = st.text_input(
        "Learning Path (optional)",
        placeholder="e.g., 'LLM Fundamentals' or 'Computer Vision Basics'"
    )
    
    # Input method selection
    input_method = st.radio(
        "How would you like to add URLs?",
        ["Paste URLs", "Upload CSV File", "Upload Text File"],
        horizontal=True
    )
    
    urls = []
    
    if input_method == "Paste URLs":
        url_text = st.text_area(
            "Paste URLs (one per line)",
            height=200,
            placeholder="https://example.com/article1\nhttps://example.com/article2\n..."
        )
        if url_text:
            urls = [url.strip() for url in url_text.split("\n") if url.strip()]
    
    elif input_method == "Upload CSV File":
        csv_file = st.file_uploader("Upload CSV file", type=["csv"])
        if csv_file:
            try:
                df = pd.read_csv(csv_file)
                st.write("Preview of CSV file:")
                st.dataframe(df.head())
                
                # Try to find URL column
                url_column = st.selectbox(
                    "Select the column containing URLs",
                    options=df.columns.tolist()
                )
                
                if url_column:
                    urls = df[url_column].dropna().astype(str).tolist()
                    urls = [url.strip() for url in urls if url.strip()]
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
    
    elif input_method == "Upload Text File":
        text_file = st.file_uploader("Upload text file (one URL per line)", type=["txt"])
        if text_file:
            content = text_file.read().decode("utf-8")
            urls = [url.strip() for url in content.split("\n") if url.strip()]
    
    # Display URLs to be imported
    if urls:
        st.subheader(f"📋 Found {len(urls)} URLs")
        
        # Check for duplicates
        unique_urls, duplicates = detect_duplicate_urls(urls)
        
        if duplicates:
            st.warning(f"⚠️ Found {len(duplicates)} duplicate URLs that will be skipped")
            with st.expander("View duplicates"):
                for dup in duplicates:
                    st.text(dup)
        
        st.info(f"✅ {len(unique_urls)} unique URLs will be imported")
        
        # Preview URLs
        with st.expander("Preview URLs to import"):
            for i, url in enumerate(unique_urls[:20], 1):
                st.text(f"{i}. {url}")
            if len(unique_urls) > 20:
                st.text(f"... and {len(unique_urls) - 20} more")
        
        # Import button
        if st.button("🚀 Import URLs", type="primary"):
            if not unique_urls:
                st.error("No URLs to import")
                return
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Process URLs in batches
                batch_size = 10
                total_batches = (len(unique_urls) + batch_size - 1) // batch_size
                
                all_documents = []
                
                for batch_idx in range(total_batches):
                    batch_urls = unique_urls[batch_idx * batch_size:(batch_idx + 1) * batch_size]
                    
                    status_text.text(f"Processing batch {batch_idx + 1}/{total_batches} ({len(batch_urls)} URLs)...")
                    
                    # Process batch
                    documents = process_urls_for_ingestion(
                        batch_urls,
                        default_category=default_category if default_category != "General" else None,
                        default_tags=default_tags,
                        learning_path=learning_path if learning_path else None
                    )
                    
                    all_documents.extend(documents)
                    
                    progress_bar.progress((batch_idx + 1) / total_batches)
                
                # Chunk documents
                status_text.text("Chunking documents...")
                chunked_docs = chunk_documents(all_documents)
                
                # Add to vector store
                status_text.text("Adding to vector store...")
                vector_store = get_vector_store([doc.page_content for doc in chunked_docs])
                
                # Store metadata separately if needed
                # For now, metadata is included in the document chunks
                
                progress_bar.progress(1.0)
                status_text.text("✅ Import complete!")
                
                st.success(f"✅ Successfully imported {len(unique_urls)} URLs ({len(chunked_docs)} chunks)")
                
                # Show summary
                st.subheader("📊 Import Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("URLs Imported", len(unique_urls))
                with col2:
                    st.metric("Documents Created", len(all_documents))
                with col3:
                    st.metric("Chunks Created", len(chunked_docs))
                
            except Exception as e:
                st.error(f"Error during import: {e}")
                st.exception(e)
    
    else:
        st.info("👆 Please add URLs using one of the methods above")


if __name__ == "__main__":
    main()

