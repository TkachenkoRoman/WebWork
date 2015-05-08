__author__ = 'roman'

class Task:
    """
        all proper info about task
    """
    COMPLETED_TASK = 1
    UNCOMPLETED_TASK = 0
    def __init__(self, substringToSearch, string, status):
        self.substringToSearch = substringToSearch # text to search
        self.string = string # part of text to search in
        self.status = status
        self.client = None
    def setClientPerformer(self, client):
        self.client = client
    def getClientPerformer(self):
        return self.client
    def setStartPos(self, pos):
        self.startPos = pos
    def getStartPos(self):
        return self.startPos

class TaskManager:
    """ Divides text into parts, generates Tasks for clients """
    def __init__(self, substringToSearch):
        with open ("static/task/data.txt", "r") as myfile:
            self.data = myfile.read()
            self.substringToSearch = substringToSearch
            print("DATA.TXT: ", self.data[0:500])

    def getTasks(self, clientsAmount):
        if clientsAmount == 0:
            return None

        dataLen = self.data.__len__()
        resultTaskList = []
        if dataLen > 0:
            if clientsAmount > 1:
                approximateTaskLen = dataLen // clientsAmount
                print("approximateTaskLen: ", approximateTaskLen)
                currentPosStart = 0
                currentPosEnd = approximateTaskLen
                for i in range(clientsAmount):
                    extraData = 0
                    if i != clientsAmount - 1:
                        while self.data[currentPosEnd] != '\n':
                            currentPosEnd = currentPosEnd -1
                            extraData = extraData + 1
                    currTask = Task(self.substringToSearch, self.data[currentPosStart:currentPosEnd], Task.UNCOMPLETED_TASK)
                    currTask.setStartPos(currentPosStart)
                    resultTaskList.append(currTask)
                    currentPosStart = currentPosEnd + 1
                    if i == clientsAmount - 2:
                        currentPosEnd = dataLen
                        print("currentPosEnd = ", currentPosEnd, self.data[currentPosEnd - 10:currentPosEnd])
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
