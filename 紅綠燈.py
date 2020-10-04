import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)    #Red
GPIO.setup(3,GPIO.OUT)     #Yellow
GPIO.setup(14,GPIO.OUT)     #Green


def traffic_light():
    #Red
    GPIO.output(2,True)
    time.sleep(2)
    GPIO.output(2,False)
    time.sleep(0.5)
    
    #Yellow
    for i in range(5)
       GPIO.output(3,True)
       time.sleep(0.2)
       GPIO.output(3,False)
       time.sleep(0.5)

    
    # Green
    GPIO.output(14,True)
    time.sleep(1)
    GPIO.output(14,False)
    time.sleep(0.5)
    
try:
    while True:
        traffic_light()

except KeyboardInterrupt:
    pass

GPIO.cleanup()