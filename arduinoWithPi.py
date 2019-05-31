import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
while True:
	input = GPIO.input(21)
	if(input==1):
		print("Pressure sensor Medium squeeze")
