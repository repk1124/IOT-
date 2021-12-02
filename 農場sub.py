import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)    #Red
GPIO.setup(20,GPIO.OUT)     #Yellow
GPIO.setup(2,GPIO.OUT)     #Green
pin = [19,20,2]

def on_connect(client,userdata,flags,rc):
    print("Connect with result code"+str(rc))
    global Connected 
    Connected = True

def on_message(client,userdata,msg):
    if msg.topic == "AF":
        msg.payload = float(msg.payload)
        if msg.payload <= 28 :
            GPIO.output(pin, False)
            GPIO.output(2, True)
            print(msg.topic+" Temp: "+str(msg.payload)+" Green ")
        elif msg.payload <= 32 :
            GPIO.output(pin, False)
            GPIO.output(20, True)
            print(msg.topic+" Temp: "+str(msg.payload)+" Yellow ")
        else :
            GPIO.output(pin, False)
            GPIO.output(19, True)
            print(msg.topic+" Temp: "+str(msg.payload)+" Red ")

Connected = False
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1",1883)

client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)
client.subscribe(("AF",0))

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print ("exiting")

GPIO.output(pin, False)
client.disconnect()
client.loop_stop()