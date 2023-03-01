import requests
import os

from dotenv import load_dotenv

load_dotenv()


class Notion:
    api_url = 'https://api.notion.com/v1/'
    headers = {'Authorization': f'Bearer {os.getenv("NOTION_API_KEY")}',
               'accept': 'application/json',
               'Notion-Version': '2022-06-28'}

    def __init__(self, database_id):
        self.database_id = database_id
        self.database = self.get_database()
        self.data = {"parent": {'type': 'database_id',
                                "database_id": database_id}}

    def get_database(self):
        return requests.get(f'{Notion.api_url}databases/{self.database_id}', headers=Notion.headers).json()

    def create_property(self, **kwargs):
        """
        Creates a dict in the format of properties for the Notion API
        :param kwargs: Format 'NotionColumnName=Value'
        :return: Properties Dict
        """
        properties = {}
        for name, value in kwargs.items():
            # Check if the Column is in the database
            if name not in self.database['properties'].keys():
                # TODO: Add logging
                pass
            prop_type = self.database['properties'][name]['type']
            property = {'type': prop_type, prop_type: None}
            match prop_type:
                case "checkbox":
                    if type(value) != bool:
                        # TODO: add Error
                        pass
                    property[prop_type] = value
                case "date":
                    property[prop_type] = {'start': value}
                case "multi_select":
                    property[prop_type] = [{'name': tag} for tag in value]
                case "number":
                    property[prop_type] = value
                case "select":
                    property[prop_type] = {'name': value}
                case "title":
                    property[prop_type] = [{'type': 'text', 'text': {'content': value}}]
                case "rich_text":
                    property[prop_type] = [{'type': 'text', 'text': {'content': value}}]
                # TODO: Add case for relation
            properties[name] = property
        return properties

    def create_page(self, properties):
        """
        Creates a page in the Database
        :param properties: Dictonary of the properties
        :return: Response from the API
        """
        data = self.data
        data['properties'] = properties
        return requests.post(f'{Notion.api_url}pages', headers=Notion.headers, json=data).json()

    def get_pages(self):
        # TODO: Add filter
        return requests.post(f'{Notion.api_url}databases/{self.database_id}/query', headers=Notion.headers).json()


notion = Notion(os.getenv('NOTION_DB_ID'))
properties = notion.create_property(Name='test', Datum='2023-02-24', Tags=['Uni', 'test123'],
                                    TodoistID='8123887asdj')
print(notion.get_pages()['results'][0])