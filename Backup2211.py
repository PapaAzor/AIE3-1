# na chama backup tego co pisal piotrek (na wypadek zjarania maliny, odpukac)
# 
#
#
#----------------------------robotclass.py----------------------------------
import time
import threading
class Robot:
	def __init__(self):
		self.movement_state = 'unmodified' #movement state is changed by dot tracking and represents how the lift should go to have the dot in the center (or re if it has reached it)
		self.movement_state_lock = threading.Lock()
		self.rotation_angle = 0
		self.rotation_angle_lock = threading.Lock()
		self.rotation_target = 0 #rotation target can only be 0/90/-90
		self.rotation_target_lock = threading.Lock()
		
		#for movement logic
		self.movement_array = 0
		self.new_movement_array = False
		self.new_movement_array_lock = threading.Lock()
	
	def update_movement_array(self, array):
		while self.movement_array != array:
			with self.new_movement_array_lock:
				self.movement_array = array
			time.sleep(0.001)
	def change_rotation_target(self, new_target):
		while self.rotation_target != new_target:
			with self.rotation_target_lock:
				self.rotation_target = new_target
			time.sleep(0.001)
	def change_movement_state(self, new_state):
		while self.movement_state != new_state:
			with self.movement_state_lock:  # Acquire lock
				self.movement_state = new_state
			time.sleep(0.001)  # Allow other threads to run
				
	def change_rotation_angle(self, new_rotation_value):
		while self.rotation_angle != new_rotation_value:
			with self.rotation_angle_lock:  # Acquire lock
				self.rotation_angle = new_rotation_value
			time.sleep(0.001)  # Allow other threads to run
	
	def get_movement_array(self):
		with self.movement_array_lock:
			return self.movement_array
	def get_movement_state(self):
		with self.movement_state_lock:  # Acquire lock
			return self.movement_state
	def get_rotation_value(self):
		with self.rotation_angle_lock:  # Acquire lock
			return self.rotation_angle
	def get_rotation_target(self):
		with self.rotation_target_lock:  # Acquire lock
			return self.rotation_target
#-----------------function_dot_tracker.py---------------
import cv2
from time import sleep
from numpy import array
from picamera2 import Picamera2


def dot_tracker(piCam, tracking_object):
    x = 0
    y = 0
    w = 0
    h = 0
    HEIGHT = 360
    WIDTH = 640
    hueBOT = 40
    hueTOP = 64
    satBOT = 123
    satTOP = 195
    valBOT = 120
    valTOP = 215
    while tracking_object.movement_state != 'reached':
        frame = piCam.capture_array()
        frame = cv2.resize(frame, (WIDTH,HEIGHT))
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #frameHSV = cv2.GaussianBlur(frameHSV, (3,3),5)
        bot_bound = array([hueBOT,satBOT,valBOT])
        top_bound = array([hueTOP,satTOP,valTOP])
        mask1 = cv2.inRange(frameHSV,bot_bound,top_bound)
        contours, junk = cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        coordinates = []
        if len(contours) != 0:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:
                    x,y,w,h = cv2.boundingRect(contour)
                if i == 0:
                    coordinates = [x,y,w,h]
                    distance_coordinates = int(abs((WIDTH/2)-(x+w)))
                    saved_contour = contour
                    i+=1
                else:
                    distance_current = int(abs((WIDTH/2)-(x+w)))
                    if distance_current < distance_coordinates:
                        coordinates = [x,y,w,h]
                        distance_coordinates = distance_current
                        saved_contour = contour
           
            object_position_x = int(coordinates[0]+0.5*coordinates[2])
            object_position_y = int(coordinates[1]+0.5*coordinates[3])
            distance_from_middle = int(object_position_x-(WIDTH/2))
           
            cv2.drawContours(frame,[saved_contour],0,(0,0,255),2)
            cv2.rectangle(frame,(coordinates[0],coordinates[1]),(coordinates[0]+coordinates[2],coordinates[1]+coordinates[3]),(0,0,255),2)
           
            reached_border_value = int(0.8*HEIGHT)
            cv2.line(frame,(int(WIDTH/2),0),(int(WIDTH/2),HEIGHT),(0,0,255),1)
            cv2.line(frame, (0,reached_border_value),(WIDTH,reached_border_value),(0,0,255),1)

            cv2.line(frame,(int(WIDTH/2),reached_border_value),(object_position_x,object_position_y),(0,255,0),2)
    
            cv2.imshow('0',mask1)
            if object_position_y  > reached_border_value:
                tracking_object.change_movement_state('reached')#here the tracker will terminate and return a that we have reached the next dot
                print('reached')
            else:
                tracking_object.chnage_movement_state('not_reached')
                print('not_reached')
        sleep(0.5)
