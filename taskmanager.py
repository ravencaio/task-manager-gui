import task_module 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

app = ttk.Window('Task Manager')                                                   
style = Style('solar')               # Theme and app style, change this to change app's theme

# Loads tasks.json into variable
task_list = task_module.load_tasks()

def task_update_status(task_id, status):        # Function used to update task status
    task_list[str(task_id)]['status'] = status
    task_module.update_tasks(task_list, task_id)
    print(f'atualizou task {task_id} com status de {status}')
    t5_stash[str(task_id)].config(text=f' {status}')

def change_name(task_id):                 # Function used to change task's name
    newname = taskname.get()
    task_list[str(task_id)]['description'] = newname
    task_module.update_tasks(task_list, task_id)
    t2_stash[str(task_id)].config(text=task_list[str(task_id)]['description'])

def task_update_interface(task_id):
    global taskname                     # Creates new window for updating task's name
    taskname = ttk.StringVar()
    tasup = ttk.Toplevel('Change task name')
    lu1 = ttk.Label(tasup, text='Name: ', font=('arial', 10))
    eu1 = ttk.Entry(tasup, textvariable=taskname, font=('arial', 10))
    bu1 = ttk.Button(tasup, text='✓', bootstyle='success', command=lambda:[tasup.destroy(), change_name(task_id)])

    lu1.grid(row=0,column=0,sticky=W)
    eu1.grid(row=0, column=1)
    bu1.grid(row=0, column=2)

def delete_task(task_id):                               # Deletes a task based on it's id and refreshes the interface
    del task_list[str(task_id)]
    task_module.update_tasks(task_list, task_id, delete=True)

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

def create_task(task_id = task_module.generate_id(task_list), update = False):
    if update:
       task_id = task_module.generate_id(task_list)                   # Function that creates tasks on the app's window, if update is set it updates the JSON database.
       new_task = task_module.create_task(task_id, aname.get())
       task_list[str(task_id)] = new_task
       task_module.update_tasks(task_list, task_id)
'''FOR REFERENCE:             T1 - Task and task id label
                              T2 - Task description label
                              T3 - Task "created" and "last updated" label
                              T4 - Task "status" text label
                              T5 - Task actual status label
                              B1 - Task "done" status set button
                              B2 - Task "in progress" status set button
                              B3 - Task "to do" status set button
                              B4 - Task exclusion button
                              B5 - Task edit button
'''                              
    t1 = ttk.Label(app, text=f'Task {task_list[str(task_id)]['id']} - ', font=('arial', 10))
    t2 = ttk.Label(app, text=task_list[str(task_id)]['description'], font=('arial', 10))
    t3 = ttk.Label(app, text=f'- created: {task_list[str(task_id)]['created']} last updated: {task_list[str(task_id)]['last updated']} ', font=('arial', 10))
    t4 = ttk.Label(app, text=f'status:', font=('arial', 10))
    t5 = ttk.Label(app, text=f' {task_list[str(task_id)]['status']}', font=('arial', 10))
    b1 = ttk.Button(app, text='DONE', bootstyle='success', command=lambda j=task_list[str(task_id)]['id']:task_update_status(j, 'done'))
    b2 = ttk.Button(app, text='IN PROGRESS', command=lambda j=task_list[str(task_id)]['id']:task_update_status(j, 'in progress'))
    b3 = ttk.Button(app, text='TO DO', bootstyle='warning', command=lambda j=task_list[str(task_id)]['id']:task_update_status(j, 'to do'))
    b4 = ttk.Button(app, text='X', bootstyle='danger', command=lambda j=task_list[str(task_id)]['id']:[delete_task(j), print(t1_stash.keys())])
    b5 = ttk.Button(app, text='🖊️', command=lambda j = task_list[str(task_id)]['id']:task_update_interface(j))  

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

def show_task():                            # Function for creating tasks on the app's window
    for task in task_list.values():     
        create_task(task_id=task['id'])

def add_interface():      # Function for the "NEW TASK" button interface
    global aname
    aname = ttk.StringVar()         
    create = ttk.Toplevel('Create a new task')
    lc1 = ttk.Label(create, text='Name: ', font=('arial', 10))
    ec1 = ttk.Entry(create, textvariable=aname, font=('arial', 10))
    bc1 = ttk.Button(create, text='✓', bootstyle='success', command=lambda:[create_task(row, update=True), create.destroy()])

    lc1.grid(row=0,column=0,sticky=W)
    ec1.grid(row=0, column=1)
    bc1.grid(row=0, column=2)


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

row = len(t1_stash.keys())+1
b6 = ttk.Button(app, text='NEW TASK', bootstyle='success', command=lambda:add_interface(), width= 25)            # B6 - "NEW TASK" Button
b6.grid(row=row+1, column= 1)

show_task()
    

app.resizable(width=False, height=False)
app.mainloop()
