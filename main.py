import os
from datetime import datetime

from dotenv import load_dotenv
from todoist import Todoist
from config import get_config, write_config
from notion import Notion


# TODO: Instead of creating new task when tag, add tag to existing task in notion
def sync_todays_tasks(todoist: Todoist, notion: Notion):
    todays_task = todoist.get_tasks_with_tag('heute')
    synced_tasks_notion = notion.get_pages(Tags={'contains': 'Heute'})
    synced_tasks_ids = [task['properties']['TodoistID']['rich_text'][0]['text']['content'] for task in
                        synced_tasks_notion]
    for task in todays_task:
        if task.id not in synced_tasks_ids:
            property = notion.create_property(Name=task.content, Datum=task.due.date, Tags=['Heute'], TodoistID=task.id)
            notion.create_page(property)
    for task in synced_tasks_notion:
        print(task)


def sync_tasks(todoist: Todoist, notion: Notion):
    config = get_config()
    last_sync = config['DEFAULT']['LAST_SYNCED']

    # Get all tasks since last sync
    tasks = todoist.get_tasks(filter=f'created after: {last_sync}')

    # Get all notion tasks and create a list of all their todoist ids
    pages = notion.get_pages()
    pages_todoist_ids = [page['properties']['TodoistID']['rich_text'][0]['text']['content'] for page in pages]
    print(pages_todoist_ids)
    print(tasks)
    for task in tasks:
        if task.id not in pages_todoist_ids:
            if task.due is None:
                properties = notion.create_property(Name=task.content, TodoistID=task.id)
            else:
                properties = notion.create_property(Name=task.content, TodoistID=task.id, Datum=task.due.date)
            print(properties)
            print(notion.create_page(properties))

    # Refresh the Last synced date in the config
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
    #config['DEFAULT']['LAST_SYNCED'] = now
    #write_config(config)


if __name__ == '__main__':
    load_dotenv()
    todoist = Todoist()
    notion = Notion(os.getenv('NOTION_DB_ID'))
    sync_tasks(todoist, notion)
