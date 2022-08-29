import pymongo
from typing import Dict, Any
from env_config import config
from pymongo.collection import Collection


class MongoManager:
    def __init__(self) -> None:
        pass

    def get_collection_of_house_records(self) -> Collection:
        client = pymongo.MongoClient(config['MONGO_CONNECT_URL'])
        db = client[config['HOUSE_DB']]
        house_records = db[config['HOUSE_COLLECTION']]
        return house_records

    def insert_or_update_house_records(self, collection: Collection, detail_info: Dict[str, Any]) -> None:
        try:
            post_id = detail_info['post_id']
            query_info = {'post_id': post_id}
            update_info = {'$set': detail_info}
            collection.update_one(
                query_info,
                update_info,
                upsert=True
            )
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
