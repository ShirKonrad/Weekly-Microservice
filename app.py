import json
from datetime import datetime

from flask import Flask, jsonify, request

from models.Event import Event
from models.Task import Task
from service import get_assignment

app = Flask(__name__)

DATE_FORMAT = '%d.%m.%Y, %H:%M:%S'


@app.route('/assignment', methods=['POST'])
def get_tasks_assignment():
    request_data = request.get_json()
    print(request_data)

    tasks = []
    events = []
    day_hours = (request_data["dayHoursStart"], request_data["dayHoursEnd"])
    for task in request_data["tasks"]:
        tasks.append(
            Task(id=task["id"], duration=task["estTime"], deadline=datetime.strptime(task["dueDate"], DATE_FORMAT),
                 priority=task["priority"]))

    for event in request_data["events"]:
        events.append(
            Event(id=event["id"], start_time=datetime.strptime(event["startTime"], DATE_FORMAT),
                  finish_time=datetime.strptime(event["endTime"], DATE_FORMAT)))
    print(tasks)
    print(events)

    solution = get_assignment(tasks, events, day_hours)
    return json.dumps(solution)


if __name__ == '__main__':
    app.run(debug=True)
