import cv2
import time
from numpy import array
from picamera2 import Picamera2
import threading
from function_dot_tracker import dot_tracker
from RobotClass import Robot
import serial
from function_serial_reader import serial_read
from movement_file import movement_control
import RPi.GPIO as GPIO
from logic_file import logic
#----------------- SETTING PICAM-----------------------

GPIO.setmode(GPIO.BOARD)
dir1_pin= 37
dir2_pin = 33			# 1 - RIGHT WHEEL, FORWARD WHEN HIGH
pwm1_pin = 35			# 2 - LEFT WHEEL, BACKWARD WHEN HIGH
pwm2_pin = 31

GPIO.setup(dir1_pin,GPIO.OUT)
GPIO.setup(dir2_pin,GPIO.OUT)
GPIO.setup(pwm1_pin,GPIO.OUT)
GPIO.setup(pwm2_pin,GPIO.OUT)
pwm1 = GPIO.PWM(pwm1_pin, 100)
pwm2 = GPIO.PWM(pwm2_pin, 100)
GPIO.output(dir1_pin, GPIO.HIGH) #right forward
GPIO.output(dir2_pin, GPIO.LOW)	#left forward
pwm1.start(0)
pwm2.start(0)

pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(0)

piCamera=Picamera2()
piCamera.preview_configuration.main.size=(1920,1080)
piCamera.preview_configuration.main.format="RGB888"
piCamera.preview_configuration.align()
piCamera.configure("preview")
piCamera.start()

#this creates a thread tasked with running dot_tracker function
orzel = Robot()
#preparing serial
ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
ser.flush()
#--------

#-------- trzeba teraz dodac moj Robot.c i zrobic dzielenie zmiennej od strony pytona bo w c 
dot_tracking_thread = threading.Thread(target=dot_tracker, args=(piCamera,orzel))
serial_read_thread = threading.Thread(target=serial_read, args=(orzel,ser))
logic_thread = threading.Thread(target=logic, args=(orzel,))
logic_thread.start()
dot_tracking_thread.start()
serial_read_thread.start()

while orzel.if_calibrated() == False:
		time.sleep(1)
movement_control_thread = threading.Thread(target=movement_control,args=(orzel,pwm1,pwm2))
movement_control_thread.start()
#print(orzel.rotation_angle)
#print(orzel.movement_state)
cv2.destroyAllWindows()

