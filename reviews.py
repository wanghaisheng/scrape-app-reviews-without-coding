from google_play_scraper import Sort, reviews_all
from app_store_scraper import AppStore
from urllib.parse import quote
import csv
import pandas as pd
import os
import random
from pathlib import Path

# Global variables to store scraped data
googlerows = []
applerows = []

# Function for scraping Google Play reviews
def play_store_scraper(package, country='us', lang='en'):
    try:
        results = reviews_all(package, sleep_milliseconds=0, lang=lang, country=country, sort=Sort.MOST_RELEVANT)
        for x, item in enumerate(results):
            googlerows.append(item)
        
        # Save the reviews to a CSV file
        df = pd.DataFrame(googlerows)
        df.to_csv(f"./{package}-{lang}-{country}-google-app-review.csv", index=False, encoding='utf-8')
    except Exception as e:
        print(f"Error scraping Google Play for {package}: {e}")
        return None

# Function for scraping App Store reviews
def app_store_scraper(app_name, country='us', lang='en'):
    if country == 'cn':
        app_name = quote(app_name)  # URL encode app name for Chinese App Store
        lang = 'zh-Hans-CN'
    
    app = AppStore(country=country, app_name=app_name)
    app.review(sleep=random.randint(3, 6))
    
    for review in app.reviews:
        data = {
            'score': review['rating'],
            'userName': review['userName'],
            'review': review['review'].replace('\r', ' ').replace('\n', ' ')
        }
        applerows.append(data)

    # Save the reviews to a CSV file
    df = pd.DataFrame(applerows)
    df.to_csv(f"./{app_name}-{country}-apple-app-review.csv", index=False, encoding='utf-8')

# Function to process the URLs and trigger scraping for each
def app_reviews():
    # Get input URLs from environment variables or hardcoded
    urls = os.getenv('app_urls', '').split(',')
    lang = os.getenv('lang', 'en')
    country = os.getenv('country', 'us')

    for url in urls:
        url = url.strip()

        if 'play.google.com' in url:
            package_name = url.split('id=')[-1]
            print(f"Scraping Google Play app: {package_name}")
            play_store_scraper(package_name, country, lang)

        elif 'apps.apple.com' in url:
            app_name = url.split('/')[-2]
            print(f"Scraping App Store app: {app_name}")
            app_store_scraper(app_name, country, lang)
        else:
            print(f"Skipping unsupported URL: {url}")

OUTPUT_DIR = Path("data")
app_reviews()
