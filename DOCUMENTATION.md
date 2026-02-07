# PROJECT DOCUMENTATION
## Twitter/X Market Intelligence Scraper

---

## 1. EXECUTIVE SUMMARY

This project implements a **Selenium-based web scraper** that collects tweets from Twitter/X related to Indian stock market hashtags, processes the text data through a pipeline of cleaning, deduplication, and TF-IDF vectorization, and generates market intelligence signals suitable for financial analysis.

**Assignment Compliance:**
- ✅ Uses Selenium for browser automation (not API-based)
- ✅ Fully configurable via `config.py`
- ✅ Comprehensive file-based logging
- ✅ Clean modular architecture
- ✅ Error handling & timeouts
- ✅ Persistent session management
- ✅ No paid APIs or external services

---

## 2. PROJECT ARCHITECTURE

### System Diagram
```
config.py (Configuration)
    ↓
main.py (Pipeline Orchestrator)
    ↓
[Scraper] → [Processor] → [Analyzer] → [Storage + Visualization]
    ↓           ↓            ↓             ↓
  Twitter   Clean/Dedup   TF-IDF      Parquet
  Search    Text          Signal       + Logs
```

### Data Flow
```
Twitter/X Website
    ↓ (Selenium)
twitter_scraper.py (Collect raw tweets)
    ↓
Raw Tweet List: [{"content": "...", "username": "...", "timestamp": ...}]
    ↓
cleaner.py (Remove URLs, mentions, normalize text)
    ↓
Cleaned Tweet List: [{"content": "market analysis", ...}]
    ↓
deduplicator.py (Remove exact-duplicate tweets)
    ↓
Unique Tweet List
    ↓
text_vectorizer.py (TF-IDF: text → numbers)
    ↓
TF-IDF Matrix: shape (n_documents, 3000)
    ↓
signal_generator.py (Aggregate features)
    ↓
Signal + Confidence Score
    ↓
streaming_plots.py (Visualize)
parquet_store.py (Store to tweets.parquet)
    ↓
✓ Complete
```

---

## 3. MODULE DOCUMENTATION

### 3.1 `config.py` - Configuration Management

**Purpose:** Centralized configuration. All parameters can be adjusted without code changes.

**Key Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `HASHTAGS` | list | `["nifty50", "sensex", "intraday", "banknifty"]` | Hashtags to scrape |
| `MAX_TWEETS` | int | `2000` | Total tweets to collect |
| `HEADLESS_MODE` | bool | `True` | Run Chrome without visible window |
| `CHROME_PROFILE_PATH` | str | `r"C:\selenium_chrome_profile"` | Chrome profile storage |
| `TWEET_LOAD_TIMEOUT` | int | `20` | Seconds to wait for tweets to load |
| `SCROLL_SLEEP_MIN/MAX` | float | `2.5`/`4.0` | Random delay between scrolls |
| `TFIDF_MAX_FEATURES` | int | `3000` | Vocabulary size |
| `TFIDF_MIN_DF` | int | `2` | Min document frequency |
| `OUTPUT_PARQUET_FILE` | str | `"tweets.parquet"` | Output file path |
| `LOG_FILE` | str | `"scraper.log"` | Log file path |
| `LOG_LEVEL` | str | `"INFO"` | Logging level (DEBUG/INFO/WARNING/ERROR) |

---

### 3.2 `main.py` - Pipeline Orchestrator

**Purpose:** Coordinates all pipeline stages in proper sequence.

**Execution Order:**
```python
1. Load configuration
2. Initialize logger
3. Create TwitterScraper instance
4. Scrape tweets
5. Clean each tweet
6. Deduplicate
7. Vectorize to TF-IDF
8. Generate signal
9. Visualize
10. Store to Parquet
11. Report results
```

**Key Features:**
- Imports all modules
- Loads config parameters
- Handles errors gracefully
- Logs progress at each step
- Reports final statistics

---

### 3.3 `scraper/twitter_scraper.py` - Tweet Collection

**Purpose:** Use Selenium to automate browser and collect tweets.

**Key Methods:**

```python
class TwitterScraper:
    def __init__(self, headless=True):
        """Initialize Chrome with Selenium.
        
        Args:
            headless: Run in background if True
            
        Features:
            - Persistent login session storage
            - Anti-detection measures
            - User-agent spoofing
            - Navigator.webdriver hiding
        """
        
    def _is_logged_in(self):
        """Check if Twitter session is authenticated.
        
        Returns: bool - True if logged in
        
        Method: Navigate to home, check page title for login phrases
        """
        
    def scrape_tweets(self, max_tweets=200):
        """Collect tweets from configured hashtags.
        
        Args:
            max_tweets: Target number of tweets
            
        Returns:
            list: [{"username": str, "content": str, "timestamp": float}, ...]
            
        Process:
            1. Check login status
            2. For each hashtag:
               a. Navigate to search URL
               b. Wait for tweets to load
               c. Extract tweet elements
               d. Scroll and collect until max_tweets reached
        """
        
    def close(self):
        """Shutdown browser and free resources."""
```

