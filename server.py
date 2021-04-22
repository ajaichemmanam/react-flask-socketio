from flask_socketio import SocketIO, emit
from flask import Flask
from flask_cors import CORS
from random import random
from threading import Thread, Event
from time import sleep

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)
# Server functionality for receiving and storing data from elsewhere, not related to the websocket
#Data Generator Thread
thread = Thread()
thread_stop_event = Event()
class DataThread(Thread):
    def __init__(self):
        self.delay = 0.5
        super(DataThread, self).__init__()
    def dataGenerator(self):
        print("Initialising")
        try:
            while not thread_stop_event.isSet():
                socketio.emit('responseMessage', {'temperature': round(random()*10, 3)})
                sleep(self.delay)
        except KeyboardInterrupt:
            # kill()
            print("Keyboard  Interrupt")
    def run(self):
        self.dataGenerator()
# Handle the webapp connecting to the websocket
@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit('responseMessage', {'data': 'Connected! ayy'})
    # need visibility of the global thread object
    global thread
    if not thread.isAlive():
        print("Starting Thread")
        thread = DataThread()
        thread.start()

# Handle the webapp connecting to the websocket, including namespace for testing
@socketio.on('connect', namespace='/devices')
def test_connect2():
    print('someone connected to websocket!')
    emit('responseMessage', {'data': 'Connected devices! ayy'})

# Handle the webapp sending a message to the websocket
@socketio.on('message')
def handle_message(message):
    # print('someone sent to the websocket', message)
    print('Data', message["data"])
    print('Status', message["status"])
    global thread
    global thread_stop_event
    if (message["status"]=="Off"):
        if thread.isAlive():
            thread_stop_event.set()
        else:
            print("Thread not alive")
    elif (message["status"]=="On"):
        if not thread.isAlive():
            thread_stop_event.clear()
            print("Starting Thread")
            thread = DataThread()
            thread.start()
    else:
        print("Unknown command")


# Handle the webapp sending a message to the websocket, including namespace for testing
@socketio.on('message', namespace='/devices')
def handle_message2():
    print('someone sent to the websocket!')


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
    # socketio.run(app, debug=False, host='0.0.0.0')
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
