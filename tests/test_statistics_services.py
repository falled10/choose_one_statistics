import pytest

from api.statistics.services import create_or_update_option
from api.statistics.schemas import CreateUpdateOptionSchema
from api.statistics.models import COLLECTION_NAME
from api.statistics.utils import get_percentage
from core.settings import MONGO_INITDB_DATABASE


@pytest.mark.asyncio
async def test_create_new_option(conn):
    data = {
        'option_id': 2,
        'poll_id': 1,
        'event_type': "TOOK_PART"
    }
    option_data = CreateUpdateOptionSchema(**data)
    await create_or_update_option(conn, option_data)
    new_option = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one({'option_id': data['option_id']})
    option_count = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].count_documents(
        {'option_id': option_data.option_id})
    assert option_count == 1
    assert new_option['selected_times'] == 0
    assert new_option['took_part_times'] == 1


@pytest.mark.asyncio
async def test_update_existed_option(conn, option):
    data = {
        'option_id': option['option_id'],
        'poll_id': option['poll_id'],
        'event_type': 'WON'
    }
    old_win_count = option['won_times']
    option_data = CreateUpdateOptionSchema(**data)
    await create_or_update_option(conn, option_data)
    new_option = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one({'option_id': data['option_id']})
    assert new_option['won_times'] == old_win_count + 1
    assert new_option['_id'] == option['_id']


def test_get_percentage():
    result = get_percentage(100, 50)
    assert result == 50


def test_get_percentage_from_30():
    result = get_percentage(100, 30)
    assert result == 30


def test_get_percentage_from_0():
    result = get_percentage(0, 30)
    assert result == 0
