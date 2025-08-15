"""
Functions and variables for taskmanager.py
"""

import os
import json
from datetime import datetime

# Arguments for "tm list" command
TM_LIST_ARGS = ['todo', 'in-progress', 'done', '--extend']

GENERIC_ERROR_MSG = 'Invalid input inserted. Please type "tm help" (no quotes) for more information.'
GENERIC_ARGS_ERROR_MSG = 'Invalid argument combination inserted. Please type "tm help list" (no quotes) for more information.'

def dynamic_error_msg(inv_arg, command) -> str:
    """
    Builds a custom error message
    """
    msg = ''
    if inv_arg:
        msg += f'Invalid argument "{inv_arg}" inserted.'
    else:
        msg += f'Argument(s) expected after "{command}".'
    if command:
        msg += f' Please type "tm help {command}" (no quotes) for more information.'
    else:
        msg += f' Please type "tm help" (no quotes) for more information.'
    return msg

def generate_id(task_list) -> int:
    """
    Finds the next unique ID that can be assigned to a task, given the task list
    """
    if task_list:
        return max(tuple(map(lambda a: int(a), task_list.keys()))) + 1
    return 1

def check_id(task_list, task_id, case) -> bool:
    """
    Checks if there exists a task, given a task list and ID.
    Also, displays an error message in case the task doesn't exist.
    """
    if str(task_id) not in task_list.keys():  # Triggers when "task_id" is invalid
        print(dynamic_error_msg(task_id, case))
        return False
    return True

def format_task(task, priority=None, extended=False) -> str | bool:
    """
    Returns task with custom formatting
    """
    msg = ''

    match priority: # Only tasks with the given priority will be formatted
        case 'todo':
            if task['status'] != 'to do': return False
        case 'in-progress':
            if task['status'] != 'in progress': return False
        case 'done':
            if task['status'] != 'done': return False
        case _:
            msg += f'({task["status"]}) '

    msg += f'Task no. {task["id"]}: {task["description"]}'

    if extended:
        msg += f'\nCREATED: {task["created"]}; LAST UPDATED: {task["last updated"]}'
    return msg

def now() -> str:
    """
    Shows actual date and time. Formats to "YYYY-MM-DD hh-mm"
    """
    return str(datetime.now().isoformat(sep=" ", timespec="minutes"))

def create_task(identification, description) -> dict:
    """
    Creates a task (no shit Sherlock)
    """
    return {
        'id': identification,
        'description': description,
        'status': 'to do',
        'created': now(),
        'last updated': now(),
    }

def load_tasks() -> dict:
    """
    Loads tasks.json into a dictionary
    """
    try:
        with open('task_storage/tasks.json', 'r') as tasks_file:
            return json.load(tasks_file)
    except json.JSONDecodeError: # Triggers when "tasks.json" file is written irregularly
        os.remove('task_storage/tasks.json')
        null = {}
        with open('task_storage/tasks.json', 'w') as tasks_file:
            json.dump(null, tasks_file)
        with open('task_storage/tasks.json', 'r') as tasks_file:
            return json.load(tasks_file)

    except FileNotFoundError: # Triggers when the script can't find "tasks.json" file
        dir = 'task_storage'
        if not os.path.isdir(dir):
            os.mkdir(dir)
        null = {}
        with open('task_storage/tasks.json', 'w') as tasks_file:
            json.dump(null, tasks_file)
        with open('task_storage/tasks.json', 'r') as tasks_file:
            return json.load(tasks_file)

def load_settings() -> dict:
    '''
    Loads settings.json into a dictionary    
    '''
    try:
        with open('task_storage/settings.json', 'r') as tasks_settings:
            return json.load(tasks_settings)
    except json.JSONDecodeError: # Triggers when "tasks.json" file is written irregularly
        os.remove('task_storage/settings.json')
        settings = {
            "theme" : "cyborg",
            "show" : 1
        }
        with open('task_storage/settings.json', 'w') as tasks_settings:
            json.dump(settings, tasks_settings)
        with open('task_storage/settings.json', 'r') as tasks_settings:
            return json.load(tasks_settings)

    except FileNotFoundError: # Triggers when the script can't find "tasks.json" file
        dir = 'task_storage'
        if not os.path.isdir(dir):
            os.mkdir(dir)
        settings = {
            "theme" : "cyborg",
            "show" : 1
        }
        with open('task_storage/settings.json', 'w') as tasks_settings:
            json.dump(settings, tasks_settings)
        with open('task_storage/settings.json', 'r') as tasks_settings:
            return json.load(tasks_settings)

def update_tasks(task_list, task_id, delete=False) -> None:
    """
    Updates the tasks.json file
    """
    with open('task_storage/tasks.json', 'w') as tasks_file:
        if not delete: # Updates 'last updated' key of task if you won't delete it
            task_list[str(task_id)]['last updated'] = now()
        json.dump(task_list, tasks_file)

def update_settings(new) -> None:
    with open('task_storage/settings.json', 'w') as settings_file:
        json.dump(new, settings_file)

