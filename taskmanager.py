import task_module 
import ttkbootstrap as ttk                                   
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

# Loads tasks.json into variable
task_list = task_module.load_tasks()
settings = task_module.load_settings()

app = ttk.Window('Task Manager', themename=settings['theme'])                 # Theme and app style, change this to change app's theme




def task_update_status(task_id, status):        # Function used to update task status
    task_list[str(task_id)]['status'] = status
    task_module.update_tasks(task_list, task_id)
    t5_stash[str(task_id)].config(text=f' {status}')

def change_name(task_id):                 # Function used to change task's name
    newname = taskname.get()
    task_list[str(task_id)]['description'] = newname
    task_module.update_tasks(task_list, task_id)
    t2_stash[str(task_id)].config(text=task_list[str(task_id)]['description'])

def task_update_interface(task_id):
    global taskname                    # Creates new window for updating task's name
    disable_allbuttons()

    taskname = ttk.StringVar()
    tasup = ttk.Toplevel('Change task name')
    lu1 = ttk.Label(tasup, text='Name: ', font=('arial', 10))
    eu1 = ttk.Entry(tasup, textvariable=taskname, font=('arial', 10))
    bu1 = ttk.Button(tasup, text='✓', bootstyle='success', command=lambda:[change_name(task_id), enable_allbuttons() , refresh(), tasup.destroy()])

    tasup.protocol('WM_DELETE_WINDOW', func=lambda:[enable_allbuttons(), tasup.destroy()])

    lu1.grid(row=0,column=0,sticky=W)
    eu1.grid(row=0, column=1)
    bu1.grid(row=0, column=2)


def refresh():
    for task in t1_stash.keys():
        t1_stash[str(task)].destroy()
        t2_stash[str(task)].destroy()
        t3_stash[str(task)].destroy()
        t4_stash[str(task)].destroy()
        t5_stash[str(task)].destroy()
        b1_stash[str(task)].destroy()
        b2_stash[str(task)].destroy()
        b3_stash[str(task)].destroy()
        b4_stash[str(task)].destroy()
        b5_stash[str(task)].destroy()

    t1_stash.clear()
    t2_stash.clear()
    t3_stash.clear()
    t4_stash.clear()
    t5_stash.clear()
    b1_stash.clear()
    b2_stash.clear()
    b3_stash.clear()
    b4_stash.clear()
    b5_stash.clear()

    show_task()


def delete_task(task_id):                               # Deletes a task based on it's id and refreshes the interface
    del task_list[str(task_id)]
    task_module.update_tasks(task_list, task_id, delete=True)

    refresh()

def delete_confirmation_interface(task_id):
    delwindow = ttk.Toplevel('')
    b4 = b4_stash[str(task_id)]

    delwindow.protocol('WM_DELETE_WINDOW', func=lambda:[enable_allbuttons(), delwindow.destroy()])

    td1 = ttk.Label(delwindow, text= f'Are you sure you want to delete TASK {task_id}?', font=('arial', 12))
    bd1 = ttk.Button(delwindow, text='✓', bootstyle='success', command=lambda:[delete_task(task_id), enable_allbuttons(), delwindow.destroy()])
    bd2 = ttk.Button(delwindow, text='X', bootstyle= 'danger', command=lambda:[enable_allbuttons(), delwindow.destroy()])

    disable_allbuttons()

    td1.grid(row=0, column=0, sticky=W)
    bd1.grid(row=0, column=1)
    bd2.grid(row=0, column=2)

def enable_allbuttons():
    for button in b1_stash.values():
        button.config(state=NORMAL)
    for button in b2_stash.values():
        button.config(state=NORMAL)
    for button in b3_stash.values():
        button.config(state=NORMAL)
    for button in b4_stash.values():
        button.config(state=NORMAL)
    for button in b5_stash.values():
        button.config(state=NORMAL)
    b6.config(state=NORMAL)
    b7.config(state=NORMAL)

def disable_allbuttons():
    for button in b1_stash.values():
        button.config(state=DISABLED)
    for button in b2_stash.values():
        button.config(state=DISABLED)
    for button in b3_stash.values():
        button.config(state=DISABLED)
    for button in b4_stash.values():
        button.config(state=DISABLED)
    for button in b5_stash.values():
        button.config(state=DISABLED)
    b6.config(state=DISABLED)
    b7.config(state=DISABLED)

def add_interface():      # Function for the "NEW TASK" button interface
    row = len(t1_stash) + 1

    disable_allbuttons()

    global aname
    aname = ttk.StringVar()         
    create = ttk.Toplevel('Create a new task')
    lc1 = ttk.Label(create, text='Name: ', font=('arial', 10))
    ec1 = ttk.Entry(create, textvariable=aname, font=('arial', 10))
    bc1 = ttk.Button(create, text='✓', bootstyle='success', command=lambda:[create_task(row, update=True), enable_allbuttons(), create.destroy()])

    create.protocol('WM_DELETE_WINDOW', func=lambda:[enable_allbuttons(), create.destroy()])

    lc1.grid(row=0,column=0,sticky=W)
    ec1.grid(row=0, column=1)
    bc1.grid(row=0, column=2)


