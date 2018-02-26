import Adafruit_CharLCD as LCD
import socket
import os
import time
import subprocess
import glob
import shutil
import shlex
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Declare GPIO Port
lcd_rs        = 18
lcd_en        = 23
lcd_d4        = 12
lcd_d5        = 16
lcd_d6        = 20
lcd_d7        = 21
lcd_backlight = 4
lcd_columns = 16
lcd_lines  = 2


lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                           lcd_d6, lcd_d7, lcd_columns, lcd_lines,
                           lcd_backlight)
#Pendrive Name
src = 'debain'
dest = 'removable'

def execute(command):
    """Helper function for executing commands"""
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exit_code = proc.wait()
    stdout = proc.stdout.read()
    stderr = proc.stderr.read()
   # if not exit_code:
        #print("An error occured : {}.\nExiting.".format(stderr))
        #return None
    return stdout
def _execute(command):
    """Warning! Don't use this for anything"""
    out = os.popen(command)
    stdout = out.read().strip()
    return int(stdout)
def clean(dest_dev):
   stdout=execute("rm -rf {}" .format(dest_dev))

def copy(src_dev, dest_dev):
    src_mnt = '/mnt/src_usb/'
    dest_mnt = '/mnt/dest_usb/'
    mkdir_src_stdout = execute("mkdir -p {}".format(src_mnt))
    mkdir_dest_stdout = execute("mkdir -p {}".format(dest_mnt))
    mount_src_stdout = execute("mount /dev/{} {}".format(src_dev, src_mnt))
    mount_dest_stdout = execute("mount /dev/{} {}".format(dest_dev, dest_mnt))
    x=glob.glob("/mnt/src_usb/*")
    for i in x:
      print (i)
    #print(x[0])
    #shutil.copytree(src_mnt, dest_mnt)
    # this is a not very good way
    src_size = _execute("df {} | awk 'NR > 1 {{ print $3 }}'".format(src_mnt))
    dest_available = _execute("df {} | awk 'NR > 1 {{ print $4 }}'".format(dest_mnt))
    #input_format = GPIO.input(19)
    #input_enter = GPIO.input(26)
    #input_select = GPIO.input(13)
    
    while True:
        input_format = GPIO.input(19)
        input_enter = GPIO.input(26)
        input_select = GPIO.input(6)
        input_next=GPIO.input(13)
        if input_format == False:
            #lcd.message("formatting")
            lcd.clear()
            stdout=execute("rm -rf {}" .format(dest_mnt))
            #stdout=execute("cd {} rm -r src_usb")
            lcd.message("Formatting")
            time.sleep(2)
            break
        elif input_enter == False:
	    lcd.message("Select File")	
            i=0	
            while True:
                 if src_size < dest_available:
       	            lcd.clear()
       	           # lcd.message("Select File")
	            time.sleep(0.3)
		    lcd.clear()
            	    #for i in x:
               	    #print (i)
                    file=x[i]
                    newFile=(file.replace("/mnt/src_usb/",''))
                    lcd.message(newFile)
		    time.sleep(0.5)
       	            if GPIO.input(19)==0:
				print(GPIO.input(19))
				GPIO.cleanup(6)
				time.sleep(1)
                       	        #i=0
		                #lcd.clear()
                       	        #print(x[i])
		                lcd.clear()
		                lcd.message("copying")
		                stdout=execute("cp -r {} {}".format(x[i], dest_mnt))
		                time.sleep(1)
		                lcd.clear()
		                lcd.message("completed")
		                time.sleep(2)
		                lcd.clear()
                       	        #continue
    	            elif GPIO.input(13)==0:
			    if(len(file))>i:
	            	   	 i=i+1
			   	 print(i)
			       	 time.sleep(1)
			   	 print(x[i])		
                 else:
                    lcd.message("Memmory Full")
                    time.sleep(1)
		    lcd.message("please format")
		    time.sleep(1)
		    lcd.clear()
		    main()
		    break
#	except:
#		main()
 #       finally:
#		lcd.clear()
#		lcd.message("exited")
	   

    umount_src_stdout = execute("umount {}".format(src_dev))
    umount_dest_stdout = execute("umount {}".format(dest_dev))
    #shutil.rmtree(src_mnt)
    #shutil.rmtree(dest_mnt)

def main():
    dev_path = '/dev/disk/by-label/*'
    input_state = GPIO.input(26)
    while True:
        src_dev = ""
        dest_dev = ""
        usb_links = glob.glob(dev_path)
        if not usb_links:
            time.sleep(1)
            continue
        #print(len(usb_links))
        if len(usb_links) <= 2:
            lcd.message("Insert Pendrive")
            time.sleep(0.5)
            lcd.clear()
            continue
        for devs in usb_links:
            if src.lower() in devs.lower():
                src_dev = os.readlink(devs).split('/')[-1]
            if dest.lower() in devs.lower():
                dest_dev = os.readlink(devs).split('/')[-1]

        if src_dev and dest_dev:
            copy(src_dev, dest_dev)
            #print(src_dev+"*****")
            break
while True:
     flag=0
     lcd.clear()
     lcd.message("Enter Button")
     main()
     # print("print")
