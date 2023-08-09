# To-do list application
# Author: Ryan Barrett
# Date: 8/8/2023
# Desc: Simple To-do list application for programming practice
import tkinter
# Imports
from os.path import exists
import pickle
import customtkinter as tk

# TODO make it not ugly


# Object for a list entry
class Entry:
    def __init__(self, val="", completed=False):
        self.val = val
        self.completed = completed


# Function to get saved list (if one exists). If no such file exists, returns empty hash table
def get_list():
    if exists('to-do.pkl'):
        return pickle.load(open('to-do.pkl', 'rb'))
    else:
        return {}


# Function to save the current state of the list !! Will override whatever is currently saved
def save_list(lis: list):
    pickle.dump(lis, open('to-do.pkl', 'wb'))  # Will create new file if one does not currently exist


def print_list(lis):
    for key, value in lis.items():
        print(key, value.val)


if __name__ == '__main__':
    # On startup, load list if one already exists, else initialize an empty list
    cur_list = get_list()
    print_list(cur_list)

    # Build GUI TODO move this into own function
    tk.set_appearance_mode("System")
    tk.set_default_color_theme("blue")
    root = tk.CTk()
    root.title("To-do List")
    root.geometry("700x450")
    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    task_frame = tk.CTkFrame(master=frame)
    task_frame.pack()
    # List of our current tasks
    task_box = tkinter.Listbox(master=task_frame,
                               width=25,
                               height=5)
    task_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    # Add a scroll-bar to it
    scroll_bar = tk.CTkScrollbar(master=task_frame)
    scroll_bar.pack(side=tkinter.RIGHT)

    # Function to empty and draw the task list
    def draw_tasks(show_complete=False):
        # First, clear out the listbox
        task_box.delete(0, tkinter.END)
        for x in cur_list.values():
            if show_complete and x.completed:
                task_box.insert(tkinter.END, x.val)
            elif not show_complete and not x.completed:
                task_box.insert(tkinter.END, x.val)
    draw_tasks()

    # Task label and entry
    task_label = tk.CTkLabel(master=frame, text="Enter New Task")
    task_label.pack(padx=10)

    task_entry = tk.CTkEntry(master=frame, placeholder_text="I wanna...")
    task_entry.pack(pady=5, padx=10)

    # Function to add a new task to the current task list
    def add_task():
        task = task_entry.get()
        if task and task not in cur_list:
            cur_list[task] = (Entry(val=task))
            save_list(cur_list)
            # Update the list of tasks
            task_box.insert(tkinter.END, task)
            task_entry.delete(0, tkinter.END)  # Reset the entry text box

    # Function to mark the current selected task as complete
    def complete_task():
        cur_index = task_box.curselection()
        if cur_index:
            task_val = task_box.get(cur_index[0], cur_index[0])[0]
            if cur_list.get(task_val, False):
                # Mark this one as complete
                cur_list[task_val].completed = True
                # Remove it from the listbox
                task_box.delete(cur_index[0], cur_index[0])
                # Update saved list
                save_list(cur_list)

    # Function to swap to viewing completed/un-completed tasks
    def swap_view():
        show_complete = False if "Show Completed Tasks" == change_view_button.cget('text') else True
        draw_tasks(not show_complete)
        if show_complete:
            change_view_button.configure(text="Show Completed Tasks")
        else:
            change_view_button.configure(text="Show Un-completed Tasks")

    # Function to delete a task
    def delete_task():
        cur_task = task_box.curselection()
        if cur_task:
            task_val = task_box.get(cur_task[0], cur_task[0])[0]
            if task_val in cur_list:
                # Remove from the list
                del cur_list[task_val]
                # Remove from the task box
                task_box.delete(cur_task[0], cur_task[0])
                # Update tasks shown
                # makes sure we're showing the current view
                draw_tasks("Show Un-completed Tasks" == change_view_button.cget('text'))
                # Save tasks
                save_list(cur_list)

    # Function to clear out completed tasks
    def clear_completed():
        keys = list(cur_list.keys())
        for k in keys:
            if cur_list[k].completed:
                del cur_list[k]
        # Save list
        save_list(cur_list)
        # Update view
        draw_tasks("Show Un-completed Tasks" == change_view_button.cget('text'))

    # Add button
    add_button = tk.CTkButton(master=frame, text="Add", command=add_task)
    add_button.pack(pady=5, padx=10)

    # Complete button
    mark_done_button = tk.CTkButton(master=frame, text="Mark Completed", command=complete_task)
    mark_done_button.pack(pady=5, padx=10)

    # Delete task
    delete_task_button = tk.CTkButton(master=frame, text="Delete Task", command=delete_task)
    delete_task_button.pack(pady=5, padx=10)

    # Show completed/show un-completed button
    change_view_button = tk.CTkButton(master=frame, text="Show Completed Tasks", command=swap_view)
    change_view_button.pack(pady=5, padx=10)

    # Clear completed tasks
    clear_completed_button = tk.CTkButton(master=frame, text="Clear Completed Tasks", command=clear_completed)
    clear_completed_button.pack(pady=5, padx=10)

    # Start GUI
    root.mainloop()

