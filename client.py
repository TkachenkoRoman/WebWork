__author__ = 'roman'

class Client:
    def __init__(self, id, ws, httpUserAgent):
        self.id = id
        self.websocket = ws
        self.httpUserAgent = httpUserAgent
    def getSocket(self):
        return self.websocket

    def getId(self):
        return self.id

    def getHttpUserAgent(self):
        return self.httpUserAgent