from bluetooth import *
import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 3
GPIO_ECHO = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  #Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)   #ECHO
distance0 = 0
StopTime1 = 0

PORT = 6
client_socket = BluetoothSocket(RFCOMM)

client_socket.connect(("B8:27:EB:66:7A:43",PORT))

def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    
def get_speed():
    temperature = 35
    speed = 33100 + temperature * 60
    return speed
    
def get_velocity():
    global StopTime1,distance0,dist_error
    send_trigger_pulse()
    StopTime0 = StopTime1
    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime1 = time.time()
        
    TimeElapsed = StopTime1 - StartTime
    speed = get_speed()
    distance1 = TimeElapsed * speed * 0.5
    
    if distance1 < 2 or distance1 > 400:
         dist_error = True
    else:
         dist_error = False
    
    velocity = (distance1-distance0)/(StopTime1-StopTime0)
    distance0 = distance1
    return abs(velocity)
    
try:
    global dist_error
    dist_error = False
    while True:
        for i in range(20):
        #velocity = get_velocity()
            spe=[31.5,25.5,15.5,5.5]
            i = random.choice(spe)
            senddata = str(i)
            client_socket.send(senddata)
            print(senddata)
            
            time.sleep(3)
            
        print("count = 20")
    client_socket.close()
    
except KeyboardInterrupt:
    pass

GPIO.cleanup()
