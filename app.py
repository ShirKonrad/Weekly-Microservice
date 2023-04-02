import json
from datetime import datetime

from flask import Flask, jsonify, request

from Classes import Task, Event
from main import get_assignment

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/assignment', methods=['POST'])
def get_tasks_assignment():
    working_hours = (9, 18)  # Working hours from 9am to 6pm
    # tasks = [Task(id=1, duration=2, deadline=datetime(2023, 3, 30), priority=2),
    #          Task(id=2, duration=3, deadline=datetime(2023, 3, 29, 19, 0), priority=1),
    #          Task(id=3, duration=2, deadline=datetime(2023, 3, 28, 10, 0), priority=3),
    #          Task(id=4, duration=4, deadline=datetime(2023, 3, 31, 19, 0), priority=1)]
    events = [Event(id=1, start_time=datetime(2023, 3, 29, 10, 0), finish_time=datetime(2023, 3, 29, 12, 0)),
              Event(id=2, start_time=datetime(2023, 3, 29, 14, 0), finish_time=datetime(2023, 3, 29, 15, 0))]
    request_data = request.get_json()
    tasks = []
    for task in request_data:
        date_format = '%Y-%m-%dT%H:%M:%S.000Z'
        tasks.append(
            Task(id=task["id"], duration=task["estTime"], deadline=datetime.strptime(task["dueDate"], date_format),
                 priority=task["priority"]))
    print(tasks)

    solution = get_assignment(tasks, events, working_hours)
    return json.dumps(solution)


if __name__ == '__main__':
    app.run(debug=True)
