from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    start_time: datetime
    finish_time: datetime

    def __hash__(self):
        return hash((self.id, self.start_time, self.finish_time))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f'Event(start_time={self.start_time.__str__()}, finish_time={self.finish_time.__str__()})'