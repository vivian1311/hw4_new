import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time
mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

x = np.arange(0, 1, 1/18)
y = np.arange(0, 1, 1/18)
z = np.arange(0, 1, 1/18)
t = np.arange(0, 1, 1/18)
tilt = np.arange(0, 18, 1)

i = 0
# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    global i
    i += 1
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    data = float(msg.payload)
    print(data)
    print(i)
    if (i-1)%4 == 0:
        print("nx = ", int((i-1)/4))
        x[int((i-1)/4)] = data
        print("x = ", x[(i-1)/4])
    elif (i-1)%4 == 1:
        print("ny = ", int((i-1)/4))
        y[int((i-1)/4)] = data
    elif (i-1)%4 == 2:
        print("nz = ", int((i-1)/4))
        z[int((i-1)/4)] = data
    elif (i-1)%4 == 3:
        print("nt = ", int((i-1)/4))
        tilt[int((i-1)/4)] = data
    


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)


while True:
    mqttc.loop()
    if i >= 72:
        print(x)
        print(y)
        print(z)
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(t, x, color = "red", linestyle = "-", label = "x")
        ax[0].plot(t, y, color = "blue", linestyle = "-", label = "y")
        ax[0].plot(t, z, color = "green", linestyle = "-", label = "z")
        ax[0].legend(loc = 'upper left', frameon = False)
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Acc Vector')
        
        ax[1].plot(t,tilt)
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel('Amplitude')
        plt.show()
        break
