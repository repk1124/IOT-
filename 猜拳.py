import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)  # Red
GPIO.setup(3, GPIO.OUT)  # Yellow
GPIO.setup(14, GPIO.OUT)  # Green


def pss(n):
    if n == 0:
        # 數入0"亮紅燈"並顯示"石頭"
        GPIO.output(2, True)
        print("石頭")
    elif n == 2:
        # 數入2"亮黃燈"並顯示"剪刀"
        GPIO.output(3, True)
        print("剪刀")
    elif n == 5:
        # 數入5"亮綠燈"並顯示"布"
        GPIO.output(14, True)
        print("布")
    else:
        count = 0 #閃爍次數預設0次
        pin = [2,3,14]
        # 輸入其它後一通亂閃
        while True:
            i = random.choice(pin) # 隨機取腳位控燈
            #print("控制腳位 : ",i) # 本地測試用
            #print("秒數 : ",random.uniform(0,0.5)) # 本地測試用
            GPIO.output(i, True)
            time.sleep(random.uniform(0,0.5)) # 隨機0~0.5之浮點數
            GPIO.output(i, False)
            time.sleep(random.uniform(0,0.5)) # 隨機0~0.5之浮點數
            count += 1 #閃爍次數加一次
            if count == 50: #閃爍50次跳出迴圈
                break

try:
    while True:
        n = input("請輸入數字 : ")
        # 空格處理
        n = n.replace(" ", "")
        # 防輸入其他字
        if n.isdigit():
            pss(int(n))
        else:
            print("你輸入的不是數字，請重新輸入 !")


except KeyboardInterrupt:
    pass

GPIO.cleanup()