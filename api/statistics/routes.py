from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, status
from fastapi.responses import Response
from fastapi.routing import APIRouter

from api.statistics.schemas import RequestOptionsSchema, CalculatedOptionSchema, RequestStatisticsSchema
from api.statistics.services import create_or_update_option, get_calculated_options, make_option_inactive
from core.database import get_database

router = APIRouter()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_or_update_options_route(options: RequestOptionsSchema,
                                         conn: AsyncIOMotorClient = Depends(get_database)):
    """Creates new or updates existed one option
    checking by `option_id` and `poll_id`
    """
    for option in options.data:
        await create_or_update_option(conn, option)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/{poll_id}', status_code=status.HTTP_200_OK, response_model=List[CalculatedOptionSchema])
async def get_statistics_for_option_ids(poll_id: int, conn: AsyncIOMotorClient = Depends(get_database)):
    """Returns statistic for options selected by `options_ids`
    """
    return await get_calculated_options(poll_id, conn)


@router.delete("/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def make_option_inactive_route(option_id: int, conn: AsyncIOMotorClient = Depends(get_database)):
    """Disable statistics for option with `option_id`
    """
    await make_option_inactive(option_id, conn)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
