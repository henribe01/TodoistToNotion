from datetime import datetime

from dotenv import load_dotenv
from todoist import Todoist
from config import get_config

if __name__ == '__main__':
    load_dotenv()
    todoist = Todoist()
    config = get_config()
    tasks = todoist.get_tasks(datetime.strptime(config['LAST_SYNCED'], '%Y-%m-%d %H:%M:%S.%f'))
    print(tasks)