import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)    #Green
GPIO.setup(19, GPIO.OUT)
pin = [2,19]

def SetupPhotoresistor(GPIOpin):
    GPIO.setup(GPIOpin,GPIO.IN)
    
def turnOnOffLED(LDR_DO):
    if LDR_DO == 1:
        GPIO.output(pin, True)
    else :
        GPIO.output(pin, False)

try:
    SetupPhotoresistor(14)
    while True:
        turnOnOffLED(GPIO.input(14))
        print(GPIO.input(2))
        time.sleep(1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()