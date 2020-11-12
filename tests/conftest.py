import pytest

from fastapi.testclient import TestClient

from api.statistics.models import COLLECTION_NAME
from core.settings import MONGO_INITDB_DATABASE
from core.database import get_database, connect_to_mongo, close_mongo_connection
from main import app


@pytest.fixture()
async def conn():
    try:
        await connect_to_mongo()
        db = await get_database()
        yield db
    finally:
        await close_mongo_connection()


@pytest.fixture(autouse=True)
async def collections(conn):
    yield
    await conn.drop_database(MONGO_INITDB_DATABASE)


@pytest.fixture()
async def option(conn):
    data = {
        'option_id': 1,
        'poll_id': 1,
        'took_part_times': 2,
        'selected_times': 1,
        'took_part_poll_times': 1,
        'won_times': 1
    }
    option = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].insert_one(data)
    return await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one({'_id': option.inserted_id})


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
