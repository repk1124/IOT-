import RPi.GPIO as GPIO
import datetime
import time

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 3
GPIO_ECHO = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  #Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)   #ECHO
GPIO.setup(2,GPIO.OUT)    #Green
GPIO.setup(17,GPIO.OUT)     #Servomotor
pwm = GPIO.PWM(17,50)
pwm.start(0)
pin = [2,17]
person = 10000 #預設偵測距離
countlist = [] #總數List
timelist = [] #時間緩存List
count = 0 #經過人數
time_count = 0 #時間次數緩存

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

def SetAngle(angle):
    dutyCycle = 1/20 * angle + 3
    pwm.ChangeDutyCycle(dutyCycle)

try:
    while True:
        currentTime = time.strftime("%H:%M:%S")
        speed = get_speed()
        dist = distance(speed)
        on = 180 #開啟-馬達轉180
        off = 0 #關閉-馬達轉回0
        if dist > person :
            if dist > 100: #距離100cm外
                count+=1 #人數+1
                print("經過人數:",count)
                SetAngle(int(off)) #馬達關閉轉至0
                GPIO.output(pin, False) #關燈與馬達
                person = 10000 #距離緩存回預設
                time_count = 0 #時間次數緩存回預設
                timelist.append(currentTime) #Append出去時間
                date_time1 = datetime.datetime.strptime(timelist[0],'%H:%M:%S') #string進入時間轉datetime型別
                date_time2 = datetime.datetime.strptime(timelist[1],'%H:%M:%S') #string出去時間轉datetime型別
                all_time = (date_time2 - date_time1).seconds #停留時間計算
                timelist.append(all_time) #Append停留時間
                countlist.insert(0,timelist) #插入該筆time list至第0位
                print("近5筆感測紀錄 : ")
                for i in range(count):
                    print("第",i+1,"筆資料:")
                    print("進入時間:",countlist[i][0])
                    print("離開時間:",countlist[i][1])
                    print("停留時間:",countlist[i][2],"秒")
                    if i == 4 : #第五筆終止迴圈
                        break
                timelist = []
        if dist < 100 : #距離100cm外
            person = dist #距離緩存=人體距離
            time_count += 1 #時間次數緩存+1
            if time_count == 1 : #抓第一筆時間紀錄
                GPIO.output(pin, False) #關燈與馬達
                GPIO.output(pin, True) #開燈與馬達
                SetAngle(int(on)) #馬達轉180
                timelist.append(currentTime) #Append進入時間
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(pin, False)
    pass

GPIO.cleanup()