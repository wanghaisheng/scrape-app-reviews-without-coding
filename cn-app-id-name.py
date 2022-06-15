import os
import csv
import json
import time
import requests


next_url = None

review_path = 'reviews'
if not os.path.exists(review_path):
    os.mkdir(review_path)


# with open('config_api.json', 'r') as file:
#     config = json.loads(file.read())
#     pending_queue = config['ids']
#     max_page = config['max_page']
#     headers = config['headers']
#     intervals = config['intervals']


# 发送请求获取响应
def get_response(app_id, page):
    time.sleep(5)
    try:
        url = 'https://amp-api.apps.apple.com/v1/catalog/cn/apps/' + app_id +'/reviews?l=zh-Hans-CN&offset=' + str(page * 10) + '&platform=web&additionalPlatforms=appletv%2Cipad%2Ciphone%2Cmac'
        r = requests.get(url)
#         r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError:
        return 'HTTPError!'


# 解析响应
def parse_response(r):
    global next_url
    if "next" in r.keys():
        next_url = r['next']
    else:
        next_url = None

    for item in r['data']:
        yield {
            "id": item['id'],
            "type": item['type'],
            "title": item['attributes']['title'],
            "userName": item['attributes']['userName'],
            "isEdited": item['attributes']['isEdited'],
            "review": item['attributes']['review'],
            "rating": item['attributes']['rating'],
            "date":  item['attributes']['date']
        }


# 写入 csv 文件
def write_to_file(app_id, item):
    with open(f'{review_path}/{app_id}.csv', 'a', encoding='utf-8-sig', newline='') as csv_file:
        fieldnames = ['id', 'type', 'title', 'userName', 'isEdited', 'review', 'rating', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(item)


# 主函数
def  main(appName,appid):

    print(f'开始爬取 {appid}')
    for i in range(0, 1000):
        r = get_response(appid, i)
        print(f"第 {i+1} 页评论已获取")
        for item in parse_response(r):
            write_to_file(cur_id, item)
        print(f'第 {i} 页评论已存储')
        if not next_url:
            break
    print(f'结束爬取 {cur_id}')


if __name__ == '__main__':
    try:
        appid = os.getenv('appid').strip()
        appName = os.getenv('appName').strip()
        main(appName,appid)    
        
    except:    
        print('pls input id and name')

