import numpy as np

def generate_signal(tfidf_matrix):
    signal = np.mean(tfidf_matrix.toarray(), axis=0)
    confidence = np.std(signal)
    return signal, confidence