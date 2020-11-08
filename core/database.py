from motor.motor_asyncio import AsyncIOMotorClient

from core.settings import MONGO_URL


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_URL, maxPollSize=10, minPollSize=10)


async def close_mongo_connection():
    db.client.close()
