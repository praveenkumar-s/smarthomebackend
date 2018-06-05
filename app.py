from flask import Flask
import datetime
import json
import requests
from flask import request
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_mqtt import Mqtt
import temp_listener
from subprocess import Popen, PIPE

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
bootstrap = Bootstrap(app)
databank={}


@app.route('/')
def index():
    return "index##"

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
    from os import environ
    
    app.run(debug=False , host='0.0.0.0', port=5000 , threaded=True)