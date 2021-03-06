__author__ = 'roman'
import jsonpickle

class ClientToServerMessage:

    CONNECTION_MSG = 0 # client sends message that he is connected
    STATUS = 10 # status msg says client is busy or not, if busy persentage of the work that is done

    def __init__(self, msg):
        jsonMsg = jsonpickle.decode(msg)
        self.type = jsonMsg["type"]
        self.status = jsonMsg["status"]
        self.substringFound = jsonMsg["substringFound"]
        self.time = jsonMsg["time"]