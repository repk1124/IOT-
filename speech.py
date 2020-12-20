import speech_recognition as sr
import cv2
import numpy as np
import threading

cap=cv2.VideoCapture(0)
r = sr.Recognizer()
r.energy_threshold = 4000

def camera():
    print("Camera Start")
    while(cap.isOpened()):
        ret ,frame = cap.read()
        cv2.imshow("capture", frame)
        cv2.waitKey(1)
        
def speech():
    i=0
    img = 0
    while(cap.isOpened()):
        ret ,frame = cap.read()
        #my_stt = r.recognize_google(audio,language="en-US")
        print("Speech Start")
        my_stt = input()
        if my_stt == "take a photo":
            cv2.imwrite('C:\\Users\\repk1\\Desktop\\speech\\'+str(i)+'.jpg',frame)
            img = cv2.imread('C:\\Users\\repk1\\Desktop\\speech\\'+str(i)+'.jpg')
            i+=1
            continue
        elif my_stt == "show the photo":
            cv2.imshow("img",img)
            cv2.waitKey (0)
            continue
        print(img)
        print(my_stt)
    
while(1):
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        threads = [threading.Thread(target=camera),threading.Thread(target=speech)]
        for t in threads:
            t.start()
    except sr.UnknownValueError:
        print("Could Not Understand !")
    except sr.RequestError as e:
        print("Could Not Request !")
cap.release()
cv2.destroyAllWindows()