**Anti-Detection Measures:**
- User-agent spoofing (mimics real browser)
- Disable automation flags
- Hide navigator.webdriver
- Random scroll delays
- Proper wait times

---

### 3.4 `processing/cleaner.py` - Text Normalization

**Purpose:** Clean and normalize tweet text for analysis.

**Cleaning Pipeline:**
```python
def clean_text(text):
    """Clean and normalize tweet text.
    
    Steps:
    1. Lowercase
    2. Remove URLs (http://...)
    3. Remove @mentions
    4. Remove #hashtags
    5. Remove non-letters/punctuation
    6. Collapse whitespace
    7. Trim edges
    
    Example:
    Input:  "Check @user! #nifty50 📈 http://t.co/xyz up 2%"
    Output: "check user nifty50 up"
    """
```

---

### 3.5 `processing/deduplicator.py` - Duplicate Removal

**Purpose:** Remove exact-duplicate tweets.

```python
def deduplicate(tweets_list):
    """Remove tweets with identical content.
    
    Algorithm: Hash-based (Python set)
    Time: O(n)
    Space: O(n)
    
    Example:
    Input:  1850 tweets (129 duplicates)
    Output: 1721 unique tweets
    """
```

---

### 3.6 `analysis/text_vectorizer.py` - TF-IDF Vectorization

**Purpose:** Convert text to numerical feature matrix.

```python
def vectorize(texts):
    """Convert texts to TF-IDF sparse matrix.
    
    Configuration:
    - max_features: 3000 (vocabulary size)
    - min_df: 2 (ignore rare words)
    - stop_words: None (keep domain-specific terms)
    
    Returns:
    - scipy.sparse.csr_matrix
    - Shape: (n_documents, 3000)
    
    Why TF-IDF?
    - Weighs common words less
    - Weighs rare/specific words more
    - Produces meaningful numerical representation
    """
```

---

### 3.7 `analysis/signal_generator.py` - Signal Aggregation

**Purpose:** Aggregate TF-IDF features into market signal.

```python
def generate_signal(tfidf_matrix):
    """Generate market signal from TF-IDF matrix.
    
    Calculation:
    - signal = mean(tfidf_matrix, axis=0)  # Mean per feature
    - confidence = std(signal)             # Std dev
    
    Returns:
    - signal: np.array[3000] - mean activation per feature
    - confidence: float - std dev (0.0-1.0)
    
    Interpretation:
    - High confidence (>0.05): Consistent sentiment across tweets
    - Low confidence (<0.02): Noisy/contradictory signals
    - signal[i]: Importance of feature i
    """
```

---

### 3.8 `storage/parquet_store.py` - Data Persistence

**Purpose:** Save tweets to Apache Parquet format.

```python
def save_parquet(tweets, file_path="tweets.parquet"):
    """Persist tweets to Parquet file.
    
    Benefits:
    - Columnar format (efficient for analytics)
    - Compression (5-10x smaller than CSV)
    - Type-safe (schema preserved)
    - Fast I/O (binary format)
    
    File Size: 2000 tweets ≈ 2-4 MB
    """
```

---

### 3.9 `visualization/streaming_plots.py` - Plotting

**Purpose:** Visualize aggregated market signal.

```python
def streaming_plot(signal):
    """Plot aggregated market signal.
    
    Plot Type: Line plot
    X-axis: Feature index (0-2999)
    Y-axis: Running-average activation
    
    Shows: Overall sentiment/signal trend
    """
```

---

## 4. INSTALLATION & SETUP

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (matching Chrome version, in PATH)

### Installation Steps

```bash
# 1. Navigate to project
cd C:\Users\user\Desktop\.DIV\TwitterScraper\TwitterScrap

# 2. Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### First-Time Login Setup

```bash
# 1. Edit config.py:
HEADLESS_MODE = False  # Allow visible browser

# 2. Run:
python main.py

# 3. Log in to Twitter manually in Chrome window

# 4. Close Chrome (credentials saved)

# 5. Edit config.py back:
HEADLESS_MODE = True  # For normal operation

