from dataclasses import dataclass
from datetime import datetime

from models.TaskDomain import TaskDomainObject


@dataclass
class Task:
    id: int
    duration: int
    priority: int
    deadline: datetime
    domain: TaskDomainObject

    def __init__(self, id, duration, priority, deadline):
        self.id = id
        self.duration = duration
        self.priority = priority
        self.deadline = deadline
        self.domain = TaskDomainObject(interval=self.duration, end_date=self.deadline)

    def __hash__(self):
        return hash((self.id, self.duration, self.deadline, self.priority))

    def __eq__(self, other):
        # return hash(self) == hash(other)
        return self.id == other.id

    def __repr__(self):
        return f'Task(id={self.id}, duration={self.duration}, deadline={self.deadline.__str__()}, priority={self.priority})'

    def get_possible_start_times(self, events, day_hours):
        return self.domain.get_domain_range(events, day_hours)