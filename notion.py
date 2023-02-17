import requests
import os
from dotenv import load_dotenv

api_url = 'https://api.notion.com/v1/pages'

headers = {'Authorization': f'Bearer {os.getenv("NOTION_API_KEY")}',
           'Content-Type': 'application/json',
           'Notion-Version': '2021-08-16'}

data = {
    "parent": {'type': 'database_id',
               "database_id": os.getenv('NOTION_DB_ID')}}


def add_task(title, due_date=None, tags=None, subject=None):
    data['properties'] = {'Name':
                              {'type': 'title',
                               'title': [{'type': 'text', 'text': {'content': title}}]}}
    if due_date:
        data['properties']['Datum'] = {'type': 'date', 'date': {'start': due_date}}
    if tags:
        data['properties']['Tags'] = {'type': 'multi_select', 'multi_select': [{'name': tag} for tag in tags]}
    if subject:
        data['properties']['Fach'] = {'type': 'select', 'select': {'name': subject}}
    response = requests.post(api_url, headers=headers, json=data)
