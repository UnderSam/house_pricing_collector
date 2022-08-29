from beanie import init_beanie
import motor.motor_asyncio
from dotenv import dotenv_values
from .models.house_record import HouseRecord

config = dotenv_values(".env")

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        config['MONGO_CONNECT_URL']
    )
    db = client[config['HOUSE_DB']]
    collection = db[config['HOUSE_COLLECTION']]

    await init_beanie(database=collection, document_models=[HouseRecord])
