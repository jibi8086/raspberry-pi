import RPi.GPIO as GPIO
import time
import requests
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
print("Distance Measurement In Progress")
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")
time.sleep(2)
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)
while GPIO.input(ECHO)==0:
  pulse_start = time.time()
while GPIO.input(ECHO)==1:
  pulse_end = time.time()
pulse_end=input("Enter Pulse End: ")
pulse_start=input("Enter Pulse Start: ")
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
print ("Distance:",distance,"cm")
if distance>2:
  Sensordistance = distance
  userdata = {"distance": Sensordistance,"state":"critical"}
  resp = requests.post('https://jibin8086.000webhostapp.com/Image/python_test.php', params=userdata)
  print("success")
 elif distance>5:
  Sensordistance = distance
  userdata = {"distance": Sensordistance,"state":"half fill"}
  resp = requests.post('https://jibin8086.000webhostapp.com/Image/python_test.php', params=userdata)
  print("success")
  
