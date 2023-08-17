<h1>Description:</h1>
This is a simple To-do list application made in Python ver: 3.11.

It saves tasks into a pickle file (to-do.pkl) within the same location to-do.py is saved in.

<h1>Requirements:</h1>
Libraries included with Python: tikinter, pickle.

External libraries: customtkinter.

>pip3 install customtkinter 

<h1>To run:</h1>
Make sure required libraries are installed and python version is up to date (may work on older versions, but not tested).

Download to-do.py.

Run to-do.py from location it was downloaded to.

<h1>Actions:</h1>

1. Add task
 
   Enter name of new task in text box that has placeholder text 'I wanna...' then either hit 'Enter' key or click the 'Add' button.

   **Note**: Tasks must be unique. Will not save duplicate tasks.

   **Note**: Task names are limited to at most 50 characters long. Task names longer than that will be truncated.

2. Mark task complete

    Click on one (or more) tasks from the task window. Then, press the 'Mark Completed' button.

    Completed tasks can be viewed in the 'Finished Tasks' view (see #4).
3. Delete task

    Click on one (or more) tasks from either the un-completed or completed tasks window. Then, press the 'Delete Task' button.
4. Swap view

    Click the button labeled either 'Show Un-completed' or 'Show Completed' to swap view. 
    Button text changes depending on current view.

    Which window is currently being shown is denoted by label above the task list:

       Label says "To-do": currently viewing list of un-completed tasks.

       Label says "Finished Tasks": currently viewing list of completed tasks.
5. Clear completed tasks

    Click the button labeled "Clear Completed Tasks" to remove all tasks that are marked completed.

    **Note**: This will delete all tasks that have been marked complete from the saved list.
