from pymongo import MongoClient

def getClient():
    # DB接続の初期設定
    HOST = 'jma-xml-mongo'
    PORT = 27017
    USERNAME = 'root'
    PASSWORD = 'password'

    return MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)