# 6. Run again:
python main.py
```

---

## 5. CONFIGURATION EXAMPLES

### Example 1: Standard Operation
```python
HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]
MAX_TWEETS = 2000
HEADLESS_MODE = True
TWEET_LOAD_TIMEOUT = 20
DEDUPLICATION_ENABLED = True
TFIDF_MAX_FEATURES = 3000
LOG_LEVEL = "INFO"
```

### Example 2: Quick Test
```python
HASHTAGS = ["nifty50"]
MAX_TWEETS = 200
TWEET_LOAD_TIMEOUT = 20
LOG_LEVEL = "DEBUG"
```

### Example 3: Slow Network
```python
TWEET_LOAD_TIMEOUT = 40
SCROLL_SLEEP_MIN = 3.0
SCROLL_SLEEP_MAX = 5.0
PAGE_LOAD_WAIT = 15
```

### Example 4: Detailed Analysis
```python
MAX_TWEETS = 5000
TFIDF_MAX_FEATURES = 5000
TFIDF_MIN_DF = 1
LOG_LEVEL = "DEBUG"
```

---

## 6. EXECUTION

### Running the Pipeline

```bash
python main.py
```

### Expected Output

```
INFO:root:Starting Twitter Market Intelligence Scraper...
INFO:root:Scraping tweets for #nifty50...
INFO:root:Collected 245 tweets for #nifty50
INFO:root:Scraping tweets for #sensex...
INFO:root:Collected 198 tweets for #sensex
...
INFO:root:Total tweets scraped: 1,853
INFO:root:Total unique tweets: 1,721
INFO:root:Starting TF-IDF vectorization (max_features=3000, min_df=2)...
INFO:root:Created TF-IDF matrix (1721, 3000)
INFO:root:Generated market signal with confidence: 0.0342
INFO:root:Saving tweets to tweets.parquet...
INFO:root:Pipeline completed successfully!
```

### Output Files

**tweets.parquet:**
```python
import pandas as pd
df = pd.read_parquet("tweets.parquet")
print(df.head())
# Columns: username, content, timestamp
# Format: Apache Parquet (binary, compressed)
```

**scraper.log:**
```
2026-02-07 14:35:12,789 | twitter_scraper.py:42 (scrape_tweets) | Found 15 tweets
2026-02-07 14:35:13,456 | cleaner.py:15 (clean_text) | Cleaned 1500 texts
2026-02-07 14:35:14,123 | text_vectorizer.py:31 (vectorize) | Created matrix (1721, 3000)
```

---

## 7. TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| **"Log in to X" message** | Set `HEADLESS_MODE = False`, log in manually, switch back to `True` |
| **Tweets timeout (after 20 sec)** | Increase `TWEET_LOAD_TIMEOUT` to 30 or 40 |
| **ChromeDriver not found** | Add ChromeDriver to PATH or update path in config |
| **No tweets collected** | Check internet connection; verify hashtags are trending |
| **Parquet not created** | Check `scraper.log` for errors; verify write permissions |
| **Out of memory** | Reduce `MAX_TWEETS` or `TFIDF_MAX_FEATURES` |

---

## 8. PERFORMANCE METRICS

### Typical Runtime
- Scraping: 5-12 minutes (depends on tweet volume)
- Cleaning: < 1 second
- Deduplication: < 1 second
- Vectorization: 5-10 seconds
- Signal generation: < 1 second
- Visualization: < 2 seconds
- **Total: 5-15 minutes**

### Resource Usage
- **Memory:** 200-500 MB
- **Disk:** Output file (tweets.parquet): 2-5 MB
- **CPU:** Moderate (Selenium I/O bound)

### Time Complexity
- Scraping: O(n) where n = tweets
- Cleaning: O(n×m) where m = avg words/tweet
- Dedup: O(n) hash-based
- Vectorization: O(n×m)
- **Overall dominated by scraping (browser I/O)**

---

## 9. SECURITY & PRIVACY

### Credentials
- Stored only in local Chrome profile (`C:\selenium_chrome_profile`)
- Not in code, config files, or logs
- Not sent to external services

### Anti-Detection Measures
- User-agent spoofing
- Disable automation flags
- Hide navigator.webdriver property
- Random delays between requests
- Proper page load waits

### External Services
- No API keys required
- No paid services
- No external authentication
- No data sent outside local machine

---

## 10. DEPENDENCIES

```
selenium          # Browser automation
pandas            # Data manipulation
numpy             # Numerical operations
pyarrow           # Parquet I/O
scikit-learn      # TF-IDF vectorization
matplotlib        # Visualization
```

**Total size:** ~200 MB (virtual environment)

---

## 11. COMPLIANCE CHECKLIST

- ✅ **Assignment Requirement:** Uses Selenium (not API-based)
- ✅ **Configurable:** All parameters in `config.py`
- ✅ **Logging:** Comprehensive file logs with context
- ✅ **Modular:** Separate modules for each concern
- ✅ **Error Handling:** Timeouts, exception handling
- ✅ **Session Management:** Persistent login credentials
- ✅ **Documentation:** Docstrings, comments throughout
- ✅ **No External APIs:** Uses public web interface only
- ✅ **Headless Capable:** Can run in background
- ✅ **Tested:** Exit code 0 on successful runs

---

## 12. FUTURE ENHANCEMENTS

Potential improvements (not implemented):
- Parallel hashtag scraping
- Incremental/resume capability
- Sentiment analysis
- Keyword extraction
- Real-time streaming
- Database integration
- Web UI dashboard

---

## 13. VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial release |

---

**Last Updated:** February 7, 2026  
**Status:** Complete and tested  
**Exit Code:** 0 (success)
