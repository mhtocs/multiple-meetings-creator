"""Payload schemas for meeting API
"""

from typing import List
from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass(frozen=True)
class Participants:
    email: str


@dataclass_json
@dataclass()
class Session:
    topic: str
    presenter: str
    agenda: str
    participants: List[Participants]
    start_time_in_sec: int = field(repr=False)
    startTime: str = field(init=False)  # calculated field
    duration: str
    timezone: str

    def __post_init__(self):
        start_time = datetime.fromtimestamp(self.start_time_in_sec)
        self.startTime = f'{start_time.strftime("%b %d, %Y %I:%M %p")}'
