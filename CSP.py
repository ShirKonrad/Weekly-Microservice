from dataclasses import dataclass, field
from datetime import timedelta, datetime
from typing import TypeVar, Dict, List, Optional

from Constraint import BaseConstraint
from Classes import Task


class CSP:
    def __init__(self, variables, domains):
        self.variables: List[Task] = variables
        self.domains: Dict[Task, List[datetime]] = domains
        self.constraints: Dict[Task, List[BaseConstraint]] = {}
        # self.objective_function = lambda assignment: sum(
        #     task.priority for task in self.variables if task in assignment or assignment[task] is not None)

        for task in self.variables:
            self.constraints[task] = []

    # def addVariable(self, var: Task, domain: iter(datetime)):
    #     self.variables.append(var)

    def add_constraint(self, constraint: BaseConstraint):
        for task in constraint.vars:
            if task not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[task].append(constraint)

    # Check if the value assignment is consistent by checking all constraints
    # for the given variable against it
    def consistent(self, task: Task, assignment: Dict[Task, datetime]) -> bool:
        for constraint in self.constraints[task]:
            if not constraint.satisfied(assignment, task):
                return False
        return True

    def select_unassigned_variable(self, assignment):
        unassigned_variables = [variable for variable in self.variables if assignment[variable] is None]
        return max(unassigned_variables, key=lambda variable: len(self.domains[variable]))

    # The score function favors values that are closer to the deadline and have a higher priority. By doing so,
    # it encourages the solver to find solutions that prioritize tasks with higher priorities and earlier deadlines.
    def priority_score(self, task, value):
        # Calculate the time difference between the deadline of the task and the starting time of the value.
        time_diff = (task.deadline - value).total_seconds() / 60

        # Assign a priority score based on the priority of the task. The higher the priority, the higher the score.
        if task.priority == 1:
            priority_score = 3
        elif task.priority == 2:
            priority_score = 2
        else:
            priority_score = 1

        # Multiply the time difference by the priority score to get the final score.
        return time_diff * priority_score

    def assignment_score(self, assignment):
        score = 0
        for task, assign_time in assignment.items():
            score += self.priority_score(task, assign_time)

        return score
        # return sum(task.priority for task in assignment.keys())

    def backtracking_search(self, assignment: Dict[Task, datetime], variables, solution):
        # assignment is complete if every variable is assigned (our base case)
        # if len(assignment) == len(self.tasks):
        #     return assignment

        # if not variables:
        #     solution = max(self.assignment_score(assignment), self.assignment_score(solution))
        #     return solution

        task_to_assign = variables[0]
        assign_values = sorted(self.domains[task_to_assign], key=lambda val: self.priority_score(task_to_assign, val), reverse=True)

        # get all variables in the CSP but not in the assignment
        # unassigned: List[Task] = [task for task in self.tasks if task not in assignment]

        # get the every possible domain value of the first unassigned variable
        # task_to_assign: Task = unassigned[0]

        for assign_value in assign_values:
            local_assignment = assignment.copy()
            local_assignment[task_to_assign] = assign_value
            if self.consistent(task_to_assign, local_assignment):
                assignment[task_to_assign] = assign_value
                if self.assignment_score(assignment) > self.assignment_score(solution):
                    solution = assignment.copy()
                result = self.backtracking_search(assignment, variables[1:], solution)
                solution = result[1].copy()
                if result[0] is not None:
                    return result, solution
                del assignment[task_to_assign]
                # assignment[task_to_assign] = None

        # If not all variables can be assigned values without violating the constraints, then return a partial solution
        if task_to_assign in assignment:
            # assignment[task_to_assign] = None
            return assignment, solution

        # if len(assignment) == 0:
        #     return solution
            # if self.assignment_score(solution) > self.assignment_score(assignment):
            #     self.print_assignment(solution)
            #     self.print_assignment(assignment)
            #     return solution
            # else:
            #     self.print_assignment(solution)
            #     self.print_assignment(assignment)
            #     return assignment

        # If no value can be assigned to the variable without violating the constraints, then backtrack
        return None, solution
        # assignment[task_to_assign] = None


    def print_assignment(self, assignment):
        print("---------------------------SOLUTION-----------------------------")
        sol = dict(sorted(assignment.items(), key=lambda item: item[1]))
        for task, assign in sol.items():
            start_time = assign.__str__()
            print("task " + task.id.__str__() + ": " + start_time)

        # for assign_time in self.domains[task_to_assign].get_optional_hours_range():
        #     # for value in self.domains[first]:
        #     local_assignment = assignment.copy()
        #     local_assignment[task_to_assign] = assign_time
        #     # if we're still consistent, we recurse (continue)
        #     if self.consistent(task_to_assign, local_assignment):
        #
        #         result = self.backtracking_search(local_assignment)
        #
        #         if result is not None:
        #             return result
        #
        # assignment[task_to_assign] = None
        # return assignment

    def solve(self):
        # Sort the list of variables in decreasing order of priority
        tasks = sorted(self.variables, key=lambda t: t.priority, reverse=False)
        result = self.backtracking_search({}, tasks, {})
        return result[1]
