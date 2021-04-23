# react-flask-socketio
This is a base code for testing websocket connection between python flask with socketio as Server and react Webapp as client

Run `pip install -r requirements.txt` under root folder <br />
Run `python server.py` (localhost:5000) <br />

Go to socketapp and open CMD, then run `npm install` <br />
Type `npm start` <br />
The data sent from python server is being displayed in the browser <br />
Click on "Start/Stop" to start or stop sending data from the server <br />

<br />
<br />
## Requirements
Requires Python 3+
<br />
npm i socket.io-client <br />

pip install Flask-SocketIO <br />
pip install gevent-websocket

Please pay attention to socketio version if you get any issues like "http://localhost:3000 is not an accepted origin Access to XMLHttpRequest at 'http://localhost:5001/socket.io/?EIO=3&transport=polling&t=NY2-yMT' from origin 'null' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. index.js:83 GET http://localhost:5001/socket.io/?EIO=3&transport=polling&t=NY2-yMT net::ERR_FAILED"
