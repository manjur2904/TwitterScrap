"""Twitter scraper module using Selenium.

This module contains `TwitterScraper`, a small Selenium-based scraper that
navigates the Twitter (X) web UI to collect tweet text for a list of
hashtags. The implementation uses a persistent Chrome profile to keep a
logged-in session between runs (so headless operation can reuse cookies).

Usage notes:
- First run with `headless=False` and log in manually to save session.
- Subsequent runs can use `headless=True` to run without opening a window.

The code intentionally keeps Selenium usage (not API-based scraping)
because the technical assignment requires browser automation.
"""

import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import (
    HASHTAGS,
    CHROME_PROFILE_PATH,
    TWEET_LOAD_TIMEOUT,
    SCROLL_SLEEP_MIN,
    SCROLL_SLEEP_MAX,
    DEBUG_SCREENSHOTS_ENABLED,
)

# Get logger (will use config from main.py)
logger = logging.getLogger(__name__)

class TwitterScraper:
    """
    Args:
        headless (bool): If True, start Chrome in headless mode. Keep False
            for the first run to perform manual login and persist session.
    """

    def __init__(self, headless=True):
        self.headless = headless
        options = Options()

        # Using a SEPARATE Selenium profile from config (NOT main Chrome)
        options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")

        # Stability flags
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        # Reduce detection: common user-agent and disable automation switches
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        )
        options.add_argument(f"user-agent={ua}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Run Chrome headless to avoid opening a visible browser window
        if headless:
            # For newer Chrome versions use the new headless mode flag; fall back to older if needed
            try:
                options.add_argument("--headless=new")
            except Exception:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        service = Service()  # Uses chromedriver from PATH
        self.driver = webdriver.Chrome(service=service, options=options)

        # Remove webdriver flag to make automation less detectable
        try:
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                },
            )
        except Exception:
            # Not critical if CDP isn't available
            pass

    def _is_logged_in(self):
        """Return True if the Selenium session appears logged in.

        Heuristic: navigate to the home timeline and check the page title for
        common login/signup phrases. This is a light-weight check used to
        determine whether we must prompt the user to manually log in.
        """
        try:
            # Try to navigate to home timeline to check login status
            self.driver.get("https://twitter.com/home")
            time.sleep(2)
            # If we end up on login page, we're not logged in
            return "Log in to X" not in self.driver.title and "Sign up to X" not in self.driver.title
        except Exception:
            return False

    def scrape_tweets(self, max_tweets=200):
        """Collect tweets for configured hashtags.

        Args:
            max_tweets (int): Upper bound on total tweets to collect across all tags.

        Returns:
            list: List of dicts with keys `username`, `content`, `timestamp`.
        """
        tweets = []

        # Check if we're logged in. If not logged in and headless, abort with
        # a clear message so the user can perform the one-time manual login.
        if not self._is_logged_in():
            if self.headless:
                logger.error(
                    "❌ NOT LOGGED IN to Twitter and running in headless mode!\n"
                    "SETUP REQUIRED: Run this script with headless=False FIRST:\n"
                    "  - Modify main.py to use TwitterScraper(headless=False)\n"
                    "  - A Chrome window will open and you must log in manually\n"
                    "  - Close the browser to persist the session\n"
                    "  - Then switch back to headless=True for normal operation"
                )
                self.close()
                raise RuntimeError("Twitter login required. See instructions above.")
            else:
                # Visible mode: prompt the user to perform manual login.
                logger.warning("⏳ NOT LOGGED IN. Please log in to Twitter in the browser window...")
                input("Press ENTER after logging in: ")
                if not self._is_logged_in():
                    logger.error("Still not logged in. Exiting.")
                    self.close()
                    raise RuntimeError("Failed to log in to Twitter")

        for tag in HASHTAGS:
            # Build search URL for the hashtag and open it.
            url = f"https://twitter.com/search?q=%23{tag}&f=live"
            self.driver.get(url)

            # Wait for tweet article elements to appear on the page.
            wait = WebDriverWait(self.driver, TWEET_LOAD_TIMEOUT)
            try:
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article")))
            except Exception:
                logger.warning(
                    "Timed out waiting for tweets to load for tag %s — page title '%s'",
                    tag,
                    self.driver.title,
                )

            last_height = self.driver.execute_script("return document.body.scrollHeight")

            # Scroll and collect until we reach `max_tweets` or page end.
            while len(tweets) < max_tweets:
                cards = self.driver.find_elements(By.XPATH, "//article")
                logger.info(f"Found {len(cards)} tweets | Total collected: {len(tweets)}")

                if not cards:
                    # If no articles yet, wait a bit then retry once. Save a
                    # screenshot for debugging when running headless.
                    time.sleep(3)
                    cards = self.driver.find_elements(By.XPATH, "//article")
                    if not cards:
                        logger.warning("No tweet elements found for tag %s — saving page snapshot.", tag)
                        if DEBUG_SCREENSHOTS_ENABLED:
                            try:
                                self.driver.save_screenshot(f"debug_{tag}.png")
                            except Exception:
                                pass
                        break

                for card in cards:
                    try:
                        text = card.text.strip()
                        if not text:
                            continue

                        tweets.append({"username": "unknown", "content": text, "timestamp": time.time()})
                    except Exception:
                        # Skip malformed cards
                        continue

                # Scroll down to load more tweets and sleep a short randomized
                # interval to reduce detection risk and mimic human behavior.
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(SCROLL_SLEEP_MIN, SCROLL_SLEEP_MAX))

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        return tweets

    def close(self):
        """Shutdown the webdriver and free resources."""
        self.driver.quit()
