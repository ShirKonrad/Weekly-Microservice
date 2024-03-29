from dataclasses import dataclass, field
from datetime import datetime, timedelta, time


@dataclass
class TaskDomainObject:
    interval: int
    end_date: datetime
    start_date: datetime

    def __init__(self, interval, end_date):
        self.interval = interval
        self.end_date = end_date
        self.start_date = self.get_next_round_hour_date(datetime.now())

    def get_next_round_hour_date(self, date):
        new_date = date
        new_hour = date.hour
        if date.minute != 0:
            new_hour = (new_hour + 1) % 24
            if new_hour == 0:
                new_date += timedelta(days=1)
        new_date = new_date.replace(microsecond=0, second=0, minute=0, hour=new_hour)
        return new_date

    # def __post_init__(self):
    #     new_hour = self.start_date.hour
    #     if self.start_date.minute != 0:
    #         new_hour = (new_hour + 1) % 24
    #         if new_hour == 0:
    #             self.start_date += timedelta(days=1)
    #     self.start_date = self.start_date.replace(microsecond=0, second=0, minute=0, hour=new_hour)

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

            # Check overlapping with events
            if event_i < len(events):
                curr_event = events[event_i]

                # If the current hour is after the current event, skip to the next event
                if curr_hour >= curr_event.finish_time:
                    event_i += 1
                    is_free = False

                # If the current hour overlaps with event, skip on the event time
                elif (curr_hour <= curr_event.start_time < curr_hour + timedelta(hours=self.interval)) or (
                        curr_event.start_time <= curr_hour < curr_event.finish_time):
                    is_free = False
                    curr_hour = curr_event.finish_time
                    event_i += 1

            if is_free:
                domain_range.append(curr_hour)
                curr_hour += timedelta(hours=1)

        return domain_range

    def is_out_of_working_hours(self, time, working_hours):
        if working_hours[0] == working_hours[1]:
            return False

        elif working_hours[0] < working_hours[1]:
            return ((time + timedelta(hours=self.interval)).hour <= working_hours[0] or (
                    time + timedelta(hours=self.interval)).hour > working_hours[1] or
                    time.hour < working_hours[0] or
                    time.hour >= working_hours[1])

        else:
            return ((working_hours[1] <= time.hour < working_hours[0]) or
                    (working_hours[0] >= (time + timedelta(hours=self.interval)).hour > working_hours[1]))


    def move_to_next_day(self, curr_time, working_hours):
        if working_hours[0] < working_hours[1]:

            # If the curr time is outside the working hours, but in the same day, add a day
            if curr_time.hour < working_hours[0] or curr_time.hour >= working_hours[1]:
                if curr_time.hour >= working_hours[1]:
                    curr_time += timedelta(days=1)

            # If the curr time is in the working hours (in case the end time of the task is outside the working hours), add a day
            else:
                curr_time += timedelta(days=1)

        elif working_hours[0] > working_hours[1]:
            # if curr_time.hour >= working_hours[0] or curr_time.hour < working_hours[1]:
            if curr_time.hour >= working_hours[0]:
                curr_time += timedelta(days=1)

        # Change the hour to the start working hour
        return curr_time.replace(hour=working_hours[0])

    def __hash__(self):
        return hash((self.interval, self.end_date, self.start_date))
