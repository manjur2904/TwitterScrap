"""TF-IDF vectorization utilities.

The project uses a `TfidfVectorizer` configured to keep a reasonably-sized
vocabulary for downstream signal generation. Stop-word filtering is disabled
here deliberately so that domain-specific tokens (tickers, short terms)
aren't removed automatically.

Configuration (max_features, min_df) is defined in config.py.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from config import TFIDF_MAX_FEATURES, TFIDF_MIN_DF


def vectorize(texts):
    """Transform a list of texts to a TF-IDF sparse matrix.

    Raises `ValueError` if `texts` is empty to fail-fast for upstream logic.
    """
    if not texts:
        raise ValueError("Empty text list passed to vectorizer")

    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        min_df=TFIDF_MIN_DF,          # ignore rare words
        stop_words=None,   # IMPORTANT: remove english stopwords filter
        token_pattern=r"(?u)\b[a-zA-Z]{2,}\b"
    )

    return vectorizer.fit_transform(texts)
