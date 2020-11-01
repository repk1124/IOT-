from bluetooth import *
from numpy import *
import RPi.GPIO as GPIO
import time

server_socket = BluetoothSocket(RFCOMM)
server_socket.bind(("B8:27:EB:66:7A:43",6))
server_socket.listen(1)
GPIO.setmode(GPIO.BCM)
conn_socket, address = server_socket.accept()
GPIO.setup(19, GPIO.OUT)    #Red
GPIO.setup(20,GPIO.OUT)     #Yellow
GPIO.setup(2,GPIO.OUT)     #Green
pin = [19,20,2]
speedlist = []
acount = 0
bcount = 0
try:
    while True:
        velocity = conn_socket.recv(1024)
        velocity = float(velocity)
        if velocity <= 10 :
            GPIO.output(pin, False)
            bcount += 1
        elif velocity <= 20 :
            GPIO.output(pin, False)
            GPIO.output(2, True)
            speedlist.append(velocity)
            acount += 1
        elif velocity <= 30 :
            GPIO.output(pin, False)
            GPIO.output(20, True)
            speedlist.append(velocity)
            acount += 1
        else:
            GPIO.output(pin, False)
            GPIO.output(19, True)
            speedlist.append(velocity)
            acount += 1
        count = acount + bcount
        if count == 20 :
            print("一分鐘內有:%s起超速，平均車速:%.2f cm/sec",%(acount,mean(speedlist)))
        print("Velocity : %.2f cm/sec" %velocity)
        time.sleep(3)
            
except KeyboardInterrupt:
    pass

conn_socket.close()
server_socket.close()
GPIO.cleanup()
