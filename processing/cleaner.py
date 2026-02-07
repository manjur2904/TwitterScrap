"""Text cleaning helpers.

This module provides a small `clean_text` function used to normalize tweet
strings before further processing (TF-IDF). The cleaning is intentionally
conservative: remove URLs, mentions and hashtags, keep letters and collapse
whitespace.
"""

import re


def clean_text(text):
    """Normalize tweet text for vectorization.

    Steps:
    - Lowercase
    - Remove URLs, @mentions and #hashtags
    - Remove non-letter characters
    - Collapse multiple spaces

    Returns an empty string when `text` is falsy.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    # keep only letters and whitespace
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text