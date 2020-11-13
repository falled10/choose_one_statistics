from core.schemas import CamelModel


class OptionModel(CamelModel):
    poll_id: int
    option_id: int
    took_part_times: int = 0
    selected_times: int = 0
    took_part_in_poll_times: int = 0
    won_times: int = 0
    is_active: bool = True


COLLECTION_NAME = 'options_collection'
