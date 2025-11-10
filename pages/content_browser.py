"""Content browser and search page for AI Learning Repository."""
import streamlit as st
from simple_vector_store import SimpleVectorStore as MilvusVectorStore
from typing import List
from langchain.docstore.document import Document

# Pre-defined categories
CATEGORIES = [
    "All Categories",
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

def get_unique_values_from_store(store: MilvusVectorStore, field: str) -> List[str]:
    """Get unique values for a metadata field from the store."""
    # This is a simplified version - in production, you'd query Milvus directly
    # For now, we'll return empty list and let user filter manually
    return []

def main():
    st.title("🔍 Content Browser")
    st.markdown("Browse and search your AI learning repository")
    
    # Search interface
    search_query = st.text_input(
        "🔎 Search",
        placeholder="Search for topics, concepts, or keywords..."
    )
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            options=CATEGORIES
        )
    
    with col2:
        filter_type = st.selectbox(
            "Filter by Type",
            options=["All Types", "url", "note", "document", "video", "audio"]
        )
    
    with col3:
        num_results = st.slider(
            "Number of Results",
            min_value=5,
            max_value=50,
            value=10
        )
    
    # Search button
    if st.button("🔍 Search", type="primary") or search_query:
        if not search_query:
            st.warning("Please enter a search query")
        else:
            with st.spinner("Searching..."):
                try:
                    vector_store = MilvusVectorStore(store_path="./vector_store_personal_assistant")
                    
                    # Perform search
                    results = vector_store.similarity_search(search_query, k=num_results)
                    
                    if not results:
                        st.info("No results found. Try a different search query.")
                    else:
                        st.subheader(f"📚 Found {len(results)} results")
                        
                        # Filter results if filters are set
                        filtered_results = results
                        if filter_category != "All Categories":
                            filtered_results = [
                                r for r in results 
                                if r.metadata.get('category', '').lower() == filter_category.lower()
                            ]
                        
                        if filter_type != "All Types":
                            filtered_results = [
                                r for r in filtered_results
                                if r.metadata.get('type', '').lower() == filter_type.lower()
                            ]
                        
                        if not filtered_results:
                            st.info("No results match your filters. Try adjusting them.")
                        else:
                            # Display results
                            for i, doc in enumerate(filtered_results, 1):
                                with st.container():
                                    # Header with metadata
                                    metadata = doc.metadata
                                    
                                    col_title, col_meta = st.columns([3, 1])
                                    
                                    with col_title:
                                        title = metadata.get('title', f'Result {i}')
                                        st.markdown(f"### {i}. {title}")
                                    
                                    with col_meta:
                                        content_type = metadata.get('type', 'unknown')
                                        category = metadata.get('category', 'N/A')
                                        st.caption(f"Type: {content_type} | Category: {category}")
                                    
                                    # Source URL if available
                                    source_url = metadata.get('source_url')
                                    if source_url:
                                        st.markdown(f"🔗 [Source]({source_url})")
                                    
                                    # Tags
                                    tags = metadata.get('tags', '')
                                    if tags:
                                        tag_list = [tag.strip() for tag in tags.split(',')]
                                        tag_display = ' '.join([f"`{tag}`" for tag in tag_list[:5]])
                                        st.markdown(f"Tags: {tag_display}")
                                    
                                    # Content preview
                                    with st.expander(f"View content ({len(doc.page_content)} chars)"):
                                        st.markdown(doc.page_content[:2000] + ("..." if len(doc.page_content) > 2000 else ""))
                                    
                                    # Additional metadata
                                    if metadata.get('added_date'):
                                        st.caption(f"Added: {metadata.get('added_date', '')[:10]}")
                                    
                                    if metadata.get('learning_path'):
                                        st.caption(f"Learning Path: {metadata.get('learning_path')}")
                                    
                                    st.markdown("---")
                
                except Exception as e:
                    st.error(f"Error searching: {e}")
                    st.exception(e)
    
    # Browse by category (without search)
    st.markdown("---")
    st.subheader("📂 Browse by Category")
    
    browse_category = st.selectbox(
        "Select a category to browse",
        options=[c for c in CATEGORIES if c != "All Categories"]
    )
    
    if st.button("Browse Category"):
        with st.spinner(f"Loading content from {browse_category}..."):
            try:
                # Use a generic query to get results, then filter
                vector_store = MilvusVectorStore(store_path="./vector_store_personal_assistant")
                
                # Get some results with a generic query
                results = vector_store.similarity_search(browse_category.lower(), k=20)
                
                # Filter by category
                category_results = [
                    r for r in results
                    if r.metadata.get('category', '').lower() == browse_category.lower()
                ]
                
                if category_results:
                    st.success(f"Found {len(category_results)} items in {browse_category}")
                    
                    for i, doc in enumerate(category_results, 1):
                        metadata = doc.metadata
                        title = metadata.get('title', f'Item {i}')
                        source_url = metadata.get('source_url', '')
                        
                        st.markdown(f"**{i}. {title}**")
                        if source_url:
                            st.markdown(f"🔗 [Link]({source_url})")
                        st.caption(f"Type: {metadata.get('type', 'unknown')}")
                        st.markdown("---")
                else:
                    st.info(f"No content found in {browse_category} category")
            
            except Exception as e:
                st.error(f"Error browsing: {e}")


if __name__ == "__main__":
    main()

