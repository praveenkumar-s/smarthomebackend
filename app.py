import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
import time
from flask import request
import temp_listener
from subprocess import Popen, PIPE

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
databank={}

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/publish',methods=['POST'])
def publish_data():
    data = json.loads(request.data)
    mqtt.publish(data['topic'], data['message'])
    return '0'

@app.route('/getdata',methods=['GET'])
def getdata():
    channel=request.args.get('channel')
    mqtt.publish(channel,'GETDATA')
    p = Popen(['python', 'temp_listener.py',channel],shell = False, stdout=PIPE)
    if(p.stdout is not None):
        return p.stdout.readline()
    else:
        return '0'


    




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=False)