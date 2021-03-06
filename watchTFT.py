import smtplib # import SMTP protocol
import RPi.GPIO as GPIO # Enable Gpio port
from time import sleep #import time
from datetime import datetime #import datetime
import board #import raspberry pi board
import digitalio #Import digital
import picamera #Import Camera
import Image #import image
import ImageDraw #import ImageDraw
import ImageFont #import ImageFont
 
import Adafruit_ILI9341 as TFT # Import TFT Display
import Adafruit_GPIO as GPIO # Import GPIO for Enabling TFT Display
import Adafruit_GPIO.SPI as SPI # Import GPIO.SPI for enable circuit connection

import serial #Enable Serial Communication

SERIAL_PORT = "/dev/serial0" # Set TX and RX Serial communication
running = True	#Status Set as true for intial setup
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5) #Set TFT display baudrate
 
# Raspberry Pi configuration.
DC = 18  #Connection Raspberry pi Pin 18 to TFT
RST = 23  #Connection Raspberry pi Pin 23 to TFT
SPI_PORT = 0  #Connection Raspberry pi SPI to TFT
SPI_DEVICE = 0  #Connection Raspberry pi SPI to TFT
GPIO.setmode(GPIO.BCM) #Enable BCM mode for raspberry pi for read and write the values in circuit
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enabling push button
 
 
# Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
 
# Initialize TFT display for show the Contents.
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
    find_device = "ip addr show" # find the ip address
    interface_parse = run_cmd(find_device) # find the mac address
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name
def readData(): #Take video and sent Email
	try: # handle Exception
		if(True): # button pressed
			fromaddr = 'FrommailId@gmail.com' # from maild address
			toaddrs = 'TomailId@gmail.com' # To maild address
			msg = ""+getPositionData(gps) #call function for get the location
			username = 'username' #set username
			password = '**********' #set password
			server = smtplib.SMTP('smtp.gmail.com:587') #set smpt protocol
			server.starttls() #start
			server.login(username,password) #login the mail
			server.sendmail(fromaddr, toaddrs, msg)  #sent the mail
			server.quit() #logout mail
			TakeVideo()
			print("Completed") #completed
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

# wipe LCD screen before we start


def TakeVideo(): #Start video Recording
    camera = picamera.PiCamera()	#Enable camara
    camera.capture("/home/pi/Desktop/new/test2.jpg") #capture image
    camera.start_recording("./home/pi/Desktop/new") #start recording
    sleep(10) #Set delay for 10 seconds
    camera.stop_recording()# stop recording

def start():
    if GPIO.input(21)==0: #check button pressed or not
        print("Button Pressed") #Person pressed emergency button
        readData() # call method readData
    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n') #Show the date and time

    # current ip address
    lcd_line_2 = "IP " 

    # combine both lines into one update to the display

    draw_rotated_text(disp.buffer, lcd_line_1 + lcd_line_2, (150, 120), 90, font, fill=(255,255,255)) #Print date and time
    disp.display() #show the above data into display
    sleep(2) # delay 2 second for load the data to screen

while True: # Execution start
	try:
		start() #Call function start
	except Exception as e:
		print(e) # print exception
		start() #Again Call function start
