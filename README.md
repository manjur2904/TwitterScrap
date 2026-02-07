
# Twitter/X Market Intelligence Scraper

## 📌 Overview

A **Selenium-based web scraper** that collects tweets from Twitter/X related to Indian stock market hashtags (#nifty50, #sensex, #intraday, #banknifty), performs NLP preprocessing, applies TF-IDF vectorization, and generates actionable market signals for financial analysis.

**Technical Requirement:** Uses Selenium for browser automation (not API-based) as per assignment specifications.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Selenium Scraping** | Browser automation for real-time tweet collection |
| **Hashtag Targeting** | Configurable hashtags: #nifty50, #sensex, #intraday, #banknifty |
| **Tweet Collection** | Configurable limits (default: 2000) with timeout handling |
| **Headless Mode** | Run without visible window after login setup |
| **Text Cleaning** | Removes URLs, @mentions, #hashtags, normalizes text |
| **Deduplication** | Removes exact-duplicate tweets |
| **Persistent Storage** | Tweets saved to Parquet (columnar, compressed) |
| **TF-IDF Analysis** | Converts text to numerical features (3000 max) |
| **Signal Generation** | Aggregates TF-IDF features into market signal + confidence |
| **Visualization** | Plots aggregated signal using matplotlib |
| **File Logging** | Comprehensive logs with filename:line:function context |
| **Configurable** | All parameters in `config.py` — no code changes needed |

---

## 🏗️ Project Structure

```
TwitterScrap/
├── config.py                      # Configuration parameters
├── main.py                        # Pipeline orchestrator
├── requirements.txt               # Dependencies
├── scraper/
│   └── twitter_scraper.py        # Selenium-based scraper
├── processing/
│   ├── cleaner.py                # Text normalization
│   └── deduplicator.py           # Remove duplicates
├── analysis/
│   ├── text_vectorizer.py        # TF-IDF vectorization
│   └── signal_generator.py       # Signal aggregation
├── storage/
│   └── parquet_store.py          # Parquet persistence
├── visualization/
│   └── streaming_plots.py        # Plot generation
├── scraper.log                   # Logs (auto-generated)
└── tweets.parquet                # Output data (auto-generated)
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (matching your Chrome version, in PATH)

### Installation
```bash
# Navigate to project
cd C:\Users\user\Desktop\.DIV\TwitterScraper\TwitterScrap

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### First-Time Login Setup
The first run must be in visible mode to save login credentials:

1. Edit `config.py`:
   ```python
   HEADLESS_MODE = False  # Allow visible browser
   ```

2. Run: `python main.py`

3. Log in to Twitter/X manually when Chrome opens

4. Close the browser (credentials saved)

5. Switch back: `HEADLESS_MODE = True` for normal operation

---

## ⚙️ Configuration Guide

All settings are in **`config.py`**. Key parameters:

```python
# Scraping
HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]  # Hashtags
MAX_TWEETS = 2000                                           # Total tweets
HEADLESS_MODE = True                                        # No visible window

# Browser
CHROME_PROFILE_PATH = r"C:\selenium_chrome_profile"  # Login storage
TWEET_LOAD_TIMEOUT = 20                              # Wait time (sec)

# Processing
DEDUPLICATION_ENABLED = True                         # Remove duplicates

# TF-IDF
TFIDF_MAX_FEATURES = 3000                           # Vocabulary size
TFIDF_MIN_DF = 2                                    # Min word frequency

# Output
OUTPUT_PARQUET_FILE = "tweets.parquet"              # Output file
LOG_FILE = "scraper.log"                            # Log file
LOG_LEVEL = "INFO"                                  # Debug level
```

**Common adjustments:**
- **More tweets:** `MAX_TWEETS = 5000`
- **Slow network:** `TWEET_LOAD_TIMEOUT = 40`
- **Different hashtags:** `HASHTAGS = ["bitcoin", "ethereum", ...]`
- **Debug mode:** `LOG_LEVEL = "DEBUG"`

---

## 🚀 Running the Pipeline

```bash
python main.py
```

**Execution flow:**
1. Scrapes tweets from hashtags (Selenium)
2. Cleans text (removes URLs, mentions, punctuation)
3. Deduplicates exact-duplicate content
4. Vectorizes to TF-IDF features
5. Generates market signal + confidence
6. Visualizes signal plot
7. Saves tweets to Parquet

**Typical runtime:** 5-15 minutes (depends on tweet volume)

---

## 📊 Output Files

### `tweets.parquet`
Cleaned, deduplicated tweets dataset
```python
import pandas as pd
df = pd.read_parquet("tweets.parquet")
print(df.head())  # Columns: username, content, timestamp
```

### `scraper.log`
Complete execution log with file:line:function context
```
2026-02-07 14:35:12,789 | twitter_scraper.py:42 (scrape_tweets) | Found 15 tweets
2026-02-07 14:35:13,456 | cleaner.py:15 (clean_text) | Cleaned 1500 texts
```

---

## 🔧 Module Documentation

### `scraper/twitter_scraper.py`
Selenium-based Twitter scraper with persistent login sessions

**Key methods:**
- `__init__(headless=True)` — Initialize Chrome
- `_is_logged_in()` — Check authentication status
- `scrape_tweets(max_tweets)` — Collect tweets from hashtags
- `close()` — Shutdown browser

**Features:** Anti-detection (user-agent, CDP script hiding), infinite scroll, timeout handling

---

### `processing/cleaner.py`
Text normalization for analysis

**Operations:**
1. Lowercase text
2. Remove URLs, @mentions, #hashtags
3. Remove non-letter characters
4. Collapse whitespace

**Example:** `"Check @user #nifty50 http://t.co/xyz"` → `"check user nifty50"`

---

### `processing/deduplicator.py`
Remove exact-duplicate tweets

**Algorithm:** O(n) hash-based using Python set

**Typical result:** 1850 tweets → 1721 unique (7% reduction)

---

### `analysis/text_vectorizer.py`
TF-IDF vectorization (text-to-numbers)

**Configuration:**
- max_features: 3000 (vocabulary size)
- min_df: 2 (ignore rare words)
- Output: Sparse matrix (n_documents, 3000)

---

### `analysis/signal_generator.py`
Aggregate features into market signal

**Output:**
```python
signal: np.array[3000]  # Mean activation per feature
confidence: float       # Std dev (0.0-1.0 range)
```

**Interpretation:**
- High confidence (>0.05): Consistent sentiment
- Low confidence (<0.02): Noisy signals

---

### `storage/parquet_store.py`
Persist tweets to Apache Parquet

**Benefits:** Columnar format, compression, fast I/O, type-safe

---

### `visualization/streaming_plots.py`
Plot aggregated market signal

**Output:** Matplotlib line plot with running-average curve

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Log in to X" page** | Set `HEADLESS_MODE = False`, log in manually, switch back to `True` |
| **Tweets timeout** | Increase `TWEET_LOAD_TIMEOUT` to 30-40 in `config.py` |
| **ChromeDriver not found** | Ensure ChromeDriver in PATH or update path in config |
| **No tweets collected** | Check internet; verify hashtags are trending |
| **Memory issues** | Reduce `MAX_TWEETS` or `TFIDF_MAX_FEATURES` |

---

## 📈 Performance

- **Runtime:** 5-15 minutes (2000 tweets)
- **Memory:** ~200-500 MB
- **Output size:** 2-5 MB (Parquet, compressed)

---

## 🔐 Security & Privacy

- Credentials stored only in local Chrome profile (`C:\selenium_chrome_profile`)
- No paid APIs used
- No API keys or tokens
- Rate-limited with random delays
- Anti-detection measures (user-agent, automation hiding)

---

## ⚙️ Tech Stack

- **Selenium** — Browser automation
- **Pandas, NumPy** — Data processing
- **PyArrow** — Parquet I/O
- **Scikit-learn** — TF-IDF vectorization
- **Matplotlib** — Visualization

---

## 📋 Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] Chrome/Chromium installed
- [ ] ChromeDriver in PATH
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] First run: `HEADLESS_MODE = False` for login

---

## 🚦 Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run pipeline
python main.py

# View logs
type scraper.log  # Windows
cat scraper.log   # Mac/Linux

# Read output
python -c "import pandas as pd; print(pd.read_parquet('tweets.parquet').head())"
```

---

## ✅ Assignment Compliance

✓ Selenium browser automation (per requirement)  
✓ No paid APIs  
✓ Configurable via single config file  
✓ Comprehensive file logging with context  
✓ Clean module separation  
✓ Error handling & timeouts  
✓ Persistent session management  
✓ Headless execution capability  

---

**Version:** 1.0  
**Last Updated:** February 7, 2026
