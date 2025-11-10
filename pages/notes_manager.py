"""Notes management page for AI Learning Repository."""
import streamlit as st
from pages.app_admin import get_vector_store, get_text_chunks
from utils.content_processor import process_note_for_ingestion, chunk_documents
from utils.metadata_extractor import create_metadata

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

# Note templates
NOTE_TEMPLATES = {
    "None": "",
    "Research Paper Summary": """# Paper Title
## Authors
## Publication Date
## Key Contributions
- 
- 
- 

## Methodology
## Results
## My Thoughts
## Related Papers
""",
    "Tutorial Notes": """# Tutorial: [Title]
## Source
## Key Concepts
- 
- 

## Code Examples
```python
# Add code here
```

## Takeaways
## Next Steps
""",
    "Concept Explanation": """# [Concept Name]
## Definition
## Key Components
- 
- 

## Use Cases
## Examples
## Related Concepts
""",
    "Learning Path Entry": """# Learning Path: [Name]
## Objective
## Prerequisites
- 
- 

## Resources
- 
- 

## Progress
## Notes
"""
}

def main():
    st.title("📝 Notes Manager")
    st.markdown("Add and manage your learning notes")
    
    # Template selection
    template_choice = st.selectbox(
        "Note Template (optional)",
        options=list(NOTE_TEMPLATES.keys())
    )
    
    # Form for note entry
    with st.form("note_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            note_title = st.text_input(
                "Note Title *",
                placeholder="e.g., Understanding Transformers"
            )
            category = st.selectbox(
                "Category",
                options=CATEGORIES,
                index=len(CATEGORIES) - 1
            )
        
        with col2:
            tags_input = st.text_input(
                "Tags (comma-separated)",
                placeholder="e.g., transformers, attention, nlp"
            )
            linked_url = st.text_input(
                "Linked URL (optional)",
                placeholder="https://..."
            )
        
        learning_path = st.text_input(
            "Learning Path (optional)",
            placeholder="e.g., 'LLM Fundamentals'"
        )
        
        # Note content
        note_content = st.text_area(
            "Note Content *",
            height=400,
            value=NOTE_TEMPLATES[template_choice],
            help="Supports Markdown formatting"
        )
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Note", type="primary")
        
        if submitted:
            if not note_title or not note_content:
                st.error("Please provide both a title and content for the note")
            else:
                # Process tags
                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else None
                
                # Process note
                with st.spinner("Processing and saving note..."):
                    try:
                        documents = process_note_for_ingestion(
                            note_content=note_content,
                            title=note_title,
                            category=category if category != "General" else None,
                            tags=tags,
                            learning_path=learning_path if learning_path else None,
                            linked_url=linked_url if linked_url else None
                        )
                        
                        # Add to vector store
                        vector_store = get_vector_store([doc.page_content for doc in documents])
                        
                        st.success(f"✅ Note '{note_title}' saved successfully!")
                        st.balloons()
                        
                        # Show preview
                        with st.expander("View saved note"):
                            st.markdown(f"**Title:** {note_title}")
                            st.markdown(f"**Category:** {category}")
                            if tags:
                                st.markdown(f"**Tags:** {', '.join(tags)}")
                            if linked_url:
                                st.markdown(f"**Linked URL:** {linked_url}")
                            st.markdown("---")
                            st.markdown(note_content)
                        
                        # Clear form (by rerunning)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error saving note: {e}")
                        st.exception(e)
    
    # Markdown help
    with st.expander("📖 Markdown Formatting Help"):
        st.markdown("""
        **Bold text**: `**text**`
        
        *Italic text*: `*text*`
        
        # Heading 1: `# Heading`
        
        ## Heading 2: `## Heading`
        
        - Bullet list: `- item`
        
        1. Numbered list: `1. item`
        
        `Code`: `` `code` ``
        
        ```python
        Code block:
        ```
        ```python
        code here
        ```
        ```
        
        [Link](url): `[text](url)`
        """)
    
    # Quick stats
    st.markdown("---")
    st.subheader("📊 Quick Stats")
    st.info("Note: Statistics feature coming soon!")


if __name__ == "__main__":
    main()

