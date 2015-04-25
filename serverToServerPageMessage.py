__author__ = 'roman'

class ServerToServerPageMessage:
    NEW_CLIENT_MSG = 10
    CLIENT_LEAVED_MSG = 11
    WARNING_MSG = 12
    CLIENT_STATUS_MSG = 13
    WORK_DONE_MSG = 14

    def __init__(self, type):
        self.type = type
    def addClient(self, client):
        self.id = client.getId()
        self.httpUserAgent = client.getHttpUserAgent()
    def deletedClient(self, client):
        self.id = client.getId()
    def warning(self, msg):
        self.message = msg
    def clientStatus(self, clientId, status):
        self.clientId = clientId
        self.status = status
    def setSubstringPositions(self, substringPositions):
        self.substringPositions = substringPositions