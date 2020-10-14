import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 3
GPIO_ECHO = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  #Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)   #ECHO
GPIO.setup(14, GPIO.OUT)    #Red
GPIO.setup(15,GPIO.OUT)     #Yellow
GPIO.setup(2,GPIO.OUT)     #Green
pin = [14,15,2]

def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    
def get_speed():
    temperature = 35
    speed = 33100 + temperature * 60
    return speed
    
def distance(speed):
    send_trigger_pulse()
    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * speed) / 2
    return distance
try:
    while True:
        speed = get_speed()
        dist = distance(speed)
        if dist <= 5 :
            GPIO.output(pin, False)
            GPIO.output(14, True)
        elif dist <= 10 :
            GPIO.output(pin, False)
            GPIO.output(15, True)
        elif dist <= 15 :
            GPIO.output(pin, False)
            GPIO.output(2, True)
        else :
            GPIO.output(pin, False)
        print ("Measured Distance = %.2f cm" % dist)
        time.sleep(1)    

except KeyboardInterrupt:
    pass

GPIO.cleanup()