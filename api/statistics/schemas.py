from enum import Enum
from typing import List

from core.schemas import CamelModel


class EventType(str, Enum):
    WON = 'WON'
    SELECTED = 'SELECTED'
    TOOK_PART = 'TOOK_PART'
    TOOK_PART_IN_POLL = 'TOOK_PART_IN_POLL'


class CreateUpdateOptionSchema(CamelModel):
    poll_id: int
    option_id: int
    event_type: EventType


class CalculatedOptionSchema(CamelModel):
    option_id: int
    selected_percentage: int
    win_percentage: int


class RequestStatisticsSchema(CamelModel):
    options_ids: List[int]


class RequestOptionsSchema(CamelModel):
    data: List[CreateUpdateOptionSchema]
