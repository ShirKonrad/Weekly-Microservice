from CSP.Constraint import OverlapConstraint
from CSP.CSP import CSP


def get_assignment(tasks, events, day_hours):
    events.sort(key=lambda event: event.start_time)

    domains = {task: task.get_possible_start_times(events, day_hours) for task in tasks}

    csp: CSP = CSP(tasks, domains)
    csp.add_constraint(OverlapConstraint(tasks))

    assignment = csp.solve()

    solution = dict(sorted(assignment.items(), key=lambda item: item[1]))
    solution = {task.id: assign.__str__() for task, assign in solution.items()}
    return solution
