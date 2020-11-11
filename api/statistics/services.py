from motor.motor_asyncio import AsyncIOMotorClient

from api.statistics.schemas import CreateUpdateOptionSchema, EventType, CalculatedOptionSchema
from api.statistics.models import COLLECTION_NAME
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
        option = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].update_one(
            data, {'$inc': increment_data[option_data.event_type.value]}
        )
    else:
        option = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].insert_one(
            {**data, **increment_data[option_data.event_type.value]}
        )
    return option


async def get_calculated_options(poll_id: int, conn: AsyncIOMotorClient,
                                 page: int, page_size: int):
    options = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find(
        {'poll_id': poll_id}).skip((page - 1) * page_size).limit(page_size)
    result = [CalculatedOptionSchema(option_id=option.option_id,
                                     win_percentage=get_percentage(option.took_part_in_poll_times,
                                                                   option.win_times),
                                     selected_percentage=get_percentage(option.took_part_times,
                                                                        option.selected_times))
              for option in options]
    return result
