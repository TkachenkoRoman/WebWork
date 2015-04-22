__author__ = 'roman'

from bottle import request, Bottle, abort
from bottle import route, run, template, static_file
import json
from client import Client

app = Bottle()
allClients = []
serverSocket = None

@app.route('/websocketClient')
def handle_websocket_client():
    wsock = request.environ.get('wsgi.websocket')

    currentClientId = 0
    if allClients.__len__() <= 0: #form new id
        currentClientId = 0
    else:
        for cl in allClients:
            currId =  cl.getId()
            if currentClientId < currId:
                currentClientId = currId + 1

    _client = Client(currentClientId, wsock)
    print ("client socket received")

    allClients.append(_client) #append cluster in array to handle them

    print("all clients: ", allClients.__len__())
    print("server socket: ", serverSocket)

    if serverSocket:
        serverSocket.send(json.dump(allClients))
        print("JSON: ", json.dump(allClients))


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

        except WebSocketError:
            break

@app.route('/websocketServer')
def handle_websocket_server():
    serverSocket = request.environ.get('wsgi.websocket')

    if serverSocket:
        print ("Server socket received")
        serverSocket.send(json.dumps(allClients))
        print("JSON: ", json.dumps(allClients))


    if not serverSocket:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = serverSocket.receive()
        except WebSocketError:
            break

@app.route('/')
def index():
    return template('client_template')

@app.route('/server')
def server():
    print ("all clients: ", allClients)
    return template('server_template', clients=allClients)


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
