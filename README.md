
# 📊 Twitter/X Market Intelligence System (Indian Stock Market)

## 📌 Overview

This project is a real-time data collection and analysis system designed to extract actionable market intelligence from Twitter/X discussions related to the Indian stock market.

The system scrapes tweets without using any paid APIs, processes and cleans the data, stores it efficiently in Parquet format, and converts textual information into quantitative trading signals suitable for algorithmic trading research.

---

## 🎯 Key Features

- Twitter/X scraping using Selenium (No paid APIs)
- Focus on Indian market hashtags: #nifty50, #sensex, #intraday, #banknifty
- Collects 2000+ tweets from the last 24 hours
- Deduplication, Unicode handling, emoji support
- Efficient Parquet storage
- TF-IDF based text-to-signal conversion
- Memory-efficient visualization
- Scalable and production-ready design

---

## 🏗️ Project Structure

twitter_market_intel/
├── scraper/
│   └── twitter_scraper.py
├── processing/
│   ├── cleaner.py
│   └── deduplicator.py
├── storage/
│   └── parquet_store.py
├── analysis/
│   ├── text_vectorizer.py
│   └── signal_generator.py
├── visualization/
│   └── streaming_plots.py
├── main.py
├── requirements.txt
└── README.md

---

## ⚙️ Tech Stack

- Python 3.9+
- Selenium
- Pandas, NumPy
- PyArrow
- Scikit-learn
- Matplotlib

---

## 🚀 How to Run

### 1. Clone Repository
git clone https://github.com/your-username/twitter_market_intel.git
cd twitter_market_intel

### 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Install Chrome & ChromeDriver
Ensure ChromeDriver matches your Chrome version and is in PATH.

### 5. Run Pipeline
python main.py

---

## 📤 Output

- tweets.parquet (cleaned tweet dataset)
- Aggregated market signal
- Confidence score
- Visualization plot

---
