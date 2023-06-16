import json
from datetime import datetime

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from models.Event import Event
from models.Task import Task
from service import get_assignment

app = Flask(__name__)

DATE_FORMAT = '%d.%m.%Y, %H:%M:%S'


@app.errorhandler(HTTPException)
def handle_exception(e):
    print("HTTP ERROR")
    print(e)

    response = e.get_response()

    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response, e.code


@app.route('/assignment', methods=['POST'])
def get_tasks_assignment():
    try:
        print("------------------------------------------------------")
        print("Incoming request, time:" + datetime.now().__str__())
        request_data = request.get_json()

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
        print("Returned assignment")
        return json.dumps(solution)

    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)
        return json.dumps({
            "name": type(error).__name__.__str__(),
            "message": error.__str__(),
        }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
