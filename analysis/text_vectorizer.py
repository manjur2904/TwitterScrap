from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize(texts):
    if not texts:
        raise ValueError("Empty text list passed to vectorizer")

    vectorizer = TfidfVectorizer(
        max_features=3000,
        min_df=2,          # ignore rare words
        stop_words=None,  # IMPORTANT: remove english stopwords filter
        token_pattern=r"(?u)\b[a-zA-Z]{2,}\b"
    )

    return vectorizer.fit_transform(texts)
