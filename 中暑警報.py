import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)  # Red
GPIO.setup(3, GPIO.OUT)  # Yellow
GPIO.setup(4, GPIO.OUT)  # Green
GP = 14 #溫溼度感測位於pin14
sensor = Adafruit_DHT.DHT11

try:
    while True:
        currentTime = time.strftime("%H:%M:%S")
        #humidity,temperature = Adafruit_DHT.read_retry(sensor,GP) #運用感測器取得溫溼度
        humidity = 31 #強制設定濕度為31%來達成中暑警報條件
        temperature = 35 #強制設定溫度為35度來達成中暑警報條件
        
        if humidity is not None and temperature is not None:
            print(currentTime,'-> Temp={0}*C Humidity={1}%'.format(temperature,humidity))
            
            if ((temperature > 38 and humidity > 30) or (temperature > 31 and humidity > 80)): #濕度高於30％，且氣溫高於38℃；或相對濕度高於80％，且氣溫高於31℃時。閃爍紅燈，並以文字發布中暑警報。
                print("中暑警報!")
                for i in range(5): #閃爍5次
                    GPIO.output(2, True)
                    time.sleep(0.4)
                    GPIO.output(2, False)
                    time.sleep(0.4)
            elif temperature > 34:
                print("預防中暑警報!")
                for i in range(5): #閃爍5次
                    GPIO.output(3, True)
                    time.sleep(0.4)
                    GPIO.output(3, False)
                    time.sleep(0.4)
            else:
                print("沒有中暑危險!")
                GPIO.output(4, True)
                time.sleep(4)
                GPIO.output(4, False)
                time.sleep(1)
        else:
            print('Faild to get reading. Try again!')
        time.sleep(5)

except KeyboardInterrupt:
    pass

GPIO.cleanup()