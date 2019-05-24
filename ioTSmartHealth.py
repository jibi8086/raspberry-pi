import time
import requests
import Adafruit_DHT
import smtplib
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from time import sleep
GPIO.setmode(GPIO.BCM)#GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
buzzer = Buzzer(20)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
sensor = Adafruit_DHT.DHT22
adc.start_adc(0, gain=GAIN)
pin = 4
def read():
try:
  print("********** Enter Button ************")
  while True:
    if GPIO.input(21)==0:
      time.sleep(2)
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
      if humidity is not None and temperature is not None:
         temperature=temperature/10
         print('Temp={0:0.1f}*C '.format(temperature))
         #heartBeat=45
         temp=round(temperature)
         while True:
            value = adc.get_last_result()
            millivolts = (value / 10000.0) *1000
            celsiu = millivolts / 35
            celsius=round(celsiu)
            print('HeartBeat Pulse 0: {0}'.format(celsius))
            time.sleep(0.5)
            adc.stop_adc()
            if (temp >70) and celsius >20 and celsius<60:
              userdata = {"heartBeat":celsius,"temp":temp}
              resp =
              requests.post('https://ashlinvarghese1996.000webhostapp.com/SmartHelth/pythonRequest.php', params=userdata)
              print("success")
              fromaddr = 'smarthealth911@gmail.com'
              toaddrs = 'aswinsajikalloor@gmail.com'
              msg = "Hi,\n Patient Condition is critical patient reportgiven below \n\n Name:Aswin \n Status:Critical\n HeartBeat:"+str(celsius)+"\nTemperature:"+str(temp)+"\n\n With thanks and regards\n Smart Health MonitoringTeam"
              username = 'smarthealth911@gmail.com'
              password = 'smartadmin'
              server = smtplib.SMTP('smtp.gmail.com:587')
              server.starttls()
              server.login(username,password)server.sendmail(fromaddr, toaddrs, msg)
              server.quit()
              print("completed")
              while True:
                buzzer.on()
                buzzer.beep()
                sleep(1)
                buzzer.off()
                sleep(1)
                buzzer.beep()
                read()
                break
              else:
                print("Safe condition")
                while True:
                  buzzer.on()
                  buzzer.beep()
                  sleep(1)
                  buzzer.off()
                  break
                  sleep(1)
                  buzzer.beep()
                  time.sleep(2)
                  read()
except Exception as e:
print(e)
while True:
read()
