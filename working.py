# USAGE
# python videostream_demo.py
# python videostream_demo.py --picamera 1

# import the necessary packages
from imutils.video import VideoStream
import datetime as dt
import argparse
import imutils
import time
import cv2
import numpy as np
from PIL import Image
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import storage
import RPi.GPIO as GPIO

cascPath = "/home/pi/Downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"  # for face detection
faceCascade = cv2.CascadeClassifier(cascPath)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

#enable google cloud Storage & ref to an existing bucket
bucket = storage.Client().get_bucket('photoboothgdm.appspot.com')

cred = credentials.Certificate('photoboothgdm-firebase-adminsdk-swg32-46b010c16b.json')

default_app = firebase_admin.initialize_app(cred,{
   'databaseURL': 'https://photoboothgdm.firebaseio.com'
   })

ImageMeta = db.reference().child('ImageMeta')

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

mst = cv2.imread('moustache.png')


def put_moustache(mst,fc,x,y,w,h):
    
    face_width = w
    face_height = h

    mst_width = int(face_width*0.4166666)+1
    mst_height = int(face_height*0.142857)+1



    mst = cv2.resize(mst,(mst_width,mst_height))

    for i in range(int(0.62857142857*face_height),int(0.62857142857*face_height)+mst_height):
        for j in range(int(0.29166666666*face_width),int(0.29166666666*face_width)+mst_width):
            for k in range(3):
                if mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k] <235:
                    fc[y+i][x+j][k] = mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k]
    return fc

#GPIO Pins
GPIO.setmode(GPIO.BOARD)
button_white=12
button_yellow=16

GPIO.setup(button_white,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_yellow,GPIO.IN,pull_up_down=GPIO.PUD_UP)


# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40,40)
        )
                
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            frame = put_moustache(mst,frame,x,y,w,h)
                

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
	#Take picture after pressing white button
        if GPIO.input(button_white)==0:
            print('white button pressed')
            Time_String = dt.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S_%f')[:-3]
            ImageName = 'snapshot' + Time_String + '.jpg'
            cv2.imwrite(ImageName, frame)
        
            #upload local file to online bucket
            blob = bucket.blob("Snaps/"+ImageName)
            blob.upload_from_filename(filename=ImageName)
            ImageMeta.push().set(ImageName)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()