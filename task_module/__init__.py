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

# ATTENTION!! BORING ASS DOCUMENTATION AHEAD

TM_LINE_LENGTH = 105

TM_HELP_GENERIC = f"""
{"=" * TM_LINE_LENGTH}
{"TASK   MANAGER   HELP":^{TM_LINE_LENGTH}}
{"=" * TM_LINE_LENGTH}
{"-" * TM_LINE_LENGTH}
CLI commands should always start with "tm" (short for task manager)
{"-" * TM_LINE_LENGTH}
Following are the currently accepted task manager commands:

{"help - Shows this help message":.<80}{'(optional arguments)':.>25}

{"add - Adds a task to the task list":.<80}{"(mandatory arguments)":.>25}

{"update - Updates a task on the task list":.<80}{"(mandatory arguments)":.>25}

{'mark-in-progress - Marks a task in the task list as "in-progress"':.<80}{"(mandatory arguments)":.>25}

{'mark-done - Marks a task in the task list as "done"':.<80}{"(mandatory arguments)":.>25}

{"list - Shows the task list":.<80}{'(optional arguments)':.>25}

{"delete - Removes a task from the task list":.<80}{"(mandatory arguments)":.>25}

{"exit - Exits the program":.<80}{'(no arguments)':.>25}

You may type in "tm help command" (no quotes) for more specific information on that command
"""

TM_HELP_DOCS = {
    'help':
"""
HELP ON "HELP" COMMAND

Shows informations about commands

tm help -> Shows generic help page

tm help <command> -> Shows page dedicated to command

(optional) <command> needs to be a valid task manager command
""",
    'add':
"""
HELP ON "ADD" COMMAND

Adds a task to the task list

tm add <task_description> -> Adds a task with given task description to the task list

(mandatory) <task_description> may be anything the user can type, must be quoted if there are any blank spaces
""",
    'update':
"""
HELP ON "UPDATE" COMMAND

Updates a task on the task list

tm update <task_id> <task_description> -> Updates task description, given its ID, with a new description

(mandatory) <task_id> numeric value, ID of task the user wishes to update

(mandatory) <task_description> may be anything the user can type, must be quoted if there are any blank spaces
""",
    'mark-in-progress':
"""
HELP ON "MARK-IN-PROGRESS" COMMAND

Marks a task in the task list as "in-progress"

tm mark-in-progress <task_id> -> Updates task status as "in progress", given its ID

(mandatory) <task_id> numeric value, ID of task the user wishes to mark
""",
    'mark-done':
"""
HELP ON "MARK-DONE" COMMAND

Marks a task in the task list as "done"

tm mark-in-progress <task_id> -> Updates task status as "done", given its ID

(mandatory) <task_id> numeric value, ID of task the user wishes to mark
""",
    'list':
"""
HELP ON "LIST" COMMAND

Shows the task list

tm list -> Shows a shallow version of the task list, as tasks will display the following information:

status: may be "to do", "in progress", "done"
identification: numeric value associated to the task
description: content of the task, specified by the user

the shallow task template go as follows:

(<status>) Task no. <identification>: <description>

tm list <args> -> Shows altered versions of the task list, depending on inserted arguments

(optional) <args> Could be:

todo: task list will only show tasks with "to do" status

in-progress: task list will only show tasks with "in-progress" status

done: task list will only show tasks with "done" status

!!!Out of "todo", "in-progress", "done", only one can be choosen, otherwise an error will occur!!!

--extend: task list will show extra information about tasks, which are:

created: when was the task created
last updated: when was the task last updated (defaults to creation date upon creation)

the extended task template go as follows ->

(<status>) Task no. <identification>: <description>
CREATED: <created>; LAST UPDATED: <last updated>
""",
    'delete':
"""
HELP ON "DELETE" COMMAND

Removes a task from the task list

tm delete <task_id> -> Removes a task from the task list, given its ID

<task_id> numeric value, ID of task the user wishes to delete
""",
    'exit':
"""
HELP ON "EXIT" COMMAND

Exits the program

tm exit -> What do you think will happen?

this command doesn't accept any extra arguments and will always fail if fed any
""",
}
