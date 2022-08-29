import pymongo
from typing import Dict, Any
from env_config import config


class MongoManager:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(config['MONGO_CONNECT_URL'])
        self.db = self.client[config['HOUSE_DB']]
        self.house_records = self.db[config['HOUSE_COLLECTION']]

    def insert_house_records(self, detail_info: Dict[str, Any]) -> None:
        try:
            self.house_records.insert_one(detail_info)
        except Exception as e:
            print(f'Insert failed: {e}')


if __name__ == '__main__':
    manager = MongoManager()
    client = manager.house_records
    _ = client.find({}).limit(1)
    # client.update_many({}, {'$unset': {'Unnamed: 0': 1}})
    # client.update_many({ 'prefered_sex': '男'}, { '$set': { 'prefered_sex': 'boy' } }, True)
    # client.update_many({ 'prefered_sex': '女'}, { '$set': { 'prefered_sex': 'girl' } }, True)
    # client.update_many({ 'prefered_sex': '男女'}, { '$set': { 'prefered_sex': 'both' } }, True)
    # client.update_many({ 'region_id': 1}, { '$set': { 'region_id': '臺北' } }, True)
    # client.update_many({ 'region_id': 3}, { '$set': { 'region_id': '新北' } }, True)
