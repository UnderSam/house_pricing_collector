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
