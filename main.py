from scraper.twitter_scraper import TwitterScraper
from processing.cleaner import clean_text
from processing.deduplicator import deduplicate
from analysis.text_vectorizer import vectorize
from analysis.signal_generator import generate_signal
from storage.parquet_store import save_parquet
from visualization.streaming_plots import streaming_plot

scraper = TwitterScraper()
raw_tweets = scraper.scrape_tweets()
scraper.close()

for t in raw_tweets:
    print("RAW:", t["content"])
    t["content"] = clean_text(t["content"])

tweets = deduplicate(raw_tweets)
save_parquet(tweets)

texts = [t["content"] for t in tweets if t["content"].strip()]

if len(texts) == 0:
    raise RuntimeError("No valid tweet text available after cleaning")

print(f"Total tweets scraped     : {len(tweets)}")
print(f"Valid texts for TF-IDF   : {len(texts)}")

print("Sample cleaned tweets:")
for i in range(min(5, len(texts))):
    print("-", texts[i])

tfidf_matrix = vectorize(texts)

signal, confidence = generate_signal(tfidf_matrix)
streaming_plot(signal)

print("Signal confidence:", confidence)