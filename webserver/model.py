from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    OFF = 0
    ON = 1

@dataclass
class ChannelItem:
    channel_id: int
    description: str
    rtsp_link: str
    status: Status
