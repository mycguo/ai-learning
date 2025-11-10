"""Authentication utilities for AI Learning Repository."""
import streamlit as st
from typing import Callable, Optional


def require_login(page_name: str = "this page"):
    """Check if user is logged in, show login screen if not.
    
    Args:
        page_name: Name of the page for display purposes
    
    Returns:
        bool: True if user is logged in, False otherwise
    """
    if not hasattr(st, 'user'):
        # If user is not available, allow access (for local development)
        return True
    
    if not st.user.is_logged_in:
        show_login_screen(page_name)
        return False
    return True


def show_login_screen(page_name: str = "this page"):
    """Display login screen.
    
    Args:
        page_name: Name of the page for display purposes
    """
    st.header("🔐 Authentication Required")
    st.markdown(f"Please log in to access **{page_name}**.")
    st.info("This is a secure area. You need to be authenticated to use this feature.")
    
    if hasattr(st, 'login'):
        st.button("🔑 Log in with Google", on_click=st.login, type="primary")
    else:
        st.warning("Login functionality is not available. Please configure Streamlit authentication.")


def show_user_info():
    """Display current user information in the sidebar."""
    if hasattr(st, 'user') and st.user.is_logged_in:
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"👤 **{st.user.name}**")
            st.markdown(f"📧 {st.user.email if hasattr(st.user, 'email') else 'N/A'}")
            if st.button("🚪 Log out", use_container_width=True):
                if hasattr(st, 'logout'):
                    st.logout()
                st.rerun()


def protected_page(page_name: str, content_func: Callable):
    """Decorator/wrapper to protect a page with authentication.
    
    Args:
        page_name: Name of the page
        content_func: Function that renders the page content
    """
    if require_login(page_name):
        # Show user info in sidebar
        show_user_info()
        # Render the page content
        content_func()
    else:
        # Login screen is already shown by require_login
        st.stop()

