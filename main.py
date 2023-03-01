import os
from datetime import datetime

from dotenv import load_dotenv
from todoist import Todoist
from config import get_config, write_config
from notion import Notion


def sync_tasks(todoist, notion):
    config = get_config()
    last_sync = config['DEFAULT']['LAST_SYNCED']
    todoist_tasks = todoist.get_tasks()
    for task in todoist_tasks:
        if task.due:
            property = notion.create_property(Name=task.content, Datum=task.due.date, Tags=task.labels,
                                              TodoistID=task.id)
        else:
            property = notion.create_property(Name=task.content, Tags=task.labels,
                                              TodoistID=task.id)
        print(property)


if __name__ == '__main__':
    load_dotenv()
    todoist = Todoist()
    notion = Notion(os.getenv('NOTION_DB_ID'))
    sync_tasks(todoist, notion)
