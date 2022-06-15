
import requests
import json
import time
import os

def SearchAppId(app):
    url = "http://itunes.apple.com/search?term=" + app + "&entity=software"
    r = requests.get(url)
    html = r.content
    html_doc = str(html, 'utf-8')
    data = json.loads(html_doc)
    resultCount = data['resultCount']
    results = data['results']
    print(app + " Find " + str(resultCount) + " result(s)")
    for i in range(resultCount):
        name = results[i]['trackName']
        app_id = results[i]['trackId']
        print("name：" + name, "id：" + str(app_id))

appName=''
appid=''
# https://apps.apple.com/us/app/indycar/id606905722
#     https://apps.apple.com/us/app/capcut-video-editor/id1500855883
# https://apps.apple.com/cn/app/妙健康-健康管理平台/id841386224?l=ru&see-all=reviews
# https://apps.apple.com/cn/app/%E5%A6%99%E5%81%A5%E5%BA%B7-%E5%81%A5%E5%BA%B7%E7%AE%A1%E7%90%86%E5%B9%B3%E5%8F%B0/id841386224?l=ru&see-all=reviews
appName = os.getenv('appName').strip()
SearchAppId(appName)    
