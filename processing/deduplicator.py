def deduplicate(tweets_list):
    seen = set()
    unique_items = []
    for tweet in tweets_list:
        content = tweet["content"]
        if content not in seen:
            seen.add(content)
            unique_items.append(tweet)
    return unique_items