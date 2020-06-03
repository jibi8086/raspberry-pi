import smtplib # import SMTP protocol
import RPi.GPIO as GPIO # Enable Gpio port
from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
from time import sleep
import time
import picamera #Import Camera
import Adafruit_ADS1x15
import Image
import ImageDraw
import ImageFont
 
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import serial

SERIAL_PORT = "/dev/serial0"
running = True	
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)
 
# Raspberry Pi configuration.
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GAIN = 1
pin = 4
 
# BeagleBone Black configuration.
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0
 
# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
 
# Initialize display.
disp.begin()
disp.clear((255, 0, 0))
draw = disp.draw()


def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
	# Get rendered font width and height.
	draw = ImageDraw.Draw(image)
	width, height = draw.textsize(text, font=font)
	# Create a new image with transparent background to store the text.
	textimage = Image.new('RGBA', (width, height), (0,0,0,0))
	# Render the text.
	textdraw = ImageDraw.Draw(textimage)
	textdraw.text((0,0), text, font=font, fill=fill)
	# Rotate the text image.
	rotated = textimage.rotate(angle, expand=1)
	# Paste the text into the image, using it as a mask for transparency.
	image.paste(rotated, position, rotated)

def getPositionData(gps):
    data = gps.readline()
    message = data[0:6]
    if (message == "$GPRMC"):
        # GPRMC = Recommended minimum specific GPS/Transit data
        # Reading the GPS fix data is an alternative approach that also works
        parts = data.split(",")
        if parts[2] == 'V':
            # V = Warning, most likely, there are no satellites in view...
            print "GPS receiver warning"
        else:
            # Get the position data that was transmitted with the GPRMC message
            # In this example, I'm only interested in the longitude and latitude
            # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
            longitude = formatDegreesMinutes(parts[5], 3)
            latitude = formatDegreesMinutes(parts[3], 2)
	    return "Your position: lon = " + str(longitude) + ", lat = " + str(latitude)
    else:
        # Handle other NMEA messages and unsupported strings
        pass


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
			msg = ""+getPositionData(gps)
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
		disp.clear((255, 0, 0))
		draw_rotated_text(disp.buffer, 'Enable Network', (150, 120), 90, font, fill=(255,255,255))		
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

    draw_rotated_text(disp.buffer, lcd_line_1 + lcd_line_2, (150, 120), 90, font, fill=(255,255,255))
    disp.display()
    sleep(2)

while True: # Execution start
	try:
		start()
	except Exception as e:
		print(e)
