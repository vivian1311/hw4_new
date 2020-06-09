import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
import serial

# MQTT broker hosted on local machine
mqttc = paho.Client()
# Settings for connection
host = "localhost"
topic = "Mbed"

# signal
x = np.arange(0,2,0.005)
y = np.arange(0,2,0.005)
z = np.arange(0,2,0.005)
tilt = np.arange(0,2,0.005)
t = np.arange(0,20,0.1)


# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))
def on_message(mosq, obj, msg):
      data_input = str(msg.payload).split()
      for i in range (0, 200):
            x[i] = float(data_input[i])
      for i in range (200, 400):
            y[i] = float(data_input[i])
      for i in range (400, 600):
            z[i] = float(data_input[i])
      for i in range (600, 800):
            tilt[i] = float(data_input[i])

      # ploting
      print("start ploting\n")
      fig, ax = plt.subplots(2, 1)
      ax[0].plot(t, x, color = "red", linestyle = "-", label = "x")
      ax[0].plot(t, y, color = "blue", linestyle = "-", label = "y")
      ax[0].plot(t, z, color = "green", linestyle = "-", label = "z")
      ax[0].legend(loc = 'upper left', frameon = False)
      ax[0].set_xlabel('Time')
      ax[0].set_ylabel('Acc Vector')
      
      ax[1].plot(t,y_t)
      ax[1].set_xlabel('Time')
      ax[1].set_ylabel('Amplitude')
      plt.show()


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



# Loop forever, receiving messages
mqttc.loop_forever()