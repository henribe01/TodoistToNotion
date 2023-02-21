import os
from datetime import datetime, timedelta

from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from config import get_config

load_dotenv()


class Todoist:
    # TODO: Add error handling
    # TODO: Add function that checks if a task with "Heute" tag is finished and deletes the tag in todoist
    _api = None

    def __init__(self):
        if Todoist._api is None:
            Todoist._api = TodoistAPI(os.getenv('TODOIST_API_KEY'))
        self._api = Todoist._api

    def get_tasks(self, project_id=None, label=None, filter=None):
        """
        Gets all filtered tasks
        :param project_id: Filter by Project_id
        :param label: Filter by label
        :param filter: Filters in format (https://todoist.com/help/articles/introduction-to-filters)
        :return: List of Task objects
        """
        return self._api.get_tasks(filter=filter)

    def get_tasks_with_tag(self, tag):
        """
        Returns all tasks with specific tag
        :param tag: String of Label in Todoist
        :return: List of tasks
        """
        # TODO: Rewrite using get_tasks and label as parameter
        tasks = self._api.get_tasks()
        return [task for task in tasks if tag in task.labels]

    def get_project_from_id(self, project_id):
        """
        Passing project id while give the project
        :return:
        """
        # TODO: Get project from id
        pass
