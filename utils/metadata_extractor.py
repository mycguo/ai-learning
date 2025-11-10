"""Utilities for extracting metadata from URLs and content."""
import re
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup


def extract_domain_category(url: str) -> str:
    """Extract a category hint from the URL domain."""
    domain = urlparse(url).netloc.lower()
    
    # Common AI learning site patterns
    category_map = {
        'arxiv.org': 'Research Papers',
        'arxiv': 'Research Papers',
        'paperswithcode.com': 'Research Papers',
        'github.com': 'Tools & Frameworks',
        'github': 'Tools & Frameworks',
        'medium.com': 'Tutorials & Courses',
        'medium': 'Tutorials & Courses',
        'towardsdatascience.com': 'Tutorials & Courses',
        'youtube.com': 'Tutorials & Courses',
        'youtube': 'Tutorials & Courses',
        'coursera.org': 'Tutorials & Courses',
        'udacity.com': 'Tutorials & Courses',
        'kaggle.com': 'Tutorials & Courses',
        'huggingface.co': 'Tools & Frameworks',
        'openai.com': 'LLMs & Transformers',
        'anthropic.com': 'LLMs & Transformers',
    }
    
    for key, category in category_map.items():
        if key in domain:
            return category
    
    return 'General'


def extract_title_from_url(url: str, content: Optional[str] = None) -> str:
    """Extract title from URL or content."""
    # Try to get title from content first
    if content:
        try:
            soup = BeautifulSoup(content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag and title_tag.text.strip():
                return title_tag.text.strip()
        except:
            pass
    
    # Fallback: extract from URL path
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split('/') if p]
    if path_parts:
        # Use last meaningful part of path
        title = path_parts[-1].replace('-', ' ').replace('_', ' ')
        # Remove file extensions
        title = re.sub(r'\.[a-z]+$', '', title, flags=re.IGNORECASE)
        return title.title()
    
    # Final fallback: use domain
    return parsed.netloc.replace('www.', '')


def extract_tags_from_content(content: str, title: str = "") -> list:
    """Extract potential tags from content and title."""
    tags = []
    
    # Common AI/ML keywords
    ai_keywords = {
        'transformer': 'Transformers',
        'llm': 'LLMs',
        'gpt': 'LLMs',
        'bert': 'NLP',
        'nlp': 'NLP',
        'computer vision': 'Computer Vision',
        'cv': 'Computer Vision',
        'reinforcement learning': 'Reinforcement Learning',
        'rl': 'Reinforcement Learning',
        'deep learning': 'Deep Learning',
        'neural network': 'Deep Learning',
        'pytorch': 'PyTorch',
        'tensorflow': 'TensorFlow',
        'mlops': 'MLOps',
        'fine-tuning': 'Fine-tuning',
        'rag': 'RAG',
        'vector database': 'Vector Databases',
    }
    
    combined_text = (title + " " + content).lower()
    
    for keyword, tag in ai_keywords.items():
        if keyword in combined_text and tag not in tags:
            tags.append(tag)
    
    return tags[:5]  # Limit to 5 tags


def create_metadata(
    url: Optional[str] = None,
    title: Optional[str] = None,
    content: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[list] = None,
    content_type: str = "url",
    notes: Optional[str] = None,
    learning_path: Optional[str] = None
) -> Dict:
    """Create standardized metadata for a learning item."""
    metadata = {
        'type': content_type,
        'added_date': datetime.now().isoformat(),
    }
    
    if url:
        metadata['source_url'] = url
        if not category:
            category = extract_domain_category(url)
        if not title and content:
            title = extract_title_from_url(url, content)
    
    if title:
        metadata['title'] = title
    
    if category:
        metadata['category'] = category
    
    if tags:
        metadata['tags'] = ', '.join(tags) if isinstance(tags, list) else tags
    elif content and title:
        # Auto-extract tags if not provided
        extracted_tags = extract_tags_from_content(content, title)
        if extracted_tags:
            metadata['tags'] = ', '.join(extracted_tags)
    
    if notes:
        metadata['notes'] = notes
    
    if learning_path:
        metadata['learning_path'] = learning_path
    
    return metadata


def fetch_url_content(url: str) -> Tuple[str, Optional[str]]:
    """Fetch content from a URL and return (content, error)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Encoding": "identity"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        if response.encoding is None:
            response.encoding = 'utf-8'
        
        return response.text, None
    except Exception as e:
        return "", str(e)

