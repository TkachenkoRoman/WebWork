__author__ = 'roman'

class ServerToServerPageMessage:
    NEW_CLIENT_MSG = 10
    CLIENT_LEAVED_MSG = 11
    WARNING_MSG = 12

    def __init__(self, type):
        self.type = type
    def addClient(self, client):
        self.id = client.getId()
        self.httpUserAgent = client.getHttpUserAgent()
    def deletedClient(self, client):
        self.id = client.getId()
    def warning(self, msg):
        self.message = msg