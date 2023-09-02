import xmltodict
import schedule
import requests
import time
from utils import Logger_Factory as lgFactory
from utils import MongoClient as mongoClient
logger = lgFactory.create("xmlFeed")

def save_xml(xml_data):

    data_dict = xmltodict.parse(xml_data)

    client = mongoClient.getClient()
    collection = client[data_dict["Report"]["Control"]["Title"]]["current"]

    collection.insert_one(data_dict)
    client.close()

def download():
    # 未処理のエントリのみを取得
    logger.info('【ダウンロードを開始しました】')

    client = mongoClient.getClient()
    collection = client["feed"]["current"]

    unprocessed_entries = collection.find({"processed": {"$ne": True}})

    count = 0

    for entry in unprocessed_entries:
        try:
            response = requests.get(entry['link'])
            response.encoding = "UTF-8"
            logger.debug(f'link:{entry["link"]}')
            save_xml(response.text)

            # 処理済みフラグをセット
            collection.update_one({"_id": entry["_id"]}, {"$set": {"processed": True}})
            count += 1
        except Exception as e:
            logger.warning(f"Error encountered for link: {entry['link']}. Error: {e}. Skipping...")
            continue
        finally:
            time.sleep(1)  # 1秒待機
    logger.info(f'【{count}件のダウンロードを終了しました】')

def main():
    logger.info('=== start DownLoader ===')
    schedule.every(60).seconds.do(download)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()