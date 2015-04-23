__author__ = 'roman'

class Task:
    def __init__(self):
        with open ("static/task/data.txt", "r") as myfile:
            self.data=myfile.read()