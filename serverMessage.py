__author__ = 'roman'


class ServerMessage:

    CONECTION_MSG = 0 # msg

    def __init__(self, msgType, clientId):
        self.type = msgType
        self.id = clientId