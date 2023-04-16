import os             #access directives 
import random         #to generate random numbers
import time           #time module taking current line
import numpy as np
import cv2

folderpath = 'frames'
mylist = os.listdir(folderpath)
graphic = [cv2.imread(f'{folderpath}/{impath}')for impath in mylist]
green = graphic[0];
red = graphic[1];
kill = graphic[2];
winner = graphic[3];
intro = graphic[4];

cv2.imshow('Squid game', cv2.resize(intro, (0, 0), fx=0.67, fy=0.67))
cv2.waitKey(1)        #frames dont clash with each other

while True:
    cv2.imshow('Squid game', cv2.resize(intro, (0, 0), fx=0.67, fy=0.67))
    if cv2.waitKey(1) & 0xFF == ord('q'):           #after pressing we can exit from the frame user press q while loop break
        break

TIMER_MAX=45                #so user gets only 45 seconds to complete the game
TIMER = TIMER_MAX
maxMove = 6500000             #how frequently the red adn green light will change- if we give 5 then how many times light will change
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cap = cv2.VideoCapture(0)     #we capture each frame from the video from the webcam
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

win = False                   #variable whether the game is won or not in default it is false

prev = time.time()            #previous time means prev frame is updated
prevDoll = prev
showFrame = cv2.resize(green, (0, 0), fx=0.67, fy=0.67)
isgreen=True                #checks whether the light is green or red

while cap.isOpened() and TIMER >= 0:     #cap is video screen is running and then timer is 0 the timer is checked and if its greater then its light is green or not and if red then stop and if red light is there and pressed 'w'
    if isgreen and(cv2.waitKey(10) & 0xFF == ord('w')):
        win = True                       #then it determines that user has win or not
        break

    ret, frame = cap.read()               #from cap we are reading the frame one by one
 
    cv2.putText(showFrame, str(TIMER), (50, 50), font, 1, (0, int(255 * (TIMER) / TIMER_MAX), int(255 * (TIMER_MAX - TIMER) / TIMER_MAX)), 4, cv2.LINE_AA)

    cur = time.time()

    no = random.randint(1, 5)
    if cur - prev >= no:
        prev = cur
        TIMER = TIMER - no
        if cv2.waitKey(10) & 0xFF == ord('w'):
            win = True
            break

        if isgreen:
            showFrame = cv2.resize(red, (0, 0), fx=0.67, fy=0.67)
            isgreen = False
            ref = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)             #image is 3 layer rbg, convert into gray

        else:
            showFrame = cv2.resize(green, (0, 0), fx=0.67, fy=0.67)
            isgreen = True

    if not isgreen:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameDelta = cv2.absdiff(ref, gray)       #its absolute,frame is changing then numpy is change and then we find the difference between red light and the user,of its 0 then no movement,if thats a value we know we have a movement
        thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        change = np.sum(thresh)

        if change > maxMove:
            break
    else:
        if cv2.waitKey(10) & 0xFF == ord('W'):
            win = True
            break
    
    camshow = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)

    camH, camW = camshow.shape[0], camshow.shape[1]
    showFrame[0:camH, -camW:] = camshow

    cv2.imshow('Squid game', showFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if isgreen and (cv2.waitKey(10) & 0xFF == ord('W')):
        win = True
        break

cap.release()
if not win:
    for i in range(10):
        cv2.imshow('Squid game', cv2.resize(kill, (0, 0), fx=0.67, fy=0.67))

    while True:
        cv2.imshow('Squid game', cv2.resize(kill ,(0, 0), fx=0.67, fy=0.67))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
else:

    cv2.imshow('Squid game', cv2.resize(winner, (0, 0), fx=0.67, fy=0.67))
    cv2.waitKey(125)

    while True:
        cv2.imshow('Squid game', cv2.resize(winner, (0, 0), fx=0.67, fy=0.67))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()