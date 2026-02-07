"""Generate a simple aggregated signal from TF-IDF features.

This module contains a very small, demonstrative signal generator: it
computes the mean feature activation across documents and uses the
standard deviation of that mean as a lightweight confidence measure.
"""

import numpy as np


def generate_signal(tfidf_matrix):
    """Return (signal, confidence) from a TF-IDF sparse matrix.

    Args:
        tfidf_matrix: SciPy/NumPy-compatible sparse matrix from TF-IDF.

    Returns:
        tuple: (signal: np.ndarray, confidence: float)
    """
    signal = np.mean(tfidf_matrix.toarray(), axis=0)
    confidence = np.std(signal)
    return signal, confidence