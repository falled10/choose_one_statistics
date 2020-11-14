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
    resp = client.post('api/statistics', json={'data': data})
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
    resp = client.post('api/statistics', json={'data': data})
    assert resp.status_code == 400


@pytest.mark.asyncio
def test_update_existed_option(client, conn, option, event_loop):
    data = {
        'option_id': option['option_id'],
        'poll_id': option['poll_id'],
        'event_type': 'SELECTED'
    }
    old_win_count = option['selected_times']
    resp = client.post('api/statistics', json={'data': data})
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
    resp = client.post('api/statistics', json={'data': data})
    assert resp.status_code == 204
    new_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': option['option_id']}))
    assert new_option['selected_times'] == 2
    assert new_option['took_part_times'] == 3
    created_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': option_id_for_create}))
    assert created_option['took_part_times'] == 1


@pytest.mark.asyncio
def test_get_statistics_for_options(client, option):
    option_id_for_create = 2
    data = [
        {
            'option_id': option_id_for_create,
            'poll_id': option['poll_id'],
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
        },
        {
            'option_id': option_id_for_create,
            'poll_id': option['poll_id'],
            'event_type': 'TOOK_PART_IN_POLL'
        }
    ]
    client.post('api/statistics', json={'data': data})
    resp = client.get(f'api/statistics/{option["poll_id"]}')
    assert resp.status_code == 200
    assert resp.json()[0]['optionId'] == option['option_id']
    assert resp.json()[0]['selectedPercentage'] == 66
    assert resp.json()[1]['selectedPercentage'] == 0


@pytest.mark.asyncio
def test_make_option_inactive(client, option, conn, event_loop):
    resp = client.delete(f'api/statistics/{option["option_id"]}')
    assert resp.status_code == 204
    update_option = event_loop.run_until_complete(conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'option_id': option["option_id"]}))
    assert not update_option['is_active']


@pytest.mark.asyncio
def test_if_option_inactive_it_does_not_show_in_statistics(client, option):
    client.delete(f'api/statistics/{option["option_id"]}')
    resp = client.get(f'api/statistics/{option["poll_id"]}')
    assert resp.status_code == 200
    assert len(resp.json()) == 0
