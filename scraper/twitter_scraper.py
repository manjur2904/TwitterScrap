import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]

logging.basicConfig(level=logging.INFO)

class TwitterScraper:
    def __init__(self):
        options = Options()

        # ✅ Use a SEPARATE Selenium profile (NOT your main Chrome)
        options.add_argument(r"--user-data-dir=C:\selenium_chrome_profile")

        # Stability flags (VERY IMPORTANT on Windows)
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        service = Service()  # Uses chromedriver from PATH
        self.driver = webdriver.Chrome(service=service, options=options)

    def scrape_tweets(self, max_tweets=2000):
        tweets = []

        for tag in HASHTAGS:
            url = f"https://twitter.com/search?q=%23{tag}&f=live"
            self.driver.get(url)
            time.sleep(8)

            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while len(tweets) < max_tweets:
                cards = self.driver.find_elements(By.XPATH, "//article")
                logging.info(
                    f"Found {len(cards)} tweets | Total collected: {len(tweets)}"
                )

                for card in cards:
                    try:
                        text = card.text.strip()
                        if not text:
                            continue

                        tweets.append({
                            "username": "unknown",
                            "content": text,
                            "timestamp": time.time()
                        })
                    except Exception:
                        continue

                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(random.uniform(2.5, 4))

                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height

        return tweets

    def close(self):
        self.driver.quit()
