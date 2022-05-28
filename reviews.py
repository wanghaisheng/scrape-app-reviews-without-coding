from google_play_scraper import Sort, reviews_all
from app_store_scraper import AppStore
from google_play_scraper import app
import csv
from pathlib import Path
import pandas as pd
import random
import os

OUTPUT_DIR = Path("data")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = str(OUTPUT_DIR)
# package_name = 'com.netcompany.smittestop_exposure_notification'
package_name= 'com.lemon.lvoverseas'

googlerows = []
def play_store_scraper(package):
    results = reviews_all(package,sleep_milliseconds=0,lang='en',country='us',sort=Sort.MOST_RELEVANT)


    # Adds the fields to the CSV
    for x, item in enumerate(results):
        googlerows.append(item)

    

    df = pd.DataFrame(googlerows)
    df.to_csv(os.path.abspath('.')+os.sep+"data/"+package+"-google-app-review.csv", index=False)

applerows = []

def app_store_scraper(app_name):
    app = AppStore(country="us",app_name=app_name)
    app.review(sleep = random.randint(3,6))
#     app.review()

    for review in app.reviews:
        score = review['rating']
        username = review['userName']
        review = review['review']
        applerows.append(review)
    df = pd.DataFrame(applerows)
    df.to_csv(os.path.abspath('.')+os.sep+"data/"+app_name+"-apple-app-review.csv", index=False)

play_store_scraper(package_name)
app_store_scraper('capcut-video-editor')
