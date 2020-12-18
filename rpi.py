import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
pin = [19,20]
def setup(GPIOnum,OUT_IN):
    if OUT_IN == "IN":
        GPIO.setup(GPIOnum,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    else:
        GPIO.setup(GPIOnum,GPIO.OUT)
    
counter = 0
def motion(channel):
    global counter
    counter += 1
    print("Motion detected {0}".format(counter))
    LDE_Blink(pin,3)

def LDE_Blink(GPIOnum,times):
    for i in range(0,times):
        GPIOnum = random.choice(pin)
        GPIO.output(GPIOnum,GPIO.HIGH)
        time.sleep(random.uniform(0,0.5))
        GPIO.output(GPIOnum,GPIO.LOW)
        time.sleep(random.uniform(0,0.5))
    GPIO.output(2,False)
    time.sleep(1)
    GPIO.output(2,True)

if __name__ == "__main__":
    try:
        GPIO.output(2,True)
        setup(14,"IN")
        setup(pin,"OUT")
        GPIO.add_event_detect(14,GPIO.BOTH,callback=motion,bouncetime=300)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.output(pin,False)
        GPIO.cleanup()