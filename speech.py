import speech_recognition as sr
import cv2
import numpy as np
import threading

cap=cv2.VideoCapture(0)
r = sr.Recognizer()
r.energy_threshold = 4000

def camera(): #相機Live畫面
    print("Camera Start")
    while(cap.isOpened()):
        ret ,frame = cap.read()
        cv2.imshow("capture", frame)
        cv2.waitKey(1)
        
def speech(): #接收語音指令進行拍照與看照片
    i=0
    img = 0
    while(cap.isOpened()):
        ret ,frame = cap.read()
        my_stt = r.recognize_google(audio,language="en-US")
        print("Speech Start")
        #my_stt = input()
        if my_stt == "take a photo":
            cv2.imwrite('C:\\Users\\repk1\\Desktop\\speech\\'+str(i)+'.jpg',frame)
            img = cv2.imread('C:\\Users\\repk1\\Desktop\\speech\\'+str(i)+'.jpg')
            i+=1
            print(my_stt)
            continue
        elif my_stt == "show the photo":
            cv2.imshow("img",img)
            cv2.waitKey (0)
            print(my_stt)
            continue
    
while(1):
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        threads = [threading.Thread(target=camera),threading.Thread(target=speech)]
        for t in threads:
            t.start()  #啟動多執行續執行倆def
    except sr.UnknownValueError:
        print("Could Not Understand !")
    except sr.RequestError as e:
        print("Could Not Request !")
cap.release()
cv2.destroyAllWindows()
