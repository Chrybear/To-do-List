# To-do list application
# Author: Ryan Barrett
# Date: 8/8/2023
# Desc: Simple To-do list application for programming practice
# Imports:
import tkinter
from os.path import exists
import pickle
import customtkinter as tk


# Object for a task item
# Current implementation would work with just a hash table and does not need a custom object.
# However, using an object opens possibilities for adding additional functionality, such as task priority, for a task.
class Task:
    def __init__(self, val="", completed=False):
        self.val = val
        self.completed = completed


# Function to get saved list (if one exists). If no such file exists, returns empty hash table.
# Reads from whatever location 'to-do.py' is currently located in.
def get_list():
    if exists('to-do.pkl'):
        return pickle.load(open('to-do.pkl', 'rb'))
    else:
        return {}


# Function to save the current state of the list !! Will override whatever is currently saved !!
# Saves to whatever location 'to-do.py' is currently located in.
def save_list(lis: list):
    pickle.dump(lis, open('to-do.pkl', 'wb'))  # Will create new file if one does not currently exist


# Function to print out all tasks currently saved into the console.
def print_list(lis):
    for key, value in lis.items():
        print(key, value.val)


if __name__ == '__main__':
    # On startup, load task hash table if one already exists, else initialize an empty hash table
    cur_list = get_list()
    # for i in range(100):
    #     cur_list[str(i)] = Entry(val=str(i))
    # print_list(cur_list)

    # Build GUI
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("blue")
    root = tk.CTk()
    root.title("To-do List")
    # root.geometry("900x750")
    frame = tk.CTkFrame(master=root)
    frame.pack(pady=10, padx=10, ipadx=10, fill="both", expand=True)

    # Label to display if we are looking at tasks that have/have not been done
    displaying_label = tk.CTkLabel(master=frame,
                                   text_color="#9900cc",
                                   text="To-do",
                                   font=("Calibri", 32, "bold")
                                   )
    displaying_label.pack()

    task_frame = tk.CTkFrame(master=frame, fg_color="transparent")
    task_frame.pack(anchor="center", expand=True)

    task_box_frame = tk.CTkFrame(master=task_frame, fg_color="#ffccff", bg_color="#ffccff")
    task_box_frame.pack(side="left", expand=True, ipadx=5, ipady=5)
    # List of our current tasks
    task_box = tkinter.Listbox(master=task_box_frame,
                               width=40,
                               font=("Calibri", 20, "bold"),
                               bg="#ffccff",
                               bd=0,
                               highlightthickness=0,
                               activestyle="none",
                               selectmode="multiple"
                               )
    task_box.pack(side="left", expand=True)
    # Add scroll-bars to the task box
    y_scroll_bar = tk.CTkScrollbar(master=task_box_frame, orientation="vertical")
    # x_scroll_bar = tk.CTkScrollbar(master=task_box_frame, orientation="horizontal")
    task_box.configure(yscrollcommand=y_scroll_bar.set)
    # task_box.configure(xscrollcommand=x_scroll_bar.set)

    y_scroll_bar.configure(command=task_box.yview)
    # x_scroll_bar.configure(command=task_box.xview)
    y_scroll_bar.pack(side="right", fill='y')
    # x_scroll_bar.pack(side="bottom", fill='x')

    # Function to empty and draw the task list
    def draw_tasks(show_complete=False):
        # First, clear out the listbox
        task_box.delete(0, 'end')
        for x in cur_list.values():
            if show_complete and x.completed:
                task_box.insert('end', x.val)
            elif not show_complete and not x.completed:
                task_box.insert('end', x.val)
    draw_tasks()

    # Task label and entry
    entry_frame = tk.CTkFrame(master=frame)
    entry_frame.pack(pady=10, padx=10, anchor="s")

    task_label = tk.CTkLabel(master=entry_frame, text="Enter New Task")
    task_label.pack(padx=10, side=tkinter.LEFT)

    task_entry = tk.CTkEntry(master=entry_frame, placeholder_text="I wanna...")
    task_entry.pack(pady=5, padx=10, side=tkinter.LEFT)

    # Function to add a new task to the current task list
    def add_task(event=None):  # We need a dummy parameter to make hitting 'enter' on keyboard work
        task = task_entry.get().strip()  # We want to remove redundant spaces/blank entries
        if task and task not in cur_list:
            # Need to account for rabble-rousers that may enter very long tasks
            # We will cut tasks down to 50 chars at most
            # This just makes sure that string length will be max 50 characters long (including spaces)
            task = task[:51]  # If splicing with index > length of string, python treats it as simply the full string
            cur_list[task] = (Task(val=task))
            save_list(cur_list)
            # Update the list of tasks (if we're showing un-completed)
            if "To-do" == displaying_label.cget('text'):
                task_box.insert('end', task)
            task_entry.delete(0, 'end')  # Reset the entry text box

    root.bind('<Return>', add_task)  # This enables user to simply hit 'Enter' instead of pressing 'Add' button

    # Function to mark the current selected task as complete
    def complete_task():
        cur_tasks = [task_box.get(x, x)[0] for x in task_box.curselection()]
        for task in cur_tasks:
            if cur_list.get(task, False):
                # Mark this one as complete
                cur_list[task].completed = True
        # After we finish, save list and re-draw task list (if we're viewing un-finished tasks)
        save_list(cur_list)
        draw_tasks(False if "To-do" == displaying_label.cget('text') else True)

    # Function to swap to viewing completed/un-completed tasks
    def swap_view():
        show_complete = False if "To-do" == displaying_label.cget('text') else True
        draw_tasks(not show_complete)
        if show_complete:
            change_view_button.configure(text="Show Completed")
            displaying_label.configure(text="To-do")
        else:
            change_view_button.configure(text="Show Un-completed")
            displaying_label.configure(text="Finished Tasks")

    # Function to delete a task
    def delete_task():
        cur_tasks = [task_box.get(x, x)[0] for x in task_box.curselection()]
        for task in cur_tasks:
            if cur_list.get(task, False):
                # Delete this task
                del cur_list[task]
        # After we finish, save list and re-draw task list
        save_list(cur_list)
        draw_tasks(False if "To-do" == displaying_label.cget('text') else True)

    # Function to clear out completed tasks
    def clear_completed():
        keys = list(cur_list.keys())
        for k in keys:
            if cur_list[k].completed:
                del cur_list[k]
        # Save list
        save_list(cur_list)
        # Update view
        draw_tasks("Finished Tasks" == displaying_label.cget('text'))

    # Button frame
    button_frame = tk.CTkFrame(master=task_frame,
                               bg_color="transparent",
                               fg_color="transparent",
                               width=30,
                               height=10
                               )
    button_frame.pack(side='right')
    # Add button (added to entry frame as this button relates to entering a task)
    add_button = tk.CTkButton(master=entry_frame, text="Add", command=add_task, fg_color="#9900cc")
    add_button.pack(pady=10, padx=10, side=tkinter.LEFT)

    # Complete button
    mark_done_button = tk.CTkButton(master=button_frame, text="Mark Completed", command=complete_task, 
                                    fg_color="#9900cc")
    mark_done_button.pack(pady=15, padx=10, fill="both")

    # Delete task
    delete_task_button = tk.CTkButton(master=button_frame, text="Delete Task", command=delete_task,
                                      fg_color="#9900cc")
    delete_task_button.pack(pady=15, padx=10, fill="both")

    # Show completed/show un-completed button
    change_view_button = tk.CTkButton(master=button_frame, text="Show Completed", command=swap_view,
                                      fg_color="#9900cc")
    change_view_button.pack(pady=15, padx=10, fill="both")

    # Clear completed tasks
    clear_completed_button = tk.CTkButton(master=button_frame, text="Clear Completed Tasks", command=clear_completed,
                                          fg_color="#9900cc")
    clear_completed_button.pack(pady=15, padx=10, fill="both")

    # Start GUI
    root.mainloop()

