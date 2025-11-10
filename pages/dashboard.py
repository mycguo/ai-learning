"""Dashboard page showing statistics and overview of AI Learning Repository."""
import streamlit as st
from simple_vector_store import SimpleVectorStore as MilvusVectorStore
import pandas as pd
from utils.auth import require_login, show_user_info
from utils.user_store import get_user_store_path, get_current_user_name

def main():
    # Check authentication
    if not require_login("Dashboard"):
        return
    
    # Show user info in sidebar
    show_user_info()
    
    st.title("📊 Dashboard")
    user_name = get_current_user_name()
    st.markdown(f"Overview of **{user_name}'s** AI Learning Repository")
    
    try:
        # Use user-specific vector store
        user_store_path = get_user_store_path("./vector_store")
        vector_store = MilvusVectorStore(store_path=user_store_path)
        stats = vector_store.get_collection_stats()
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", stats.get("document_count", 0))
        
        with col2:
            st.metric("Total Vectors", stats.get("vector_count", 0))
        
        with col3:
            st.metric("Store Status", stats.get("status", "Unknown"))
        
        with col4:
            store_path = stats.get("store_path", "N/A")
            st.metric("Store Path", store_path.split("/")[-1] if "/" in store_path else store_path)
        
        st.info(f"ℹ️ This is your personal repository. Your content is stored separately from other users.")
        
        st.markdown("---")
        
        # Category distribution (placeholder - would need to query metadata)
        st.subheader("📂 Content by Category")
        st.info("Category distribution feature coming soon! This requires querying metadata from the vector store.")
        
        # Recent activity (placeholder)
        st.subheader("🕒 Recent Activity")
        st.info("Recent activity tracking coming soon!")
        
        # Quick actions
        st.markdown("---")
        st.subheader("🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Import URLs", use_container_width=True):
                st.switch_page("pages/bulk_import.py")
        
        with col2:
            if st.button("📝 Add Note", use_container_width=True):
                st.switch_page("pages/notes_manager.py")
        
        with col3:
            if st.button("🔍 Browse Content", use_container_width=True):
                st.switch_page("pages/content_browser.py")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        st.info("Make sure you have added some content to your repository first!")


if __name__ == "__main__":
    main()

