__author__ = 'roman'

from bottle import request, Bottle, abort
from bottle import route, run, template, static_file
import json
import jsonpickle
from client import Client
from jsonSerializableClient import JSONClient
from serverMessage import ServerMessage
from taskmanager import *

app = Bottle()
allClients = []
serverSocket = None

def getJSONClients(clients):
    result = []
    for cl in clients:
            jsonCl = JSONClient(cl.getId(), cl.getHttpUserAgent())
            result.append(jsonCl)
    return result

def sendClientsInfoToServerPage(allClients, serverSocket):
    if serverSocket:
        serverSocket.send(jsonpickle.encode(getJSONClients(allClients))) #send client info to server page

def sendMsgToClient(msg, socket):
    if socket:
        socket.send(jsonpickle.encode(msg)) #send client info to server page

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
    serverMsg = ServerMessage(ServerMessage.CONECTION_MSG, _client.getId())
    sendMsgToClient(serverMsg, _client.getSocket()) # send message that client is connected

    print("all clients: ", allClients.__len__())
    print("server socket: ", serverSocket)

    sendClientsInfoToServerPage(allClients, serverSocket)
    print("JSON data sended when new client was connected: ", jsonpickle.encode(getJSONClients(allClients))) #send client info to server page)


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
                    sendClientsInfoToServerPage(allClients, serverSocket)

        except WebSocketError:
            for cl in allClients:
                if cl.getSocket() == wsock:
                    allClients.remove(cl)
                    sendClientsInfoToServerPage(allClients, serverSocket)
            break

@app.route('/websocketServer')
def handle_websocket_server():
    global serverSocket #use global serverSocket because i want to send some data to server page from another function
    serverSocket = request.environ.get('wsgi.websocket')

    if serverSocket:
        print ("Server socket received")
        sendClientsInfoToServerPage(allClients, serverSocket)

    taskManager = TaskManager()
    print("Task manager generated tasks: ")
    for task in taskManager.getTasks(allClients.__len__()):
        print("task -- ", task.task[task.task.__len__()-200:task.task.__len__()])
    print("clients amount: ", allClients.__len__())

    if not serverSocket:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = serverSocket.receive()
            print(message);
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
