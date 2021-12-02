import socket
import RPi.GPIO as GPIO

bind_ip = "192.168.0.110"
bind_port = 8888

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((bind_ip,bind_port))
server.listen(5)
print("Listening on %s:%d"% (bind_ip,bind_port))

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)    #green
GPIO.setup(19,GPIO.OUT)     #red
GPIO.setup(20,GPIO.OUT)     #yellow
GPIO.setup(17,GPIO.OUT)
pwm = GPIO.PWM(17,50)
pwm.start(0)
pin=[2,19,20]

def SetAngle(angle):
    dutyCycle = 1/20 * angle + 3
    pwm.ChangeDutyCycle(dutyCycle)

try:
    client,addr = server.accept()
    print("Acepted connection from: %s:%d" % (addr[0],addr[1]))
    on = 180 #開啟-馬達轉180
    off = 0 #關閉-馬達轉回0
    GPIO.output(pin, False)
    count = 0
    while True:
        data = client.recv(1024)
        if data == b'gon':
            GPIO.output(2,True)
        elif data == b'goff':
            GPIO.output(2,False)
        elif data == b'ron':
            GPIO.output(19,True)
        elif data == b'roff':
            GPIO.output(19,False)
        elif data == b'yon':
            GPIO.output(20,True)
        elif data == b'yoff':
            GPIO.output(20,False)
        elif data == b'aon':
            GPIO.output(pin,True)
        elif data == b'aoff':
            GPIO.output(pin,False)
        elif data == b'mon':
            if count == 0:
                SetAngle(int(on))
                count = 1
            elif count == 1:
                SetAngle(int(off))
                count = 0
        else:
            print("Do Nothing ~")
            
except KeyboardInterrupt:
    client_socket.close()
    GPIO.output(pin, False)
    pass

GPIO,cleanup()
        





























