import serial
import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np

mqttc = paho.Client()

# XBee 
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY 0x140.")
print(char.decode())

s.write("ATDL 0x240\r\n".encode())
char = s.read(3)
print("Set DL 0x240.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")


# plot 
num = np.arange(0, 20, 1)
t = np.arange(0, 20, 1) 

for i in range (0, 20):
    s.write("/Data_Number/run\r".encode())
    print("aa")
    line = s.read()
    num[i] = float(line)
    time.sleep(1)

fig, ax = plt.subplots(1, 1)
ax.plot(t, num)
ax.set_xlabel('t')
ax.set_ylabel('num')
plt.show


host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

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



s.write("/replyans/run \r".encode())
for i in range (0, 800):
    line = s.read()
    print(line)
    mesg[i] = float(line)


mesg = ' '.join(str(data).split())
mqttc.publish(topic, mesg)
print(mesg)
time.sleep(1)

s.close()