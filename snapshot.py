import picamera
from time import sleep
import datetime as dt
from PIL import Image
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import storage
import RPi.GPIO as GPIO

#enable google cloud Storage & ref to an existing bucket
bucket = storage.Client().get_bucket('photoboothgdm.appspot.com')

cred = credentials.Certificate('photoboothgdm-firebase-adminsdk-swg32-46b010c16b.json')

default_app = firebase_admin.initialize_app(cred,{
   'databaseURL': 'https://photoboothgdm.firebaseio.com'
   })

ImageMeta = db.reference().child('ImageMeta')

test = db.reference('test').get()
print(test)

camera = picamera.PiCamera()
camera.hflip = True
camera.resolution = (1920,1080)

#GPIO Pins
GPIO.setmode(GPIO.BOARD)
button_white=12
button_yellow=16

GPIO.setup(button_white,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_yellow,GPIO.IN,pull_up_down=GPIO.PUD_UP)


while(1):
    if GPIO.input(button_white)==0:
        print('test')
        camera.start_preview()
        Time_String = dt.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S_%f')[:-3]
        ImageName = 'snapshot' + Time_String + '.jpg'
        sleep(2)
        camera.capture(ImageName)
        camera.stop_preview()
        
        #upload local file to online bucket
        blob = bucket.blob("Snaps/"+ImageName)
        blob.upload_from_filename(filename=ImageName)
        ImageMeta.push().set(ImageName)
        
    if GPIO.input(button_yellow)==0:
        print('prepare for aramageddon!')
        sleep(.1)


    

    
