from numpy import *
import paho.mqtt.client as mqtt
import time
import os

addr = str(input(請輸入IP : ))
print(addr)
TopicServerIP = addr
TopicServerPort = 1883
TopicName = "AF"
temp_list = []
while True:
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(TopicServerIP,TopicServerPort)
    a = random.uniform(20,40) #random溫度在20~40度之間
    temp_list.append(a)  #將random出來的溫度存在list內
    time.sleep(1)
    print(a)
    if len(temp_list) == 4:  #當list內有4筆資料則計算平均值
        b = round(mean(temp_list),2)  #平均值算出後取到小數點後兩位
        temp_list = []  #List歸零
        mqttc.publish(TopicName,str(b))  #傳送到sub
        print(b)
    time.sleep(random.uniform(5,10))  #random停留秒數於5~10之間，避免與其他pub之socket衝突
os.system("pause")
