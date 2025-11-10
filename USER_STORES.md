# Per-User Vector Database Implementation

## Overview
The AI Learning Repository now implements per-user vector databases, ensuring complete data isolation between users. Each user has their own dedicated vector store based on their username.

## Implementation

### User Store Utilities (`utils/user_store.py`)

A centralized utility module provides functions for managing user-specific stores:

- **`get_user_identifier()`**: Gets a safe identifier for the current user
  - Uses authenticated user's name or email
  - Sanitizes for filesystem/database use
  - Falls back to "default" for local development

- **`get_user_store_path(base_path)`**: Gets user-specific vector store path
  - Returns path like `./vector_store_username`
  - Ensures each user has isolated storage

- **`get_user_collection_name(base_name)`**: Gets user-specific Milvus collection name
  - Returns collection name like `ai_learning_username`
  - Sanitizes for Milvus naming requirements

- **`get_current_user_name()`**: Gets display name of current user
  - Returns user's name or email
  - Falls back to "Guest" if not authenticated

### User Identification

The system identifies users using:
1. **Authenticated Users**: Uses `st.user.name` or `st.user.email`
2. **Local Development**: Falls back to "default" user when auth is not available
3. **Sanitization**: Usernames are sanitized to be filesystem/database safe:
   - Special characters replaced with underscores
   - Multiple underscores collapsed
   - Leading/trailing underscores removed

### Updated Components

All pages and components now use user-specific stores:

1. **Main App** (`app.py`)
   - `user_input()` function uses user-specific store
   - Search queries use user's own repository

2. **Admin Page** (`pages/app_admin.py`)
   - `_load_vector_store()` uses user-specific path
   - All document uploads go to user's store

3. **Dashboard** (`pages/dashboard.py`)
   - Shows user-specific statistics
   - Displays user's name in header
   - Shows which repository is being viewed

4. **Content Browser** (`pages/content_browser.py`)
   - Search uses user-specific store
   - Category browsing uses user's content only

5. **Bulk Import** (`pages/bulk_import.py`)
   - Uses `get_vector_store()` which is user-specific
   - URLs imported go to user's repository

6. **Notes Manager** (`pages/notes_manager.py`)
   - Uses `get_vector_store()` which is user-specific
   - Notes saved to user's repository

## Storage Structure

### File-Based Storage (SimpleVectorStore)
```
./vector_store_username/
  ├── vectors.pkl
  └── metadata.json
```

### Milvus Storage
- Collection name: `ai_learning_username`
- Each user has isolated collection
- No cross-user data access

## Benefits

1. **Data Isolation**: Complete separation between users' data
2. **Privacy**: Users can only access their own content
3. **Scalability**: Each user's data is independently manageable
4. **Security**: No risk of cross-user data leakage
5. **Multi-tenancy**: Supports multiple users on same instance

## User Experience

### For Users
- Each user sees only their own content
- Dashboard shows personalized statistics
- Search results are from user's own repository
- No interference from other users' data

### For Administrators
- Can manage user stores independently
- Easy to identify which store belongs to which user
- Can backup/restore individual user stores

## Migration Notes

### Existing Data
- Existing data in `./vector_store_personal_assistant` remains unchanged
- New users will get their own stores automatically
- Existing users can migrate their data if needed

### Local Development
- Without authentication, uses "default" user
- All local development uses `./vector_store_default`
- Can test multi-user scenarios by simulating different users

## Technical Details

### Path Generation
```python
# Example: User "John Doe" (email: john@example.com)
user_id = "john_doe"  # Sanitized from name
store_path = "./vector_store_john_doe"
collection_name = "ai_learning_john_doe"
```

### Sanitization Rules
1. Convert to lowercase
2. Replace non-alphanumeric chars (except `_` and `-`) with `_`
3. Collapse multiple `_` into single `_`
4. Remove leading/trailing `_`

### Fallback Behavior
- If authentication not available: uses "default"
- If user name not available: uses email
- If email not available: uses "default"

## Security Considerations

1. **Path Traversal Protection**: Username sanitization prevents path traversal
2. **Access Control**: Authentication required before store access
3. **Isolation**: File system permissions can be set per user store
4. **Validation**: User identifier is validated before use

## Future Enhancements

Potential improvements:
- User store migration tools
- Admin interface to view all user stores
- User store backup/restore functionality
- Storage quota management per user
- User store analytics

## Testing

To test per-user stores:
1. Log in as different users
2. Add content as each user
3. Verify each user only sees their own content
4. Check that stores are created in separate directories

## Troubleshooting

### User Store Not Found
- Check if user is authenticated
- Verify username sanitization
- Check file system permissions

### Cross-User Data Leakage
- Verify all pages use `get_user_store_path()`
- Check that no hardcoded paths remain
- Ensure authentication is working

### Local Development Issues
- Default user store is used when auth unavailable
- Can manually set user identifier for testing
- Check that fallback logic works correctly

