__author__ = 'roman'

class ServerPageToServerMessage:

    START_SHARING_TASKS_MSG = 1;
    GREATING_MSG = 0;

    def __init__(self, jsonMsg):
        self.type = jsonMsg["type"]
        self.data = jsonMsg["data"]
