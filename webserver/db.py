from typing import List
from webserver.model import Status, ChannelItem

_in_memory_store = {
    1: ChannelItem(1, 'Outdoor 1', 'rtsp://freja.hiof.no:1935/rtplive/definst/hessdalen03.stream', Status.OFF),
    2: ChannelItem(2, 'Kitchen 1', 'rtsp://172.23.3.10/face_track_20_fhd', Status.OFF),
    3: ChannelItem(3, 'Kitchen 2', 'rtsp://34.82.126.102:554/face_track_rafa_fhd', Status.OFF),
    4: ChannelItem(4, 'Dining Room', 'rtsp://34.82.126.102:554/face_track_rafa_fhd', Status.OFF),
}

async def channel_find_by_id(channel_id: int) -> ChannelItem:
    if not int(channel_id) in _in_memory_store:
        raise Exception("Channel id {} is not found".format(channel_id))
    return _in_memory_store[channel_id]

async def channel_find_all() -> List[ChannelItem]:
    return _in_memory_store.values()

async def channel_create(description: str, rtsp_link: str, status=Status.OFF) -> int:
    max_id = max(_in_memory_store.keys()) + 1 if _in_memory_store else 1
    _tmp_db[max_id] = ChannelItem(max_id, description, rtsp_link, status)
    return max_id

async def channel_update_status(channel_id: int, status: Status) -> None:
    if not int(channel_id) in _in_memory_store:
        raise Exception("Channel id {} is not found".format(channel_id))
    _in_memory_store[channel_id].status = status

async def channel_delete(channel_id: int) -> None:
    if channel_id in _in_memory_store:
        del _in_memory_store[channel_id]
