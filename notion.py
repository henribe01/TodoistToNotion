import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = 'https://api.notion.com/v1/'

headers = {'Authorization': f'Bearer {os.getenv("NOTION_API_KEY")}',
           'accept': 'application/json',
           'Notion-Version': '2022-06-28'}

data = {"parent": {'type': 'database_id',
                   "database_id": os.getenv('NOTION_DB_ID')}}


class Notion:
    def __init__(self, database_id):
        self.database_id = database_id
        self.database = self.get_database()

    def get_database(self):
        return requests.get(api_url + 'databases/' + self.database_id, headers=headers).json()

    def create_property(self, **kwargs):
        """
        Creates a property object
        :param kwargs: Should be of form "name": "value"
        :return: A dictonary of properties
        """
        # Makes a copy of the properties of the database if it is in kwargs
        properties = {key: value for key, value in self.database['properties'].items() if key in kwargs}
        for key, value in properties.items():
            # Deletes the name because notion doesn't like it
            del properties[key]['name']
            type = properties[key]['type']
            if type in ['select', 'multi_select']:
                # Handles the select and multi_select types
                selected_option = [option for option in properties[key][type]['options'] if
                                   option['name'] == kwargs[key] or option['name'] in kwargs[key]]
                if type == 'select':
                    properties[key][type] = selected_option[0]
                elif type == 'multi_select':
                    properties[key][type] = selected_option
            elif type == 'title':
                properties[key][type] = [{'text': {'content': kwargs[key]}}]
            elif type == 'date':
                properties[key][type] = {'start': kwargs[key]}
            elif type == 'rich_text':
                properties[key][type] = [{'type': 'text', 'text': {'content': kwargs[key]}}]
            else:
                properties[key][type] = kwargs[key]
        return properties

    def create_page(self, properties):
        """
        Creates a page in the database
        :return: The response from the API
        """
        data['properties'] = properties
        return requests.post(api_url + 'pages', headers=headers, json=data).json()

    def get_pages(self, **kwargs):
        """
        Gets all the pages from the database
        :param kwargs: filters (name of property: condition(dict))
        :return: A list of pages
        """
        # TODO: Change so that it can handle multiple filters
        filters = {'and': [], 'or': []}
        for key, value in kwargs.items():
            type = self.database['properties'][key]['type']
            filters['and'].append({'property': key, type: value})
        return requests.post(api_url + f'databases/{self.database_id}/query', headers=headers,
                             json={'filter': filters}).json()['results']

# notion = Notion(os.getenv('NOTION_DB_ID'))
# property = notion.create_property(Name='Test', Datum='2021-12-31', Fach='Numerik', Tags=['Uni', 'Heute'])
# print(notion.get_pages(Tags={'contains': 'Heute'}))
