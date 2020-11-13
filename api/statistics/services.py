from motor.motor_asyncio import AsyncIOMotorClient

from api.statistics.schemas import CreateUpdateOptionSchema, EventType, CalculatedOptionSchema
from api.statistics.models import COLLECTION_NAME, OptionModel
from api.statistics.utils import get_percentage
from core.settings import MONGO_INITDB_DATABASE


async def create_or_update_option(conn: AsyncIOMotorClient,
                                  option_data: CreateUpdateOptionSchema):
    data = {'option_id': option_data.option_id, 'poll_id': option_data.poll_id}
    option = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(data)
    increment_data = {
        EventType.SELECTED.value: {'selected_times': 1},
        EventType.WON.value: {'won_times': 1},
        EventType.TOOK_PART.value: {'took_part_times': 1},
        EventType.TOOK_PART_IN_POLL.value: {'took_part_in_poll_times': 1},
    }
    if option:
        await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].update_one(
            data, {'$inc': increment_data[option_data.event_type.value]}
        )
    else:
        data = OptionModel(**data)
        await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].insert_one(
            {**data.dict(), **increment_data[option_data.event_type.value]}
        )


async def get_calculated_options(poll_id: int, conn: AsyncIOMotorClient):
    options = conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find({'poll_id': poll_id, 'is_active': True})
    options = await options.to_list(length=256)
    result = [CalculatedOptionSchema(option_id=option['option_id'],
                                     win_percentage=get_percentage(option['took_part_in_poll_times'],
                                                                   option['won_times']),
                                     selected_percentage=get_percentage(option['took_part_times'],
                                                                        option['selected_times']))
              for option in options]
    return result


async def make_option_inactive(option_id: int, conn: AsyncIOMotorClient):
    await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].update_one({'option_id': option_id},
                                                                  {'is_active': False})