#-----------------------------main.py-----------------------------------------
import cv2
import time
from numpy import array
from picamera2 import Picamera2
import threading
from function_dot_tracker import dot_tracker
from RobotClass import Robot
import serial
from function_serial_reader import serial_read
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


#dot_tracking_thread = threading.Thread(target=dot_tracker, args=(piCamera,orzel))
#dot_tracking_thread.start()


serial_read_thread = threading.Thread(target=serial_read, args=(orzel,ser))
serial_read_thread.start()

#print(orzel.rotation_angle)
#print(orzel.movement_state)
cv2.destroyAllWindows()

#-------------------------function_serial_reader.py-----------------------------------
import serial
import time

def serial_read(orzel,serial):
	calibrated = False
	while True:
		if serial.in_waiting > 0:
			msg = serial.readline().decode('utf-8', errors='ignore').rstrip()
			print(msg)		
			if msg == "666":
				calibrated = True
				print('calibration complete')
			if calibrated:
				orzel.change_rotation_angle(msg)
				print(msg)

#---------------------movement_logic_file.py-----------------------------
import time
def movement_logic(orzel):
	array = 0
	while True:
		if orzel.new_movement_array = True:
			array = orzel.get_movement_array()
			orzel.new_movement_array = False
			#here we will lopp throught the array and set an appropriate target roation value, then set movement state to \not reached\
			i=0
			for i in range(0,len(array)):
				direction = array[i]
				current_target = orzel.get_rotation_target()
				if direction == 'F':
					pass
				else if direction == 'L':
					orzel.change_rotation_target(current_target+90)
				else if direction == 'R':
					orzel.change_rotation_target(current_target-90)
				else if direction == 'T':
					orzel.change_rotation_target(current_target+180)
				else:
					#tutaj odpala sie logika do paczki
					#trzeba bedzie zmienic thread to kamery zeby patrzyl na wartosc nowej zmiennej w obiekcie i w ten sposob decydowal czy odpala tracking czy QR detection
					pass
		
		
		
		
		
		else:
			time.sleep(0.3)
			
#--------------------------------movement_file.py---------------------------------
import RPi.GPIO as GPIO

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
pwm1.start(0)
pwm2.start(0)

timer = 0
rotationTarget = 0
rotationActual = 0 # this to be replaced with rotation angle from object
rotationError = 0
rotationErrorOld = 0
rotationErrorChange = 0
rotationErrorDerivative = 0
rotationErrorArea = 0

timeOld = 0
timeNew = 0
dt = 0
k1 = 15
k2= 500
k3 =0.3

def movement_control(orzel):
	#setup
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
	pwm1.start(0)
	pwm2.start(0)

	timeOld = 0
	timeNew = 0
	dt = 0
	k1 = 15
	k2= 500
	k3 =0.3
	GPIO.output(dir1_pin,GPIO.HIGH)#right wheel forward when high
	GPIO.output(dir2_pin,GPIO.LOW) #left wheel forward when low
	
	#function proper
	while True:
		timer = 0
		rotationTarget = orzel.get_rotation_target()
		rotationError = 0
		rotationErrorOld = 0
		rotationErrorChange = 0
		rotationErrorDerivative = 0
		rotationErrorArea = 0
	
		while orzel.get_movement_state() != 'reached':
			rotationActual = orzel.get_rotation_angle()
			timeOld = timeNew
			timeNew = time.time()
			dt = timeNew - timeOld
			rotationError = rotationTarget - rotationAcual
			rotationErrorChange = rotationError - rotationErrorOld
			rotationErrorDerivative = rotationErrorChange/dt
			rotationErrorArea = rotationError*dt
			
			pwm1Value = 140+ (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
			pwm1Value = max(0,min(pwm1Value,100))
			pwm1DutyCycle = int(pwm1Value/255)*100
			pwm2Value = 140 - (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
			pwm2Value = max(0,min(pwm2Value,100))
			pwm1DutyCycle = int(pwm2Value/255)*100
			pwm12DefaultDutyCycle = 54
			
			if abs(rotationError) == 0:
				pwm1.ChangeDutyCycle(pwm1DutyCycle)
				pwm2.ChangeDutyCycle(pwm2DutyCycle)
			if abs(rotationError) == 0:
				pwm1.changeDutyCycle(pwm12DefaultDutyCycle)
				pwm2.changeDutyCycle(pwm12DefaultDutyCycle)
			
			time.sleep(0.005)
			rotationErrorOld = rotationError
		#here we have some code with delay to move towards dot for a while
		
		
		#orzel.change_movement_state('not reached')# this need to go to movement logic
#--------------------------------------------------------------------------------------------
