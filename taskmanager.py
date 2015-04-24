__author__ = 'roman'

class Task:
    COMPLETED_TASK = 1
    UNCOMPLETED_TASK = 0
    def __init__(self, substringToSearch, string, status):
        self.substringToSearch = substringToSearch # text to search
        self.string = string # part of text to search in
        self.status = status
    def setClientPerformer(self, client):
        self.client = client
    def getClientPerformer(self):
        return self.client
    def setStartPos(self, pos):
        self.startPos = pos
    def getStartPos(self):
        return self.startPos

class TaskManager:
    def __init__(self, substringToSearch):
        with open ("static/task/data.txt", "r") as myfile:
            self.data = myfile.read()
            self.substringToSearch = substringToSearch
            print("DATA.TXT: ", self.data[0:500])

    def getTasks(self, clientsAmount):
        dataLen = self.data.__len__()
        resultTaskList = []
        if dataLen > 0:
            if clientsAmount > 1:
                approximateTaskLen = dataLen // clientsAmount
                currentPosStart = 0
                currentPosEnd = approximateTaskLen
                for i in range(clientsAmount):
                    extraData = 0
                    while self.data[currentPosEnd] != '\n':
                        currentPosEnd = currentPosEnd -1
                        extraData = extraData + 1
                    currTask = Task(self.substringToSearch, self.data[currentPosStart:currentPosEnd], Task.UNCOMPLETED_TASK)
                    currTask.setStartPos(currentPosStart)
                    resultTaskList.append(currTask)
                    currentPosStart = currentPosEnd + 1
                    if i == clientsAmount:
                        currentPosEnd = dataLen
                    else:
                        currentPosEnd = currentPosEnd + approximateTaskLen + extraData
                return resultTaskList
            else:
                currTask = Task(self.substringToSearch, self.data, Task.UNCOMPLETED_TASK)
                currTask.setStartPos(0)
                resultTaskList.append(currTask)
                return resultTaskList
        else:
            return None
