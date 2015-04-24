__author__ = 'roman'

from bottle import request, Bottle, abort
from bottle import route, run, template, static_file
import json
import jsonpickle
from client import Client
from jsonSerializableClient import JSONClient
from serverToClientMessage import ServerToClientMessage
from taskmanager import *
from serverPageToServerMessage import *
from serverToServerPageMessage import *

app = Bottle()
allClients = []
serverSocket = None
taskList = []

def sendAddClientMessageToServerPage(client):
    newClientMessage = ServerToServerPageMessage(ServerToServerPageMessage.NEW_CLIENT_MSG) # add client to server page
    newClientMessage.addClient(client)
    serverSocket.send(jsonpickle.encode(newClientMessage))

def sendLeaveClientMessageToServerPage(client):
    deletedClientMessage = ServerToServerPageMessage(ServerToServerPageMessage.CLIENT_LEAVED_MSG) # add client to server page
    deletedClientMessage.deletedClient(client)
    serverSocket.send(jsonpickle.encode(deletedClientMessage))

def sendWarningMessageToServerPage(message):
    warningMessage = ServerToServerPageMessage(ServerToServerPageMessage.WARNING_MSG) # add client to server page
    warningMessage.warning(message)
    serverSocket.send(jsonpickle.encode(warningMessage))

def sendMsgToClient(msg, socket):
    if socket:
        socket.send(jsonpickle.encode(msg)) #send client info to server page

def getServerPageToServerMessage(msg):
    return jsonpickle.decode(msg)

def giveOutTasks(allClients, taskList):
    clIndex = 0
    for task in taskList: # set performers to every task
        task.setClientPerformer(allClients[clIndex])
        clIndex = clIndex + 1
        if clIndex >= allClients.__len__():
            clIndex = 0
    for task in taskList: # give out Tasks
        client = task.getClientPerformer()
        print("performer for task is client with id ", client.getId())
        if client.busy == False:
            msg = ServerToClientMessage(ServerToClientMessage.TASK_MSG, client.getId())
            msg.setTask(task)
            print("message for perfrmer: ", msg)
            client.getSocket().send(jsonpickle.encode(msg))
            client.busy = True

@app.route('/websocketClient')
def handle_websocket_client():
    wsock = request.environ.get('wsgi.websocket')

    currentClientId = 0
    if allClients.__len__() <= 0: #form new id
        currentClientId = 0
    else:
        for cl in allClients:
            currId =  cl.getId()
            if currentClientId <= currId:
                currentClientId = currId + 1

    _client = Client(currentClientId, wsock, request.environ.get('HTTP_USER_AGENT'))
    print ("client socket received")

    allClients.append(_client) #append cluster in array to handle them
    serverMsg = ServerToClientMessage(ServerToClientMessage.CONECTION_MSG, _client.getId())
    sendMsgToClient(serverMsg, _client.getSocket()) # send message that client is connected

    print("all clients: ", allClients.__len__())
    print("server socket: ", serverSocket)


    sendAddClientMessageToServerPage(_client)

    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            #wsock.send("Your message was: %r" % message)

            for cl in allClients:
                try:
                    cl.getSocket().send("Your message was: %r" % message)
                except WebSocketError:
                    print ("somebody leave..")
                    allClients.remove(cl)
                    sendLeaveClientMessageToServerPage(cl)

        except WebSocketError:
            for cl in allClients:
                if cl.getSocket() == wsock:
                    allClients.remove(cl)
                    sendLeaveClientMessageToServerPage(cl)
            break

@app.route('/websocketServer')
def handle_websocket_server():
    global serverSocket #use global serverSocket because i want to send some data to server page from another function
    global taskList
    serverSocket = request.environ.get('wsgi.websocket')

    if serverSocket:
        print ("Server socket received")
        for cl in allClients:
            sendAddClientMessageToServerPage(cl)

    if not serverSocket:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = serverSocket.receive()
            print(message);
            messageDecoded = getServerPageToServerMessage(message)
            serverPageToServerMsg = ServerPageToServerMessage(messageDecoded)

            if serverPageToServerMsg.type == ServerPageToServerMessage.START_SHARING_TASKS_MSG: # if server page wants to start sharing tasks
                taskManager = TaskManager(serverPageToServerMsg.data) # create task manager, arg - substring to search
                taskList = taskManager.getTasks(allClients.__len__()) # generate tasks
                if taskList != None:
                    print("Task manager generated tasks: ")
                    for task in taskList:
                        print("task -- ", task.string[task.string.__len__()-200:task.string.__len__()])
                    print("clients amount: ", allClients.__len__())
                    print("substring to search: ", task.substringToSearch)

                    giveOutTasks(allClients, taskList)
                else:
                    sendWarningMessageToServerPage("No clients connected")

        except WebSocketError:
            print ("except WebSocketError")
            break

@app.route('/')
def index():
    return template('client_template')

@app.route('/server')
def server():
    print ("all clients: ", allClients)
    return template('server_template')


# Static Routes
@app.route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@app.route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@app.route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

@app.route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/fonts')


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("127.0.0.1", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
