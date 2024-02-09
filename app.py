from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
import threading
import time
taim = 53
def update_online_count():
    count = len(users)
    emit('online_count', {'count': count}, broadcast=True)
def vidt():
    global taim
    while True:
        taim = taim + 1
        time.sleep(1)

x = threading.Thread(target=vidt)
x.start()

app = Flask(__name__)
socketio = SocketIO(app)

# Словарь для хранения пользователей и их имен
users = {}

@app.route('/')
def index():
    return render_template('index.html')
@app.route("/taim")
def index2():
    global taim
    return str(taim)

@app.route("/tr.mp4")
def isendv():
	try:
		return send_file('tr.mp4')
	except Exception as e:
		return str(e)
     
@app.route("/stream")
def isend2v():
	try:
		return send_file('stream2.mp4')
	except Exception as e:
		return str(e)


@socketio.on('message')
def handle_message(data):
    name = data['name']
    if len(data['message']) < 1:
        pass
    else:
        message = data['message']
        emit('message', {'name': name, 'message': message}, broadcast=True)

@socketio.on('user_connected')
def handle_connect():
    name = request.args.get('name')
    if not name or len(name) > 20:
        name = 'Guest'
    users[request.sid] = name
    emit('message', {'name': 'System', 'message': f'{name} вошел в чат!'}, broadcast=True)
    update_online_count()

@socketio.on('disconnect')
def handle_disconnect():
    name = users.get(request.sid, 'Guest')
    del users[request.sid]
    emit('message', {'name': 'System', 'message': f'{name} покинул чат!'}, broadcast=True)
    update_online_count()


if __name__ == '__main__':
    socketio.run(app, debug=True)
