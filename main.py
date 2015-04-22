__author__ = 'roman'

from bottle import request, Bottle, abort
from bottle import route, run, template, static_file

app = Bottle()
allClients = []

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    ip = request.environ.get('REMOTE_ADDR')
    wsock.send("Your ip is: %s" % ip)

    allClients.append(wsock)

    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            #wsock.send("Your message was: %r" % message)

            for ws in allClients:
                try:
                    ws.send("Your message was: %r" % message)
                except WebSocketError:
                    print ("somebody leave..")
                    allClients.remove(ws)

        except WebSocketError:
            break

@app.route('/')
def index():
    return template('client_template')

@app.route('/server')
def server():
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
