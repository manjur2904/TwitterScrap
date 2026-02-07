"""Configuration file for Twitter Scraper.

All non-constant parameters are defined here. Adjust values below to customize
scraping behavior, timeouts, and output.
"""

# ============================================================================
# SCRAPING CONFIGURATION
# ============================================================================

# Hashtags to scrape (Twitter search terms)
HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]

# Maximum total tweets to collect across all hashtags
MAX_TWEETS = 2000

# Headless mode: Set to True to run without opening a visible browser window.
# Set to False for first-time setup (you'll log in manually and session is saved).
HEADLESS_MODE = True

# ============================================================================
# SELENIUM BROWSER CONFIGURATION
# ============================================================================

# Chrome profile path for persistent login sessions
CHROME_PROFILE_PATH = r"C:\selenium_chrome_profile"

# Timeout (seconds) for waiting for tweet elements to load
TWEET_LOAD_TIMEOUT = 20

# Scroll sleep delay range (seconds) for human-like behavior and detection avoidance
SCROLL_SLEEP_MIN = 2.5
SCROLL_SLEEP_MAX = 4.0

# Initial page load wait time (seconds)
PAGE_LOAD_WAIT = 8

# ============================================================================
# DATA PROCESSING CONFIGURATION
# ============================================================================

# Enable deduplication of tweets (removes exact content duplicates)
DEDUPLICATION_ENABLED = True

# ============================================================================
# VECTORIZATION CONFIGURATION
# ============================================================================

# Maximum number of features (words) to keep in TF-IDF vocabulary
TFIDF_MAX_FEATURES = 3000

# Minimum document frequency (ignore words in fewer than this many docs)
TFIDF_MIN_DF = 2

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Output Parquet file path
OUTPUT_PARQUET_FILE = "tweets.parquet"

# Enable debug screenshots when tweets fail to load
DEBUG_SCREENSHOTS_ENABLED = True

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log level: "DEBUG", "INFO", "WARNING", "ERROR"
LOG_LEVEL = "INFO"

# Log file path (logs will be written here instead of console)
LOG_FILE = "scraper.log"

# Log format: includes timestamp, level, file, line number, function, and message
LOG_FORMAT = (
    "%(asctime)s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s"
)
