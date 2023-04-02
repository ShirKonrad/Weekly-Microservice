from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class TaskDomainObject:
    interval: int
    end_date: datetime
    start_date: datetime = field(default=datetime.now())

    def __post_init__(self):
        new_hour = self.start_date.hour
        if self.start_date.minute != 0:
            new_hour = (new_hour + 1) % 24
        self.start_date = self.start_date.replace(microsecond=0, second=0, minute=0, hour=new_hour)

    def get_domain_range(self, events, working_hours):
        domain_range = []
        curr_hour = self.start_date
        event_i = 0

        # Go over the time from now until the task's deadline, and get the free hours for the task to be scheduled
        while curr_hour <= self.end_date - timedelta(hours=self.interval):
            is_free = True

            # If the current hour is out of the working hours, move to the next day
            if self.is_out_of_working_hours(curr_hour, working_hours):
                is_free = False
                curr_hour = self.move_to_next_day(curr_hour, working_hours)

            # If the current hour overlaps with event, skip on the event time
            if event_i < len(events):
                curr_event = events[event_i]
                if (curr_hour <= curr_event.start_time < curr_hour + timedelta(hours=self.interval)) or (curr_event.start_time <= curr_hour < curr_event.finish_time):
                    is_free = False
                    curr_hour = curr_event.finish_time
                    event_i += 1

            if is_free:
                domain_range.append(curr_hour)
                curr_hour += timedelta(hours=1)

        return domain_range

    def is_out_of_working_hours(self, time, working_hours):
        return ((time + timedelta(hours=self.interval)).hour <= working_hours[0] or (
                time + timedelta(hours=self.interval)).hour > working_hours[1] or
                time.hour < working_hours[0] or
                time.hour >= working_hours[1])

    def move_to_next_day(self, curr_time, working_hours):
        # If the time is before midnight, add a day
        next_day = curr_time + timedelta(days=1)
        midnight = next_day.replace(microsecond=0, second=0, minute=0, hour=0)
        if curr_time < midnight:
            curr_time += timedelta(days=1)
        return curr_time.replace(hour=working_hours[0])

    def __hash__(self):
        return hash((self.interval, self.end_date, self.start_date))


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
        return f'Task(id={self.id}, duration={self.duration}, finish_time={self.deadline.__str__()}, priority={self.priority})'

    def get_possible_start_times(self, events, working_hours):
        return self.domain.get_domain_range(events, working_hours)


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

