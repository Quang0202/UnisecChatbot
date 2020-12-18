from pymongo import MongoClient
from pymongo import ASCENDING
import datetime

client = MongoClient("localhost", 27017)
db=client["unisec-db"]
log_collection = db.log
log_collection.create_index([("timestamp", ASCENDING)])  

class UnisecLogger():
    FORM_ACTIVATED = "form_activated"
    ENTITY_EXTRACTED = "entity_extracted"

    @staticmethod
    def log(type, target, value, message):
        """ Log to mongo """
        entry = {}
        entry['timestamp'] = datetime.datetime.utcnow()
        entry['type'] = type
        entry['target'] = target
        entry['value'] = value
        entry['message'] = message
        log_collection.insert_one(entry)
        print(entry)

# UnisecLogger.log(UnisecLogger.TYPE_INTENT_ACTIVATED, "intent_chon_truong", "chọn trường")