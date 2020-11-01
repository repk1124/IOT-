from bluetooth import *
from numpy import *
import RPi.GPIO as GPIO
import time

server_socket = BluetoothSocket(RFCOMM)
server_socket.bind(("B8:27:EB:66:7A:43",6)) #MAC地址，PORT
server_socket.listen(1)
GPIO.setmode(GPIO.BCM)
conn_socket, address = server_socket.accept()
GPIO.setup(19, GPIO.OUT)    #Red
GPIO.setup(20,GPIO.OUT)     #Yellow
GPIO.setup(2,GPIO.OUT)     #Green
pin = [19,20,2] #燈組List
speedlist = [] #存取超速紀錄
acount = 0 #超速次數
bcount = 0 #未超速次數
try:
    while True:
        velocity = conn_socket.recv(1024)
        velocity = float(velocity)
        if velocity <= 10 : #小於等於10不亮燈
            GPIO.output(pin, False)
            bcount += 1
        elif velocity <= 20 : #小於等20亮綠燈
            GPIO.output(pin, False)
            GPIO.output(2, True)
            speedlist.append(velocity) #超速紀錄至speedlist
            acount += 1
        elif velocity <= 30 : #小於等於30亮黃燈
            GPIO.output(pin, False)
            GPIO.output(20, True)
            speedlist.append(velocity) #超速紀錄至speedlist
            acount += 1
        else:  #大於30亮紅燈
            GPIO.output(pin, False)
            GPIO.output(19, True)
            speedlist.append(velocity) #超速紀錄至speedlist
            acount += 1
        count = acount + bcount #次數總和
        if count == 20 : #滿20次(一分鐘)進入判斷
            print("一分鐘內有:%s起超速，平均車速:%.2f cm/sec",%(acount,mean(speedlist)))
            speedlist = [] #清除speedlist
        print("Velocity : %.2f cm/sec" %velocity)
        time.sleep(3)
            
except KeyboardInterrupt:
    pass

conn_socket.close()
server_socket.close()
GPIO.cleanup()
