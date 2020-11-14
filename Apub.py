from numpy import *
import paho.mqtt.client as mqtt
import time

TopicServerIP = "127.0.0.1"
TopicServerPort = 1883
TopicName = "AF"
temp_list = []
while True:
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(TopicServerIP,TopicServerPort)
    a = random.uniform(20,40)
    temp_list.append(a)
    time.sleep(1)
    print(a)
    if len(temp_list) == 4:
        b = round(mean(temp_list),2)
        temp_list = []
        mqttc.publish(TopicName,str(b))
        print(b)
    time.sleep(random.uniform(5,10))