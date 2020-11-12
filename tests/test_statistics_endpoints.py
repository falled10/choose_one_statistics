import pytest

from api.statistics.models import COLLECTION_NAME
from core.settings import MONGO_INITDB_DATABASE


@pytest.mark.asyncio
def test_create_new_option(client, conn, event_loop):
    data = {
        'option_id': 2,
        'poll_id': 1,
        'event_type': "TOOK_PART"
    }
    resp = client.post('api/statistics', json=[data])
    assert resp.status_code == 204
    new_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': data['option_id']}))
    assert new_option['took_part_times'] == 1


@pytest.mark.asyncio
def test_create_new_option_with_wrong_event_type(client):
    data = {
        'option_id': 2,
        'poll_id': 1,
        'event_type': "SOMETHING ELSE"
    }
    resp = client.post('api/statistics', json=[data])
    assert resp.status_code == 400


@pytest.mark.asyncio
def test_update_existed_option(client, conn, option, event_loop):
    data = {
        'option_id': option['option_id'],
        'poll_id': option['poll_id'],
        'event_type': 'SELECTED'
    }
    old_win_count = option['selected_times']
    resp = client.post('api/statistics', json=[data])
    assert resp.status_code == 204
    new_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': data['option_id']}))
    assert new_option['selected_times'] == old_win_count + 1


@pytest.mark.asyncio
def test_update_and_create_options(client, conn, option, event_loop):
    option_id_for_create = 2
    data = [
        {
            'option_id': option_id_for_create,
            'poll_id': 1,
            'event_type': "TOOK_PART"
        },
        {
            'option_id': option['option_id'],
            'poll_id': option['poll_id'],
            'event_type': 'SELECTED'
        },
        {
            'option_id': option['option_id'],
            'poll_id': option['poll_id'],
            'event_type': 'TOOK_PART'
        }
    ]
    resp = client.post('api/statistics', json=data)
    assert resp.status_code == 204
    new_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': option['option_id']}))
    assert new_option['selected_times'] == 2
    assert new_option['took_part_times'] == 3
    created_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': option_id_for_create}))
    assert created_option['took_part_times'] == 1
