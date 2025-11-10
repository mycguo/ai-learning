"""Utilities for managing user-specific vector stores."""
import streamlit as st
import re
import os


def get_user_identifier() -> str:
    """Get a safe identifier for the current user.
    
    Returns:
        str: User identifier (username or 'default' for local dev)
    """
    if hasattr(st, 'user') and st.user.is_logged_in:
        # Use the user's name or email as identifier
        user_name = st.user.name or st.user.email
        if user_name:
            # Sanitize the username for filesystem/database use
            # Replace spaces and special chars with underscores
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', user_name.lower())
            # Remove multiple consecutive underscores
            safe_name = re.sub(r'_+', '_', safe_name)
            # Remove leading/trailing underscores
            safe_name = safe_name.strip('_')
            return safe_name
    
    # Fallback for local development or when auth is not available
    return "default"


def get_user_store_path(base_path: str = "./vector_store") -> str:
    """Get the user-specific vector store path.
    
    Args:
        base_path: Base path for vector stores
    
    Returns:
        str: User-specific store path
    """
    user_id = get_user_identifier()
    return f"{base_path}_{user_id}"


def get_user_collection_name(base_name: str = "ai_learning") -> str:
    """Get the user-specific collection name for Milvus.
    
    Args:
        base_name: Base collection name
    
    Returns:
        str: User-specific collection name
    """
    user_id = get_user_identifier()
    # Milvus collection names have restrictions, so we sanitize
    safe_user_id = re.sub(r'[^a-zA-Z0-9_]', '_', user_id)
    safe_user_id = re.sub(r'_+', '_', safe_user_id).strip('_')
    return f"{base_name}_{safe_user_id}"


def get_current_user_name() -> str:
    """Get the display name of the current user.
    
    Returns:
        str: User's display name or 'Guest'
    """
    if hasattr(st, 'user') and st.user.is_logged_in:
        return st.user.name or st.user.email or "User"
    return "Guest"

