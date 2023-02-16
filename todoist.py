import os
from datetime import datetime, timedelta

from todoist_api_python.api import TodoistAPI

TODOIST_API_TOKEN = "be64b8e7feac98c72d350c18cd3f9d02289d2164"

api = TodoistAPI(TODOIST_API_TOKEN)

last_checked = datetime.now() - timedelta(days=1)


def get_tasks_since_last_checked():
    tasks = api.get_tasks()
    return [task for task in tasks if datetime.strptime(task.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') > last_checked]

