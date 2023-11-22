import cv2
from deepface import DeepFace
import numpy as np
import time
import requests
import json

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)

start_time = time.time()
express_server_url = 'http://127.0.0.1:3000'  # Replace with your Express.js server endpoint

while video.isOpened():
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in face:
        img = cv2.rectangle(frame, (x, y), (x+w, y+w), (0, 0, 255), 1)
        try:
            analyze = DeepFace.analyze(frame, actions=['emotion'])
            current_time = time.time()
            if current_time - start_time >= 5:
                detected_emotion = analyze[0]['dominant_emotion']
                print(detected_emotion)
                
                payload = {'emotion': detected_emotion}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(express_server_url, data=json.dumps(payload), headers=headers)
                print("Emotion sent to server:", response.text)
                
                start_time = current_time  # Reset the start time
        except Exception as e:
            print(f"Error: {e}")
        
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
