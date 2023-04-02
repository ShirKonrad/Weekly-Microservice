# This is a sample Python script.
from datetime import datetime, timedelta
from typing import List, Dict

from Constraint import OverlapConstraint
from CSP import CSP
from Classes import Task, Event


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def get_assignment(tasks, events, working_hours):
    events.sort(key=lambda event: event.start_time)

    domains = {task: task.get_possible_start_times(events, working_hours) for task in tasks}

    csp: CSP = CSP(tasks, domains)
    csp.add_constraint(OverlapConstraint(tasks))

    assignment = csp.solve()

    solution = dict(sorted(assignment.items(), key=lambda item: item[1]))
    solution = {task.id: assign.__str__() for task, assign in solution.items()}
    return solution


def main():
    working_hours = (9, 18)  # Working hours from 9am to 6pm
    tasks = [Task(id=1, duration=2, deadline=datetime(2023, 3, 30), priority=2),
            Task(id=2, duration=3, deadline=datetime(2023, 3, 29, 19, 0), priority=1),
             Task(id=3, duration=2, deadline=datetime(2023, 3, 28, 10, 0), priority=3),
             Task(id=4, duration=4, deadline=datetime(2023, 3, 31, 19, 0), priority=1)]
    events = [Event(id=1, start_time=datetime(2023, 3, 29, 10, 0), finish_time=datetime(2023, 3, 29, 12, 0)),
              Event(id=2, start_time=datetime(2023, 3, 29, 14, 0), finish_time=datetime(2023, 3, 29, 15, 0))]

    print(events)
    print(tasks)

    solution = get_assignment(tasks, events, working_hours)

    print("---------------------------SOLUTION-----------------------------")
    # for task, assign in solution.items():
    #     start_time = assign.__str__()
    #     print("task " + task.id.__str__() + ": " + start_time)

    print(solution)

    # domain = Domain(end_date=datetime(2023, 1, 3) + timedelta(hours=8))
    # for hour in domain.optional_hours():
    #     print(hour)


if __name__ == '__main__':
    main()
