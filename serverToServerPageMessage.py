__author__ = 'roman'

class ServerToServerPageMessage:
    NEW_CLIENT_MSG = 0
    CLIENT_LEAVED_MSG = 1
    WARNING_MSG = 3

    def __init__(self, type):
        self.type = type
    def addClient(self, client):
        self.id = client.getId()
        self.httpUserAgent = client.getHttpUserAgent()
    def deletedClient(self, client):
        self.id = client.getId()
    def warning(self, msg):
        self.message = msg