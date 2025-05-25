"""
Run this file to open Task Manager
"""

import task_module
from shlex import split
from functools import partial

# Loads tasks.json into variable
task_list = task_module.load_tasks()

print('Welcome to Task Manager')

# User may exit program by typing "tm exit"
while True:

    # Transforms user's input into a list (preserves blank spaces between quotes)
    user_input = split(input())

    try:
        if user_input[0] == 'tm': # Every command should start with "tm" (task manager)
            match user_input[1]:

                case 'help':
                    try:
                        command = user_input[2]
                        print(task_module.TM_HELP_DOCS[command])
                    except IndexError:
                        print(task_module.TM_HELP_GENERIC)

                case 'add': # Adds a new task to "task_list"
                    try:
                        task_id = task_module.generate_id(task_list)
                        new_task = task_module.create_task(task_id, user_input[2])
                        task_list[str(task_id)] = new_task
                        task_module.update_tasks(task_list, task_id)

                        print(f'Task no. {task_id} added successfully')

                    except IndexError: # Triggers when "user_input[2]" doesn't exist
                        print(task_module.dynamic_error_msg(None, 'add'))

                case 'update': # Updates task description
                    try:
                        task_id = user_input[2]

                        # Exits 'update' clause if "task_id" is invalid
                        if not task_module.check_id(task_list, task_id, 'update'): continue

                        task_list[str(task_id)]['description'] = user_input[3]
                        task_module.update_tasks(task_list, task_id)

                        print(f'Task no. {task_id} updated succesfully')

                    except IndexError: # Triggers when "user_input[2]" or "user_input[3]" don't exist
                        print(task_module.dynamic_error_msg(None, 'update'))

                case 'mark-in-progress': # Marks task status as "in progress"
                    try:
                        task_id = user_input[2]

                        # Exits 'mark-in-progress' clause if "task_id" is invalid
                        if not task_module.check_id(task_list, task_id, 'mark-in-progress'): continue

                        task_list[str(task_id)]["status"] = "in progress"
                        task_module.update_tasks(task_list, task_id)

                        print(f'Task no. {task_id} marked as "in progress"')

                    except IndexError: # Triggers when "user_input[2]" doesn't exist
                        print(task_module.dynamic_error_msg(None, 'mark-in-progress'))

                case 'mark-done': # Marks task status as "done"
                    try:
                        task_id = user_input[2]

                        # Exits 'mark-done' clause if "task_id" is invalid
                        if not task_module.check_id(task_list, task_id, 'mark-done'): continue

                        task_list[str(task_id)]["status"] = "done"
                        task_module.update_tasks(task_list, task_id)

                        print(f'Task no. {task_id} marked as "done"')

                    except IndexError: # Triggers when "user_input[2]" doesn't exist
                        print(task_module.dynamic_error_msg(None, 'mark-done'))

                case 'list': # Shows organized list of tasks
                    args = user_input[2:] # Optional arguments
                    format_task = task_module.format_task # Original "format_task" function

                    for argument in args: # Interprets optional arguments
                        if argument in task_module.TM_LIST_ARGS: # Argument must be on list of arguments
                            match argument: # Arguments will shape formatting function behavior

                                case 'todo' | 'in-progress' | 'done': # Function will only show tasks with given status
                                    if args.count('todo') + args.count('in-progress') + args.count('done') == 1:
                                        for status in ('todo', 'in-progress', 'done'):
                                            if argument == status:
                                                format_task = partial(format_task, priority=status)
                                    else:
                                        print(task_module.GENERIC_ARGS_ERROR_MSG)
                                        break # Exits loop if argument is not unique

                                case '--extend': # Function will also show creation and update dates of tasks
                                    if args.count('--extend') == 1:
                                        format_task = partial(format_task, extended=True)
                                    else:
                                        print(task_module.GENERIC_ARGS_ERROR_MSG)
                                        break # Exits loop if argument is not unique

                        else:
                            print(task_module.dynamic_error_msg(argument, 'list'))
                            break # Exits loop if argument is not in the list of arguments

                    else: # Triggers when valid arguments are inserted
                        print()
                        empty = True
                        for task in task_list.values():
                            if format_task(task): # Ignores tasks that were not prioritized
                                empty = False
                                print(format_task(task), end='\n\n') # Prints task with defined formatting
                        if empty: # Triggers if no task gets printed
                            print('There are no such tasks\n')

                case 'delete': # Removes a task from "task_list"
                    try:
                        task_id = user_input[2]

                        # Exits 'delete' clause if "task_id" is invalid
                        if not task_module.check_id(task_list, task_id, 'delete'): continue

                        del task_list[str(task_id)]
                        task_module.update_tasks(task_list, task_id, delete=True)

                        print(f'Task no. {task_id} deleted succesfully')

                    except IndexError: # Triggers when "user_input[2]" doesn't exist
                        print(task_module.dynamic_error_msg(None, 'delete'))

                case 'exit': # Exits the program (who would've thought)
                    raise SystemExit('See you next time ;)')

                case _: # Triggers when second argument is invalid
                    print(task_module.dynamic_error_msg(user_input[1], None))

        else: # Same as (if user_input[0] != 'tm')
            print(task_module.dynamic_error_msg(user_input[0], None))

    except IndexError: # Triggers when "user_input[0]" or "user_input[1]" don't exist
        print(task_module.GENERIC_ERROR_MSG)
