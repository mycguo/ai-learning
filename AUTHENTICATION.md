# Authentication Implementation

## Overview
All pages in the AI Learning Repository now require user authentication using Streamlit's built-in authentication system. This ensures secure access to your learning content and prevents unauthorized access.

## Implementation

### Shared Authentication Module (`utils/auth.py`)

A centralized authentication module provides reusable functions:

- **`require_login(page_name)`**: Checks if user is logged in, shows login screen if not
- **`show_user_info()`**: Displays current user information in the sidebar
- **`show_login_screen(page_name)`**: Displays a user-friendly login screen

### Features

1. **Consistent Login Experience**: All pages use the same authentication flow
2. **User Information Display**: Shows logged-in user's name and email in sidebar
3. **Logout Functionality**: Easy logout button in sidebar
4. **Graceful Fallback**: Works even if authentication is not configured (for local development)

## Protected Pages

All pages now require authentication:

1. **Main App** (`app.py`) - AI Learning Repository home page
2. **Bulk Import** (`pages/bulk_import.py`) - Bulk URL import
3. **Notes Manager** (`pages/notes_manager.py`) - Notes management
4. **Content Browser** (`pages/content_browser.py`) - Content search and browsing
5. **Dashboard** (`pages/dashboard.py`) - Repository statistics
6. **Admin** (`pages/app_admin.py`) - Document management
7. **System Admin** (`pages/system_admin.py`) - System administration
8. **System Cost** (`pages/system_cost.py`) - Cost tracking

## How It Works

### Authentication Flow

1. User navigates to any page
2. `require_login()` checks authentication status
3. If not logged in:
   - Login screen is displayed
   - User clicks "Log in with Google"
   - Streamlit handles OAuth flow
4. If logged in:
   - User info is displayed in sidebar
   - Page content is rendered
   - Logout button is available

### Code Pattern

Each page follows this pattern:

```python
from utils.auth import require_login, show_user_info

def main():
    # Check authentication
    if not require_login("Page Name"):
        return
    
    # Show user info in sidebar
    show_user_info()
    
    # Page content here...
```

## Configuration

### Streamlit Authentication Setup

To enable authentication, configure Streamlit authentication in your deployment:

1. **Streamlit Cloud**: Authentication is automatically configured
2. **Self-hosted**: Configure OAuth providers in Streamlit config

### Local Development

For local development without authentication:
- The `require_login()` function gracefully handles missing authentication
- Pages will still work, but without login protection
- This allows development without authentication setup

## User Experience

### Login Screen
- Clear messaging about authentication requirement
- Single-click Google login button
- Informative UI explaining the need for authentication

### Sidebar User Info
- User's name and email displayed
- Logout button for easy session management
- Consistent across all pages

## Security Considerations

1. **Session Management**: Streamlit handles session management automatically
2. **OAuth Flow**: Uses secure OAuth 2.0 flow for authentication
3. **Access Control**: All pages are protected by default
4. **User Identification**: User information is available via `st.user`

## Future Enhancements

Potential improvements:
- Role-based access control (admin vs regular user)
- User-specific content filtering
- Multi-user support with user-specific repositories
- Session timeout configuration
- Remember me functionality

## Troubleshooting

### Authentication Not Working

1. **Check Streamlit Version**: Ensure you're using a version that supports authentication
2. **Check Configuration**: Verify OAuth is properly configured
3. **Check Secrets**: Ensure required secrets are set in Streamlit secrets

### Local Development Issues

- If authentication is not configured, pages will still work
- Use `hasattr(st, 'user')` to check if auth is available
- The auth module handles missing authentication gracefully

## Notes

- Authentication uses Streamlit's user authentication
- The `st.user` object provides user information
- All authentication is handled by Streamlit's built-in system
- No custom authentication code is required

