__author__ = 'roman'
import jsonpickle

class ServerPageToServerMessage:

    START_SHARING_TASKS_MSG = 1;
    GREATING_MSG = 0;

    def __init__(self, msg):
        jsonMsg = jsonpickle.decode(msg)
        self.type = jsonMsg["type"]
        self.data = jsonMsg["data"]
