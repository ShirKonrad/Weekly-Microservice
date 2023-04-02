# Base class for all constraints
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict

from Classes import Task


class BaseConstraint(ABC):
    # The variables that the constraint is between
    def __init__(self, vars) -> None:
        self.vars = vars

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment, var) -> bool:
        pass


class OverlapConstraint(BaseConstraint):
    def __init__(self, tasks) -> None:
        super().__init__(tasks)

    def satisfied(self, assignment: Dict[Task, datetime], curr_task: Task) -> bool:
        for task_in_assignment, task_assign in assignment.items():
            if task_in_assignment != curr_task and self.overlap(assignment[curr_task], curr_task.duration, task_assign, task_in_assignment.duration):
                return False
        return True

    def overlap(self, t1_start, t1_dur, t2_start, t2_dur):
        if (t1_start <= t2_start < t1_start + timedelta(hours=t1_dur)) or (t2_start <= t1_start < t2_start + timedelta(hours=t2_dur)):
            return True
        return False

