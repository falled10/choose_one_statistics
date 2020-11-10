from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from fastapi.routing import APIRouter

from api.statistics.schemas import ResponseOptionSchema, CreateUpdateOptionSchema
from api.statistics.services import create_or_update_option
from core.database import get_database

router = APIRouter()


@router.post('', response_model=ResponseOptionSchema)
async def create_or_update_option_route(options: List[CreateUpdateOptionSchema],
                                        conn: AsyncIOMotorClient = Depends(get_database)):
    return await create_or_update_option(conn, options)
