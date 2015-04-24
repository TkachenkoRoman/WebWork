__author__ = 'roman'
from taskmanager import Task

class ServerToClientMessage:

    CONECTION_MSG = 0 # msg
    TASK_MSG = 1

    def __init__(self, msgType, clientId):
        self.type = msgType
        self.id = clientId

    def setTask(self, task):
        self.substringToSearch = task.substringToSearch # text to search
        self.string = task.string # part of text to search in
        self.startPos = task.getStartPos() # pos in non sliced text
