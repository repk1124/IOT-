import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 3
GPIO_ECHO = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  #Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)   #ECHO
GPIO.setup(14, GPIO.OUT)    #Red
GPIO.setup(15,GPIO.OUT)     #Yellow
GPIO.setup(2,GPIO.OUT)     #Green
pin = [14,15,2]
distance0 = 0
StopTime1 = 0

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
        velocity = get_velocity() #取自感測器運算速度
        #spe=[31,25,15,5]  #測試用固定速度Random
        #i = random.choice(spe)
        #velocity = i
        if  dist_error:
             print("Range Error : Range 2-400 cm")
        else:
            if velocity <= 10 :
                GPIO.output(pin, False)
            elif velocity <= 20 :
                GPIO.output(pin, False)
                GPIO.output(2, True)
            elif velocity <= 30 :
                GPIO.output(pin, False)
                GPIO.output(15, True)
            else:
                GPIO.output(pin, False)
                GPIO.output(14, True)
            print("Velocity : %.2f cm/sec" %velocity)
            time.sleep(1) 
except KeyboardInterrupt:
    pass

GPIO.cleanup()
