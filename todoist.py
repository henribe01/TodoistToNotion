import os
from datetime import datetime, timedelta

from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv

load_dotenv()


class Todoist:
    def __init__(self):
        self._api = TodoistAPI(os.getenv("TODOIST_API_KEY"))
        self.last_checked = datetime.now() - timedelta(days=1)

    def get_tasks(self):
        tasks = self._api.get_tasks()
        return [task for task in tasks if
                datetime.strptime(task.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') > self.last_checked]
