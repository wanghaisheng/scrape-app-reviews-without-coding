from google_play_scraper import Sort, reviews_all
from app_store_scraper import AppStore
from google_play_scraper import app
import csv
from pathlib import Path
import pandas as pd
import random
import os
from urllib.parse import urlencode, quote_plus,quote

try:
    google_app_package_url = os.getenv('google_app_package_url').strip()
    if 'https://play.google.com/store/apps/details?id=' in google_app_package_url:
        
        google_app_package_name=google_app_package_url.replace('https://play.google.com/store/apps/details?id=','')
        # https://play.google.com/store/apps/details?id=com.twitter.android
        if not len(google_app_package_name.split('.'))==3:
            print('not support package,',google_app_package_url,google_app_package_name)
except:
    google_app_package_name='com.lemon.lvoverseas'
try:
# https://apps.apple.com/us/app/indycar/id606905722
#     https://apps.apple.com/us/app/capcut-video-editor/id1500855883
#https://apps.apple.com/cn/app/妙健康-健康管理平台/id841386224?l=ru&see-all=reviews
#https://apps.apple.com/cn/app/%E5%A6%99%E5%81%A5%E5%BA%B7-%E5%81%A5%E5%BA%B7%E7%AE%A1%E7%90%86%E5%B9%B3%E5%8F%B0/id841386224?l=ru&see-all=reviews
    apple_app_package_url = os.getenv('apple_app_package_url').strip()
    if 'https://apps.apple.com' in apple_app_package_url:
        if '?' in apple_app_package_url:
            apple_app_package_url=apple_app_package_url.split('?')[0]
        
        apple_app_package_name=apple_app_package_url.split('/')[-2]
        if not len(apple_app_package_name)>0:
            print('not support package,',apple_app_package_url,apple_app_package_name)        
except:
    apple_app_package_name='capcut-video-editor'
try:
    country=os.getenv('country')
except:
    country=os.getenv('apple_app_package_url').strip().replace("https://apps.apple.com/").split('/')[0]
    print('country',country)
    if country is None or country =="":
        country='us'

try:
    lang=os.getenv('lang')
except:
    lang='en'
OUTPUT_DIR = Path("data")


googlerows = []
def play_store_scraper(package):
    results = reviews_all(package,sleep_milliseconds=0,lang='en',country='us',sort=Sort.MOST_RELEVANT)


    # Adds the fields to the CSV
    for x, item in enumerate(results):
        googlerows.append(item)

    

    df = pd.DataFrame(googlerows)
    df.to_csv("./"+package+'-'+lang+'-'+country+'-'+"google-app-review.csv", index=False)

applerows = []

def app_store_scraper(app_name,country=country,lang='us'):
    if country=='cn':
        #https://github.com/cowboy-bebug/app-store-scraper/issues/34
        print('url encode app name',quote(app_name))
        app_name=quote(app_name)
        lang='zh-Hans-CN'
    app = AppStore(country=country,app_name=app_name)
    app.review(sleep = random.randint(3,6))

    for review in app.reviews:
        data={}
        data['score']= review['rating']
        data['userName']= review['userName']
        data['review']= review['review'].replace('\r',' ').replace('\n',' ')
        
        applerows.append(data)
    df = pd.DataFrame(applerows)
    df.to_csv("./"+app_name+'-'+country+'-'+"apple-app-review.csv", index=False)
def app_reviews(country_code,app_id):

    return "https://itunes.apple.com/%s/rss/customerreviews/id=%s/sortBy=mostRecent/json" % (country_code, app_id)    
# https://itunes.apple.com/us/rss/customerreviews/id=1500855883/sortBy=mostRecent/json    
if not os.getenv('google_app_package_url')=='':
    play_store_scraper(google_app_package_name)
if not os.getenv('apple_app_package_name')=='':
    app_store_scraper(apple_app_package_name)

#huawei  xiaomi samsung

