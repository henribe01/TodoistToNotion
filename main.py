from dotenv import load_dotenv
from todoist import Todoist
from notion import add_task

if __name__ == '__main__':
    load_dotenv()
    todoist = Todoist()
    tasks = todoist.get_tasks()
    for task in tasks:
        due = None
        if task.due:
            due = task.due.date
        add_task(task.content, due, task.labels)

