import smtplib
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep
import time
import Adafruit_DHT
import Adafruit_ADS1x15
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
sensor = Adafruit_DHT.DHT22
adc.start_adc(0, gain=GAIN)
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
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name
def readData():
	try:
		value = adc.get_last_result()
		#print(value)
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			temperature=temperature/10
			print('Temp={0:0.1f}*C '.format(temperature))
			temp=round(temperature)
			time.sleep(1)
		pulse = (value / 10000.0) *1000
		pulseFinal = pulse /35
		pulseFinal=round(pulseFinal)
		print(pulseFinal)
		if(temp>70) or pulseFinal>20 or pulseFinal<60:
			fromaddr = 'jibin8087@gmail.com'
			toaddrs = 'dhavoodnassar98@gmail.com'
			msg = "Hi,\n Your friend Dhavood health Report critical report given below \n\n Name:Dhavood \n Status:Critical\n HeartBeat:"+str(pulseFinal)+"\n Temperature:"+str(temp)+"\n\n With thanks and regards\n Smart Watch Team"
			username = 'jibin8087@gmail.com'
			password = '*******'
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login(username,password)
			server.sendmail(fromaddr, toaddrs, msg)
			server.quit()
			print("Completed")
		sleep(0.2)
		#lcd_line_01 = datetime.now().strftime('%b %d  %H:%M:%S\n')
		#lcd_line_02="Pulse:"+pulseFinal+" Temp:"+temp
		#lcd.clear()
		#lcd.message(lcd_line_02)
		#sleep(4)
		#lcd.clear()
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

# before we start the main loop - detect active network device and ip address
#sleep(2)
#interface = find_interface()
#ip_address = parse_ip()

def start():
    if GPIO.input(21)==0:
        print("Button Pressed")
        readData()
    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')

    # current ip address
    lcd_line_2 = "IP " 

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(2)
while True:
	try:
		start()
	except Exception as e:
		print(e)
		#start()
