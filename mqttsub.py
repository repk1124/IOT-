import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)    #Red
GPIO.setup(20,GPIO.OUT)     #Yellow
GPIO.setup(2,GPIO.OUT)     #Green
GPIO.setup(17,GPIO.OUT)     #Servomotor
pwm = GPIO.PWM(17,50)
pwm.start(0)
pin = [19,20,2]
onA = 180 #開啟-馬達轉180
onB = 90 #關閉-馬達轉回90
onC = 0 #關閉-馬達轉回0
def SetAngle(angle):  #Servomotor
    dutyCycle = 1/20 * angle + 3
    pwm.ChangeDutyCycle(dutyCycle)

def on_connect(client,userdata,flags,rc):
    print("Connect with result code"+str(rc))
    global Connected 
    Connected = True

def on_message(client,userdata,msg):
    if msg.topic == "AF": #判斷是否為A農場
        msg.payload = float(msg.payload)
        if msg.payload <= 28 : #溫度小於28度
            GPIO.output(pin, False)
            GPIO.output(2, True) #開綠燈
            print(msg.topic+" Temp: "+str(msg.payload)+" Green ")
        elif msg.payload <= 32 : #溫度介於28~32度
            GPIO.output(pin, False)
            GPIO.output(20, True) #開黃燈
            print(msg.topic+" Temp: "+str(msg.payload)+" Yellow ")
        else : #溫度大於32度
            GPIO.output(pin, False)
            GPIO.output(19, True) #開紅燈
            print(msg.topic+" Temp: "+str(msg.payload)+" Red ")
    if msg.topic == "BF": #判斷是否為B農場
        msg.payload = float(msg.payload)
        if msg.payload <= 28 : #溫度小於28度
            SetAngle(onC) #馬達轉0
            print(msg.topic+" Temp: "+str(msg.payload)+" 0 ")
        elif msg.payload <= 32 : #溫度介於28~32度
            SetAngle(onB) #馬達轉90
            print(msg.topic+" Temp: "+str(msg.payload)+" 90 ")
        else : #溫度大於32度
            SetAngle(onA) #馬達轉180
            print(msg.topic+" Temp: "+str(msg.payload)+" 180 ")

Connected = False
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1",1883)

client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)
client.subscribe([("AF",0),("BF",0)]) #訂閱A農場與B農場

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print ("exiting")

GPIO.output(pin, False)
GPIO.output(17, False)
client.disconnect()
client.loop_stop()