def create_task(task_id = task_module.generate_id(task_list), update = False):
    settings = task_module.load_settings()
    if update:
       task_id = task_module.generate_id(task_list)                   # Function that creates tasks on the app's window, if update is set it updates the JSON database.
       new_task = task_module.create_task(task_id, aname.get())
       task_list[str(task_id)] = new_task
       task_module.update_tasks(task_list, task_id)

    t1 = ttk.Label(app, text=f'Task {task_list[str(task_id)]["id"]} - ', font=('arial', 10))
    t2 = ttk.Label(app, text=task_list[str(task_id)]['description'], font=('arial', 10))
    t3 = ttk.Label(app, text=f'|| created: {task_list[str(task_id)]["created"]} last updated: {task_list[str(task_id)]["last updated"]} ||', font=('arial', 10))
    t4 = ttk.Label(app, text=f'status:', font=('arial', 10))
    t5 = ttk.Label(app, text=f' {task_list[str(task_id)]["status"]}', font=('arial', 10))
    b1 = ttk.Button(app, text='DONE', bootstyle='success', command=lambda j=task_list[str(task_id)]['id']:task_update_status(j, 'done'))
    b2 = ttk.Button(app, text='IN PROGRESS', command=lambda j=task_list[str(task_id)]['id']:task_update_status(j, 'in progress'))
    b3 = ttk.Button(app, text='TO DO', bootstyle='warning', command=lambda j=task_list[str(task_id)]['id']:task_update_status(j, 'to do'))
    b4 = ttk.Button(app, text='X', bootstyle='danger', command=lambda j=task_list[str(task_id)]['id']:delete_confirmation_interface(j))
    b5 = ttk.Button(app, text='🖊️', command=lambda j = task_list[str(task_id)]['id']:task_update_interface(j)) 
    
    '''FOR REFERENCE:         T1 - Task and task id label
                              T2 - Task description label
                              T3 - Task "created" and "last updated" label
                              T4 - Task "status" text label
                              T5 - Task actual status label
                              B1 - Task "done" status set button
                              B2 - Task "in progress" status set button
                              B3 - Task "to do" status set button
                              B4 - Task exclusion button
                              B5 - Task edit button'''

    t1_stash[f'{task_list[str(task_id)]['id']}'] = t1        # Store labels and buttons on each stash
    t2_stash[f'{task_list[str(task_id)]['id']}'] = t2
    t3_stash[f'{task_list[str(task_id)]['id']}'] = t3
    t4_stash[f'{task_list[str(task_id)]['id']}'] = t4
    t5_stash[f'{task_list[str(task_id)]['id']}'] = t5
    b1_stash[f'{task_list[str(task_id)]['id']}'] = b1                                    
    b2_stash[f'{task_list[str(task_id)]['id']}'] = b2
    b3_stash[f'{task_list[str(task_id)]['id']}'] = b3
    b4_stash[f'{task_list[str(task_id)]['id']}'] = b4
    b5_stash[f'{task_list[str(task_id)]['id']}'] = b5
    
    
    row = len(t1_stash) + 1           # Grid each label and button on app's window
    t1.grid(row=row, column=0, sticky= W)
    t2.grid(row= row, column= 1, padx= 5)       
    t3.grid(row=row, column= 2)
    t4.grid(row=row, column=3)
    t5.grid(row=row, column=4,)
    b1.grid(row=row, column=5, sticky=E)
    b2.grid(row=row, column=6, sticky=E)
    b3.grid(row=row, column=7, sticky=E)
    b4.grid(row=row, column=9, sticky=E)
    b5.grid(row=row, column=8, sticky=E)
    b6.grid(row=row+1, column= 1)
    b7.grid(row= row+1, column= 2)
    if settings['show'] == 0:
        b7.config(text='SHOW')
        hide_dates()

def show_task():                            # Function for creating tasks on the app's window
    for task in task_list.values():     
        create_task(task_id=task['id'])
    if task_list == {}:
        b6.grid(row=0, column=0)
        b7.grid(row=0, column=1)


def hide_dates():
    for label in t3_stash.values():
        label.grid_forget()
        b7.grid(row= len(t1_stash)+2, column= 3)


def show_hide():
    settings = task_module.load_settings()
    theme = settings['theme']
    if settings['show'] == 0:
        for label in t3_stash.values():
            for c in range(len(t1_stash.values())):
                label.grid(row= c, column= 2)
        new ={
                "theme" : theme,
                "show" : 1
        }
        b7.config(text='HIDE')
        task_module.update_settings(new)
        
        refresh()
    if settings['show'] == 1:
        hide_dates()
        new = {
            "theme" : theme,
            "show" : 0
                }
        b7.config(text='SHOW')
        task_module.update_settings(new)

t1_stash = {}          # Label and button stashes for storing each label and button individually
t2_stash = {}
t3_stash = {}
t4_stash = {}
t5_stash = {}
b1_stash = {}
b2_stash = {}
b3_stash = {}
b4_stash = {}
b5_stash = {}


b6 = ttk.Button(app, text='NEW TASK', bootstyle='success', command=lambda:add_interface(), width= 25)            # B6 - "NEW TASK" Button
b7 = ttk.Button(app, text='HIDE', bootstyle='light', command=show_hide)

show_task()

app.resizable(width=False, height=False)
app.mainloop()
