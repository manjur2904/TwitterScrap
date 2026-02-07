"""Main runner for the Twitter scraping and analysis pipeline.

This script ties together scraping, cleaning, deduplication, vectorization,
signal generation and plotting. It is intentionally simple: each stage is
kept as a separate module to make testing and grading straightforward.

IMPORTANT: All configuration (hashtags, timeouts, max tweets, headless mode,
output paths, etc.) is in `config.py`. Edit config.py to customize behavior.

Logging: All logs are written to a file (see config.LOG_FILE) with detailed
information including filename, line number, and function name.

First-time setup:
- Set HEADLESS_MODE=False in config.py for the first run to log in manually.
- After that, set HEADLESS_MODE=True for automated runs (session is saved).
"""

import logging
from config import (
    HEADLESS_MODE,
    MAX_TWEETS,
    DEDUPLICATION_ENABLED,
    OUTPUT_PARQUET_FILE,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
)

# Configure logging to file with detailed format
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
    ],
)
logger = logging.getLogger(__name__)
logger.info("=" * 80)
logger.info("Twitter Scraper Pipeline Started")
logger.info("=" * 80)

from scraper.twitter_scraper import TwitterScraper
from processing.cleaner import clean_text
from processing.deduplicator import deduplicate
from analysis.text_vectorizer import vectorize
from analysis.signal_generator import generate_signal
from storage.parquet_store import save_parquet
from visualization.streaming_plots import streaming_plot

# Initialize scraper with headless mode from config
logger.info(f"Starting scraper (headless_mode={HEADLESS_MODE})")
scraper = TwitterScraper(headless=HEADLESS_MODE)
logger.info(f"Scraper initialized. Collecting up to {MAX_TWEETS} tweets...")

raw_tweets = scraper.scrape_tweets(max_tweets=MAX_TWEETS)
logger.info(f"Scraping completed. Collected {len(raw_tweets)} raw tweets.")
scraper.close()
logger.info("Scraper session closed.")

# Clean text from each tweet
logger.info("Starting text cleaning process...")
for t in raw_tweets:
    t["content"] = clean_text(t["content"])
logger.info(f"Text cleaning completed for {len(raw_tweets)} tweets.")

# Deduplicate tweets
logger.info(f"Starting deduplication (enabled={DEDUPLICATION_ENABLED})...")
tweets = deduplicate(raw_tweets) if DEDUPLICATION_ENABLED else raw_tweets
logger.info(f"Deduplication completed. {len(tweets)} unique tweets remaining (removed {len(raw_tweets) - len(tweets)} duplicates).")

# Save to parquet
logger.info(f"Saving tweets to parquet file: {OUTPUT_PARQUET_FILE}")
save_parquet(tweets, file_path=OUTPUT_PARQUET_FILE)
logger.info(f"Parquet file saved successfully ({len(tweets)} records).")

# Extract and validate text
logger.info("Extracting valid text content...")
texts = [t["content"] for t in tweets if t["content"].strip()]
logger.info(f"Valid texts extracted: {len(texts)}/{len(tweets)} (filtered {len(tweets) - len(texts)} empty/whitespace-only).")

if len(texts) == 0:
    logger.error("No valid tweet text available after cleaning. Pipeline aborted.")
    raise RuntimeError("No valid tweet text available after cleaning")

logger.info(f"Total tweets processed: {len(tweets)}")
logger.info(f"Valid texts for TF-IDF: {len(texts)}")
logger.info("Sample cleaned tweets:")
for i in range(min(5, len(texts))):
    logger.info(f"  [{i+1}] {texts[i][:80]}...") if len(texts[i]) > 80 else logger.info(f"  [{i+1}] {texts[i]}")

# Vectorization
logger.info(f"Starting TF-IDF vectorization (max_features={TFIDF_MAX_FEATURES}, min_df={TFIDF_MIN_DF})...")
tfidf_matrix = vectorize(texts)
logger.info(f"TF-IDF vectorization completed. Matrix shape: {tfidf_matrix.shape}")

# Signal generation
logger.info("Generating aggregated market signal...")
signal, confidence = generate_signal(tfidf_matrix)
logger.info(f"Signal generation completed. Confidence (std): {confidence:.6f}")
logger.info(f"Signal vector shape: {signal.shape}")

# Visualization
logger.info("Displaying streaming plot...")
streaming_plot(signal)
logger.info("Plot closed.")

logger.info("="*80)
logger.info("Twitter Scraper Pipeline Completed Successfully")
logger.info("="*80)