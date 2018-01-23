import picamera
from PIL import Image
from time import sleep
import datetime as dt
import itertools
import tty, sys


with picamera.PiCamera() as camera:
        camera.framerate = 15
        camera.vflip = True
        camera.hflip = True
        #camera.brightness = 70
        #camera.sharpness = 10
        #camera.saturation = 100
        camera.resolution = (1296, 972)
        #print ( Time_String )
        #sleep(5)
        camera.start_preview()
        camera.annotate_text = 'Cheese Dude!'

        tty.setraw(sys.stdin.fileno())
        while 1:
                ch = sys.stdin.read(1)
                if ch == ' ':
                        capture()
                elif ch == 'q':
                        exitCam()

        def capture():
                Time_String = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                ImageName = './photos/image' + Time_String + '.jpg'
                camera.capture(ImageName)
                #camera.start_preview()
                #will now try and overlay the captured image on the preview for a short period, to show how it looked
                # Create an image padded to the required size with
                # mode 'RGB'
                img = Image.open(ImageName)
                pad = Image.new('RGB', (
                        ((img.size[0] + 31) // 32) * 32,
                        ((img.size[1] + 15) // 16) * 16,
                        ))
                # Paste the original image into the padded one
                pad.paste(img, (0, 0))
                o = camera.add_overlay(pad.tostring(), size=img.size)
                o.alpha = 255
                o.layer = 3
                sleep(5)

        def exitCam():
                camera.stop_preview()
                camera.close()