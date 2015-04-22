__author__ = 'roman'

from bottle import request, Bottle, abort
from bottle import route, run, template

app = Bottle()
everybody = []

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    ip = request.environ.get('REMOTE_ADDR')
    wsock.send("Your ip is: %s" % ip)

    everybody.append(wsock)

    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            #wsock.send("Your message was: %r" % message)

            for ws in everybody:
                try:
                    ws.send("Your message was: %r" % message)
                except WebSocketError:
                    print ("somebody leave..")
                    everybody.remove(ws)

        except WebSocketError:
            break

@app.route('/')
def index():
    return template('hello_template')

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("127.0.0.1", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
