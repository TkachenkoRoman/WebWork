__author__ = 'roman'

class Client:
    def __init__(self, id, ws):
        self.id = id
        self.websocket = ws

    def getSocket(self):
        return self.websocket

    def getId(self):
        return self.id
