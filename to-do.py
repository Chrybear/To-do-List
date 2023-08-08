# To-do list application
# Author: Ryan Barrett
# Date: 8/8/2023
# Desc: Simple To-do list application for programming practice


# Object for a list entry
class Entry:
    def __init__(self, val="", completed=False):
        self.val = val
        self.completed = completed
