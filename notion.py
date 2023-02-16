import requests

NOTION_API_KEY = "secret_vpMRoyOOMXfLtLAaCgJR3aedaOxNPTUAGTgWOsR1g5w"
NOTION_DB_ID = "875e14773c4341af94d5b5023675a8c6"

api_url = 'https://api.notion.com/v1/pages'

headers = {'Authorization': f'Bearer {NOTION_API_KEY}',
           'Content-Type': 'application/json',
           'Notion-Version': '2021-08-16'}

data = {
    "parent": {'type': 'database_id',
               "database_id": NOTION_DB_ID},
    "properties": {"Name": {"title": [{"text": {"content": "Test"}}]}}}

response = requests.post(api_url, headers=headers, json=data)
print(response.json())
