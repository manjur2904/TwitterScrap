"""Simple deduplication utility.

Removes duplicate tweets based on the exact `content` string. Keeps the
original ordering of the first occurrence for deterministic output.
"""


def deduplicate(tweets_list):
    """Return a list with duplicate `content` values removed.

    Args:
        tweets_list (list): List of dicts with at least the `content` key.

    Returns:
        list: Filtered list preserving first-occurrence order.
    """
    seen = set()
    unique_items = []
    for tweet in tweets_list:
        content = tweet["content"]
        if content not in seen:
            seen.add(content)
            unique_items.append(tweet)
    return unique_items