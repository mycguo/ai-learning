"""Utilities for detecting duplicate content."""
from typing import List, Set
from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    """Normalize URL for comparison."""
    parsed = urlparse(url)
    # Remove fragment, normalize scheme and netloc
    normalized = urlunparse((
        parsed.scheme.lower() or 'https',
        parsed.netloc.lower().replace('www.', ''),
        parsed.path.rstrip('/'),
        parsed.params,
        parsed.query,
        ''  # Remove fragment
    ))
    return normalized


def detect_duplicate_urls(urls: List[str]) -> tuple[List[str], List[str]]:
    """Detect duplicate URLs in a list.
    
    Returns:
        (unique_urls, duplicates)
    """
    seen = set()
    unique_urls = []
    duplicates = []
    
    for url in urls:
        normalized = normalize_url(url)
        if normalized in seen:
            duplicates.append(url)
        else:
            seen.add(normalized)
            unique_urls.append(url)
    
    return unique_urls, duplicates


def check_url_exists(url: str, existing_urls: Set[str]) -> bool:
    """Check if a URL already exists in the repository."""
    normalized = normalize_url(url)
    normalized_existing = {normalize_url(u) for u in existing_urls}
    return normalized in normalized_existing

