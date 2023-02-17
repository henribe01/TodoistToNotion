import requests
import os

api_url = 'https://api.notion.com/v1/pages'

headers = {'Authorization': f'Bearer {os.getenv("NOTION_API_KEY")}',
           'Content-Type': 'application/json',
           'Notion-Version': '2021-08-16'}

data = {
    "parent": {'type': 'database_id',
               "database_id": os.getenv("NOTION_DATABASE_ID")},
    "properties": {"Name": {"title": [{"text": {"content": "Test"}}]}}}

response = requests.post(api_url, headers=headers, json=data)
print(response.json())
