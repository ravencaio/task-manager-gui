import task_module
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style

app = ttk.Window('Task Manager')
#app.geometry('842x600')
style = Style('solar')

# Loads tasks.json into variable
task_list = task_module.load_tasks()


def task_update(task_id, status):
    task_list[str(task_id)]['status'] = status
    task_module.update_tasks(task_list, task_id)
    print(f'atualizou task {task_id} com status de {status}')
    stat[str(task_id)].config(text=f' {status}')

def delete_task(task_id):
    del task_list[str(task_id)]
    task_module.update_tasks(task_list, task_id, delete=True)
    t_stash[str(task_id)].destroy()
    t2_stash[str(task_id)].destroy()
    t3_stash[str(task_id)].destroy()
    t4_stash[str(task_id)].destroy()
    stat[str(task_id)].destroy()
    b1_stash[str(task_id)].destroy()
    b2_stash[str(task_id)].destroy()
    b3_stash[str(task_id)].destroy()
    b4_stash[str(task_id)].destroy()

    del t_stash[str(task_id)]
    del t2_stash[str(task_id)]
    del t3_stash[str(task_id)]
    del t4_stash[str(task_id)]
    del stat[str(task_id)]
    del b1_stash[str(task_id)]
    del b2_stash[str(task_id)]
    del b3_stash[str(task_id)]
    del b4_stash[str(task_id)]




def create_task():
    row = len(t_stash.keys()) + 1
    task_id = task_module.generate_id(task_list)
    new_task = task_module.create_task(task_id, aname.get())
    task_list[str(task_id)] = new_task
    task_module.update_tasks(task_list, task_id)
    print('criou task')
    t = ttk.Label(app, text=f'Task {task_list[str(task_id)]['id']} - ', font=('arial', 10))
    t2 = ttk.Label(app, text=task_list[str(task_id)]['description'], font=('arial', 10))
    t3 = ttk.Label(app, text=f'- created: {task_list[str(task_id)]['created']} last updated: {task_list[str(task_id)]['last updated']} ', font=('arial', 10))
    t4 = ttk.Label(app, text=f'status:', font=('arial', 10))
    t5 = ttk.Label(app, text=f' {task_list[str(task_id)]['status']}', font=('arial', 10))
    b1 = ttk.Button(app, text='DONE', bootstyle='success', command=lambda j=task_list[str(task_id)]['id']:task_update(j, 'done'))
    b2 = ttk.Button(app, text='IN PROGRESS', command=lambda j=task_list[str(task_id)]['id']:task_update(j, 'in progress'))
    b3 = ttk.Button(app, text='TO DO', bootstyle='warning', command=lambda j=task_list[str(task_id)]['id']:task_update(j, 'to do'))
    b4 = ttk.Button(app, text='X', bootstyle='danger', command=lambda j=task_list[str(task_id)]['id']:[delete_task(j)])
        
    t_stash[f'{task_list[str(task_id)]['id']}'] = t
    t2_stash[f'{task_list[str(task_id)]['id']}'] = t2
    t3_stash[f'{task_list[str(task_id)]['id']}'] = t3
    t4_stash[f'{task_list[str(task_id)]['id']}'] = t4
    b1_stash[f'{task_list[str(task_id)]['id']}'] = b1
    b2_stash[f'{task_list[str(task_id)]['id']}'] = b2
    b3_stash[f'{task_list[str(task_id)]['id']}'] = b3
    b4_stash[f'{task_list[str(task_id)]['id']}'] = b4
    stat[f'{task_list[str(task_id)]['id']}'] = t5

    t.grid(row=row, column=0, sticky= W)
    t2.grid(row= row, column= 1, padx= 5)
    t3.grid(row=row, column= 2)
    t4.grid(row=row, column=3)
    t5.grid(row=row, column=4, padx= 5)
    b1.grid(row=row, column=5, sticky=E)
    b2.grid(row=row, column=6, sticky=E)
    b3.grid(row=row, column=7, sticky=E)
    b4.grid(row=row, column=8, sticky=E)
    row +=1
    b5.grid(row=row, column= 0)



def add_interface():
    global aname
    aname = ttk.StringVar()
    create = ttk.Toplevel('Create a new task')
    lc1 = ttk.Label(create, text='Name: ', font=('arial', 10))
    ec1 = ttk.Entry(create, textvariable=aname, font=('arial', 10))
    bc1 = ttk.Button(create, text='✓', bootstyle='success', command=lambda:[create_task(), create.destroy()])

    lc1.grid(row=0,column=0,sticky=W)
    ec1.grid(row=0, column=1)
    bc1.grid(row=0, column=2)


stat = {}
t_stash = {}
t2_stash = {}
t3_stash = {}
t4_stash = {}
b1_stash = {}
b2_stash = {}
b3_stash = {}
b4_stash = {}


row = 0
for task in task_list.values():
    t = ttk.Label(app, text=f'Task {task['id']} - ', font=('arial', 10))
    t2 = ttk.Label(app, text=task['description'], font=('arial', 10))
    t3 = ttk.Label(app, text=f'- created: {task['created']} last updated: {task['last updated']} ', font=('arial', 10))
    t4 = ttk.Label(app, text=f'status:', font=('arial', 10))
    t5 = ttk.Label(app, text=f' {task['status']}', font=('arial', 10))
    b1 = ttk.Button(app, text='DONE', bootstyle='success', command=lambda j=task['id']:task_update(j, 'done'))
    b2 = ttk.Button(app, text='IN PROGRESS', command=lambda j=task['id']:task_update(j, 'in progress'))
    b3 = ttk.Button(app, text='TO DO', bootstyle='warning', command=lambda j=task['id']:task_update(j, 'to do'))
    b4 = ttk.Button(app, text='X', bootstyle='danger', command=lambda j=task['id']:delete_task(j))
        
    t_stash[f'{task['id']}'] = t
    t2_stash[f'{task['id']}'] = t2
    t3_stash[f'{task['id']}'] = t3
    t4_stash[f'{task['id']}'] = t4
    b1_stash[f'{task['id']}'] = b1
    b2_stash[f'{task['id']}'] = b2
    b3_stash[f'{task['id']}'] = b3
    b4_stash[f'{task['id']}'] = b4
    stat[f'{task['id']}'] = t5

    t.grid(row=row, column=0, sticky= W)
    t2.grid(row= row, column= 1, padx= 5)
    t3.grid(row=row, column= 2)
    t4.grid(row=row, column=3)
    t5.grid(row=row, column=4, padx= 5)
    b1.grid(row=row, column=5, sticky=E)
    b2.grid(row=row, column=6, sticky=E)
    b3.grid(row=row, column=7, sticky=E)
    b4.grid(row=row, column=8, sticky=E)
    row +=1

    
b5 = ttk.Button(app, text='NEW', bootstyle='success', command=add_interface)
b5.grid(row=row, column= 0)
    


app.resizable(width=False, height=False)
app.mainloop()

