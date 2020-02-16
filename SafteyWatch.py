import smtplib # import SMTP protocol
import RPi.GPIO as GPIO # Enable Gpio port
from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep
import time
import picamera #Import Camera
import Adafruit_ADS1x15
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GAIN = 1
pin = 4
# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

# looking for an active Ethernet or WiFi device
def find_interface(): # find the Ip address
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name
def readData(): #Take video and sent Email
	try: # handle Exception
		if(True): # button pressed
			fromaddr = 'From mailId@gmail.com'
			toaddrs = 'To mail id@gmail.com'
			msg = "Hi,\n Your friend is critical stage \n\n Name:Dhavood \n Status:Critical\n HeartBeat:"+str(pulseFinal)+"\n Temperature:"+str(temp)+"\n\n With thanks and regards\n Smart Watch Team"
			username = 'jibin8087@gmail.com'
			password = '**********'
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login(username,password)
			server.sendmail(fromaddr, toaddrs, msg)
			server.quit()
			print("Completed")
		sleep(0.2)
	except Exception as e:
		lcd.clear()
		lcd.message("Enable Network")
		print(e)
# find an active IP on the first LIVE network device
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

# wipe LCD screen before we start
lcd.clear()


def TakeVideo(): #Start video Recording
    camera = picamera.PiCamera()	
    camera.capture("/home/pi/Desktop/new/test2.jpg")
    camera.start_recording("./home/pi/Desktop/new")
    sleep(10)
    camera.stop_recording()

def start():
    if GPIO.input(21)==0:
        print("Button Pressed") #Person pressed emergency button
        readData()
    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n') #Show the date and time

    # current ip address
    lcd_line_2 = "IP " 

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(2)

while True: # Execution start
	try:
		start()
	except Exception as e:
		print(e)
