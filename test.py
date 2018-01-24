from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
button_white=12
button_yellow=16

GPIO.setup(button_white,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_yellow,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while(1):
    if GPIO.input(button_white)==0:
        print('button_white')
        sleep(.1)
    if GPIO.input(button_yellow)==0:
        print('button_yellow')
        sleep(.1)
        
