import re

def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)  # keep only letters
    text = re.sub(r"\s+", " ", text).strip()

    return text