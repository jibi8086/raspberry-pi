#import RPi.GPIO as GPIO
import time
import sys
import thread
import picamera
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)#Red
GPIO.setup(26, GPIO.OUT)#Green
GPIO.setup(19, GPIO.OUT)#Yellow

def Redlight(delay):
    print("Red")
    GPIO.output(26, False)
    GPIO.output(19, False)
    GPIO.output(20, True)
    for x in range(0, 1000):
        input = GPIO.input(21)
        print(input)
        if(input==1):
                camera = picamera.PiCamera()
	        camera.capture("/home/pi/Desktop/new/test2.jpg")
	        email_user = 'jibin8087@gmail.com'
	        email_send = 'aiswaryarajan936@gmail.com'
	        subject = 'Traffic Violation Detected'
	        msg =MIMEMultipart()
		now = datetime.datetime.now()
	        msg['From'] = email_user
	        msg['To'] = email_send
	        msg['Subject'] = subject
	        body = 'Hi \n Traffic rule violated Vechicle image attached with this mail.\n Date And Time :'+str(now)
	        msg.attach(MIMEText(body,'plain'))
	        filename = "test2.jpg"
	        attachment =open(filename,'rb')
	        part=MIMEBase('application','octat-stream')
	        part.set_payload((attachment).read())
	        encoders.encode_base64(part)
	        part.add_header('Content-Disposition',"attachment; filename= "+filename)
	        msg.attach(part)
	        text = msg.as_string()
	        server =smtplib.SMTP('smtp.gmail.com',587)
	        server.starttls()
	        server.login(email_user,'********')
	        server.sendmail(email_user,email_send,text)
	        server.quit()
	        camera.close()
        time.sleep(0.01)
    #time.sleep(delay)
def Greenlight(delay):
    GPIO.output(26, True)
    GPIO.output(20, False)
    GPIO.output(19, False)
    print("Green")
    time.sleep(4)
def Yellowlight(delay):
    GPIO.output(26, False)
    GPIO.output(20, False)
    GPIO.output(19, True)
    print("Yellow")
    time.sleep(4)
try:
    while True:
        #thread.start_new_thread( Redlight, (4, ) )
        Redlight(4)
        Greenlight(1)
        Yellowlight(1)
except:
   print "Error: unable to start thread"
while 1:
   pass
