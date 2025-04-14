#!/usr/bin/python

import sys
import cv2
import subprocess
import signal
import os
import time

def webcam_face_detect(video_mode, nogui = False, cascasdepath = "haarcascade_frontalface_default.xml"):

    face_cascade = cv2.CascadeClassifier(cascasdepath)

    video_capture = cv2.VideoCapture(video_mode)
    num_faces = 0
    spawnedguy = False

    while True:
        ret, image = video_capture.read()

        if not ret:
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (5,5)

            )

        #print("The number of faces found = ", len(faces))
        num_faces = len(faces)
        
        if spawnedguy == False:
            if num_faces>0:
                print("Changing")
                spawnedguy = True
                signal.signal(signal.SIGINT, signal_handler)
                subprocess.Popen("python carlaWalker.py")
                print("Spawning guy")
        elif spawnedguy == True:
            if num_faces == 0:
                print("Changing")
                spawnedguy = False
                os.kill(signal.CTRL_C_EVENT, 0)
                print("Ending guy")


        if not nogui:
            for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

            cv2.imshow("Faces found", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    video_capture.release()
    cv2.destroyAllWindows()
    return num_faces

def signal_handler(signal, frame):
  pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        video_mode= 0
    else:
        video_mode = sys.argv[1]
    webcam_face_detect(video_mode)
    