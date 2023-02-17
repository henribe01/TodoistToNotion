import os
from datetime import datetime, timedelta

from todoist_api_python.api import TodoistAPI

api = TodoistAPI(os.getenv('TODOIST_API_KEY'))

last_checked = datetime.now() - timedelta(days=1)


def get_tasks_since_last_checked():
    tasks = api.get_tasks()
    return [task for task in tasks if datetime.strptime(task.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') > last_checked]

print(get_tasks_since_last_checked())