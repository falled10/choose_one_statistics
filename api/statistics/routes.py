from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends, status
from fastapi.responses import Response
from fastapi.routing import APIRouter

from api.statistics.schemas import ResponseOptionSchema, CreateUpdateOptionSchema
from api.statistics.services import create_or_update_option
from core.database import get_database

router = APIRouter()


@router.post('', response_model=ResponseOptionSchema, status_code=status.HTTP_204_NO_CONTENT)
async def create_or_update_options_route(options: List[CreateUpdateOptionSchema],
                                         conn: AsyncIOMotorClient = Depends(get_database)):
    for option in options:
        await create_or_update_option(conn, option)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
