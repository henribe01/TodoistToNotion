import os
from datetime import datetime

from dotenv import load_dotenv
from todoist import Todoist
from config import get_config
from notion import Notion


def sync_todays_tasks(todoist: Todoist, notion: Notion):
    todays_task = todoist.get_tasks_with_tag('heute')
    synced_tasks_notion = notion.get_pages(Tags={'contains': 'Heute'})
    synced_tasks_ids = [task['properties']['TodoistID']['rich_text'][0]['text']['content'] for task in
                        synced_tasks_notion]
    for task in todays_task:
        print(task)
        if task.id not in synced_tasks_ids:
            property = notion.create_property(Name=task.content, Datum=task.due.date, Tags=['Heute'], TodoistID=task.id)
            notion.create_page(property)


if __name__ == '__main__':
    load_dotenv()
    todoist = Todoist()
    notion = Notion(os.getenv('NOTION_DB_ID'))
    config = get_config()
    sync_todays_tasks(todoist, notion)
