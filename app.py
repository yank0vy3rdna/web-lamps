from flask import Flask, request, send_file

import socket

app = Flask(__name__)


@app.route('/getInfo')
def getInfo():
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send(b'getInfo')
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")


@app.route('/lampOff')
def lampOff():
	lamp_id = request.args.get('lamp_id')
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send(('lampOff '+str(lamp_id)).encode('utf-8'))
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")

@app.route('/lampOn')
def lampOn():
	lamp_id = request.args.get('lamp_id')
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send(('lampOn '+str(lamp_id)).encode('utf-8'))
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")

@app.route('/allOn')
def allOn():
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send('allOn'.encode('utf-8'))
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")

@app.route('/allOff')
def allOff():
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send('allOff'.encode('utf-8'))
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")

@app.route('/getSunsetTime')
def getSunsetTime():
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send('getSunsetTime'.encode('utf-8'))
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")

@app.route('/getSunriseTime')
def getSunriseTime():
	sock = socket.socket()
	sock.connect(('172.18.0.5', 9090))
	sock.settimeout(1)
	sock.send('getSunriseTime'.encode('utf-8'))
	data = sock.recv(10000)
	sock.close()
	return data.decode("utf-8")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



