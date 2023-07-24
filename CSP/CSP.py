from datetime import datetime
from typing import Dict, List

from CSP.Constraint import BaseConstraint
from models.Task import Task


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
    def calc_score(self, task, value):
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
            score += self.calc_score(task, assign_time)

        return score

    def backtracking_search(self, assignment: Dict[Task, datetime], variables, solution):

        if not variables:
            return assignment, solution

        # Get the current task to assign and its possible values to assign from the domain
        task_to_assign = variables[0]
        assign_values = self.domains[task_to_assign]

        # If there are no values to assign, skip on the current task and continue to the next iteration
        if len(assign_values) == 0:
            return self.backtracking_search(assignment, variables[1:], solution)

        # Go over all the values to assign
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

        # If not all variables can be assigned values without violating the constraints, then return a partial solution
        if task_to_assign in assignment:
            return assignment, solution

        # If no value can be assigned to the variable without violating the constraints, then backtrack
        return None, solution


    def print_assignment(self, assignment):
        print("---------------------------SOLUTION-----------------------------")
        sol = dict(sorted(assignment.items(), key=lambda item: item[1]))
        for task, assign in sol.items():
            start_time = assign.__str__()
            print("task " + task.id.__str__() + ": " + start_time)


    def solve(self):
        # Sort the list of variables in ascending order of deadline and priority
        tasks = sorted(self.variables, key=lambda t: (t.deadline, t.priority), reverse=False)
        result = self.backtracking_search({}, tasks, {})
        return result[1]
