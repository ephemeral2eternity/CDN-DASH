import pymongo
import datetime
from monitor.ping import *
from monitor.get_hop_info import *
import pprint

def connect_to_mongodb(db_host, db_name):
    client = pymongo.MongoClient(db_host, 27017)
    db = client[db_name]
    return db

def insert_mongodb(collection, record):
    inserted = collection.insert(record)
    return inserted


if __name__ == "__main__":
    db_host = "qrank-mongodb.cmu-agens.com"
    db_name = "qrank"
    collection_name = "rtt"
    db = connect_to_mongodb(db_host, db_name)
    collection = db[collection_name]

    client_ip, client_info = get_ext_ip()
    mnRTT, srv_ip = getMnRTT('az.cmu-agens.com')
    inserted = insert_mongodb(collection, {"client":client_ip, "server":srv_ip, "date":datetime.datetime.utcnow(), "rtt":mnRTT})
    print(inserted)

    pprint.pprint(collection.find_one())