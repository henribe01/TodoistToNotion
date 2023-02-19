import os
from datetime import datetime, timedelta

from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from config import get_config

load_dotenv()


class Todoist:
    _api = None

    def __init__(self):
        if Todoist._api is None:
            Todoist._api = TodoistAPI(os.getenv('TODOIST_API_KEY'))
        self._api = Todoist._api

    def get_tasks(self, created_after: datetime = None):
        tasks = self._api.get_tasks()
        if created_after is not None:
            tasks = [task for task in tasks if
                     datetime.strptime(task.created_at, '%Y-%m-%dT%H:%M:%S.%fZ') > created_after]
        return tasks

    def get_tasks_with_tag(self, tag):
        """
        Returns all tasks with specific tag
        :param tag: String of Label in Todoist
        :return: List of tasks
        """
        tasks = self._api.get_tasks()
        return [task for task in tasks if tag in task.labels]
