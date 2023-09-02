import requests
import feedparser
import schedule
import time
from datetime import datetime
from utils import Logger_Factory as lgFactory
from utils import MongoClient as mongoClient
logger = lgFactory.create("xmlFeed")

# 最後に更新された日時を保持する変数
# 初回は何も設定しない
last_modified = None

# 気象庁のXML提供URL
URL = "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"

def getFeed():
    global last_modified
    logger.info('【Feedの取得を開始します】')
    headers = {}
    if last_modified:
        headers['If-Modified-Since'] = last_modified

    response = requests.get(URL, headers=headers)
    response.encoding = "UTF-8"

    # HTTPステータスコードが200の場合は、データが更新されていると判断
    if response.status_code == 200:
        last_modified = response.headers.get('Last-Modified', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
        feed = feedparser.parse(response.text)

        client = mongoClient.getClient()
        collection = client["feed"]["current"]

        for entry in feed.entries:
            data = {
                "title": entry.title,
                "link": entry.link,
                "updated": entry.updated,
                "author": entry.author,
                "content": entry.content[0].value,
                "processed": False
            }
            collection.update_one({"link": entry.link}, {"$set": data}, upsert=True)

        logger.info(f'{len(feed.entries)}件のFeedを追加しました')
        client.close()
        logger.info('【Feedの取得を終了します】')
    else:
        logger.info("【Feedは更新されていません】")

def main():
    logger.info('=== start xmlFeedProcess ===')
    schedule.every(60).seconds.do(getFeed)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()