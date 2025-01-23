import RPi.GPIO as GPIO
import time
import csv
def movement_control(orzel,pwm1,pwm2):
	
	#GPIO.setmode(GPIO.BOARD)
	dir1_pin= 29
	dir2_pin = 33			# 1 - RIGHT WHEEL, FORWARD WHEN HIGH
	pwm1_pin = 35			# 2 - LEFT WHEEL, BACKWARD WHEN HIGH
	pwm2_pin = 31
	pwm1.ChangeDutyCycle(0)
	pwm2.ChangeDutyCycle(0)
	
	timeOld = 0
	timeNew = 0
	dt = 0
	k1 = 15
	k2= 0.85
	k3 =0.025
	GPIO.output(dir1_pin,GPIO.LOW)#LEFT wheel forward when LOW
	GPIO.output(dir2_pin,GPIO.HIGH) #RIGHT wheel forward when HIGH
	

	#function proper
	pullingUpCurTime=0
	while True:
		pwm1Value = 0
		pwm2Value = 0
		timer = 0
		rotationError = 0
		rotationErrorOld = 0
		rotationErrorChange = 0
		rotationErrorDerivative = 0
		rotationErrorArea = 0
		turning_right = False
		turning_left = False
	
			#rotationTarget = orzel.get_rotation_target()
		if (orzel.get_movement_state() != 'request' and orzel.get_movement_state() != 'package') :
			rotationTarget = orzel.get_rotation_target()
			
			if orzel.get_movement_state() == 'turn_right':
				print('right turn ON')
				turning_right = True
				GPIO.output(dir1_pin, GPIO.LOW) #right backward
				GPIO.output(dir2_pin, GPIO.LOW)	#left forward
				orzel.change_movement_state('forward')
			elif orzel.get_movement_state() == 'turn_left':
				print('turn left ON')
				turning_left = True
				GPIO.output(dir1_pin, GPIO.HIGH) #right forward
				GPIO.output(dir2_pin, GPIO.HIGH) #left backward
				orzel.change_movement_state('forward')
				
			while orzel.get_movement_state() == 'forward' : #or orzel.get_movement_state()=="pulling_up
				rotationActual = orzel.get_rotation_angle()
				print(rotationActual)
				timeOld = timeNew
				timeNew = time.time()
				dt = timeNew - timeOld
				rotationError = rotationTarget - rotationActual
				rotationErrorChange = rotationError - rotationErrorOld
				rotationErrorDerivative = rotationErrorChange/dt
				rotationErrorArea = rotationError*dt
				
				
				if (orzel.get_movement_state() == 'forward'): 
					#print(rotationActual)
					if ((turning_right == True) and (rotationError > -20)): #check if we have turned
						print('right turn OFF')
						turning_right = False
						GPIO.output(dir1_pin, GPIO.LOW) #right forward
						GPIO.output(dir2_pin, GPIO.HIGH)	#left forward
					if ((turning_left == True) and (rotationError < 20)): #check if we have turned
						print('left turn OFF')
						turning_left = False
						GPIO.output(dir1_pin, GPIO.LOW) #right forward
						GPIO.output(dir2_pin, GPIO.HIGH)	#left forward
							
					if ((turning_right == True) or (turning_left == True)):	
						pwm1Value = 0.3*abs((k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea))
						pwm2Value = 0.3*abs((k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea))
						pwm1Value = max(30,min(pwm1Value,255))
						pwm2Value = max(30,min(pwm1Value,255))
						
					else:#forward
						pwm1Value = 120+ (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
						pwm2Value =  120  - (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
						pwm1Value = max(0,min(pwm1Value,255))
						pwm2Value = max(0,min(pwm2Value,255))
					pwm1DutyCycle = int(float(pwm1Value/255)*100)
					pwm2DutyCycle = int(float(pwm2Value/255)*100)
					#pwm12DefaultDutyCycle = 27
					pwm2.ChangeDutyCycle(pwm1DutyCycle)#ZMIANA 1 NA 2
					pwm1.ChangeDutyCycle(pwm2DutyCycle)
					if turning_left == True:
						#print(rotationActual)
						#print(f'PWM1 = {pwm1DutyCycle}, PWM2 = {pwm2DutyCycle}')
						#pwm1.ChangeDutyCycle(0)
						#pwm2.ChangeDutyCycle(0)
						pass #co tutaj???
						#time.sleep(0.5)
				#print(rotationActual)
				'''
				if (orzel.get_movement_state() == 'pulling_up'): 
					pullinUpRot = orzel.get_rotation_angle()
					
					
					if pullingUpCurTime == 0:
						print('pulling up')
						pullingUpStartTime = time.time()
					else:
						pass

					if pullingUpCurTime < 2.95:
						pullingUpEndTime = time.time()
						pullingUpCurTime = pullingUpEndTime - pullingUpStartTime
						
						
					else:
						pullingUpCurTime = 0
						print('pulled up, requesting new command')
						orzel.change_movement_state('request')
					
				'''
				time.sleep(0.005)
				rotationErrorOld = rotationError
					
			
			
			pwm1.ChangeDutyCycle(27)
			pwm2.ChangeDutyCycle(27)
			time.sleep(2.95)
			pwm1.ChangeDutyCycle(0)
			pwm2.ChangeDutyCycle(0)
			print('pulled up, requesting new command')
			orzel.change_movement_state('request')
			time.sleep(.3)
			
			
			'''
			if(orzel.get_movement_state() == 'pulling_up'):
			
				
				rotationTarget = orzel.get_rotation_target()
				rotationActual = orzel.get_rotation_angle()
				while(orzel.get_movement_state() == 'pulling_up'):
					
					
					myTime=time.time()-startTime
					with open(csv_file_path, mode='a', newline='') as file:
						writer=csv.writer(file)
						#writer.writerow(["time","error"])
						writer.writerow([myTime,rotationError])
					
					
					
					rotationActual = orzel.get_rotation_angle()
					print(rotationActual)
					timeOld = timeNew
					timeNew = time.time()
					dt = timeNew - timeOld
					rotationError = rotationTarget - rotationActual
					rotationErrorChange = rotationError - rotationErrorOld
					rotationErrorDerivative = rotationErrorChange/dt
					rotationErrorArea = rotationError*dt	
					pwm1Value = 70+ (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
					pwm2Value =  70  - (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
					pwm1Value = max(0,min(pwm1Value,255))
					pwm2Value = max(0,min(pwm2Value,255))
					pwm1DutyCycle = int(float(pwm1Value/255)*100)
					pwm2DutyCycle = int(float(pwm2Value/255)*100)
					pwm2.ChangeDutyCycle(pwm1DutyCycle)#ZMIANA 1 NA 2
					pwm1.ChangeDutyCycle(pwm2DutyCycle)
					time.sleep(0.005)
					rotationErrorOld = rotationError
					
				
					
					pullingUpEndTime=time.time()
					pullingUpCurTime=pullingUpEndTime-pullingUpStartTime
					rotationActual = orzel.get_rotation_angle()
					print("I got rotation: ",rotationActual," and time: ",pullingUpCurTime)
					time.sleep(0.05)
					if(pullingUpCurTime>=6*2.95):
						break
			print('pulled up, requesting new command')
			orzel.change_movement_state('request')
			#tutaj ja zapodaje i nie testuje 
		'''
		
			
				
		#while orzel.get_movement_state() == 'request':
			#time.sleep(0.05)
		
		
		
		
		
		#this is where i tried to pull up with control
		'''
		we_are_pulling_up = False
		pulling_up_timer = 0
		#timertest = time.time()#debug purpose
		while orzel.get_action() != 'request':
			rotationTarget = orzel.get_rotation_target()
			while ((orzel.if_dot_detected() == False) or ((we_are_pulling_up == True) and (time.time()-pulling_up_timer < 3.25))): #do zmiany na reached dot
			#while ((time.time()-timertest < 2) or ((we_are_pulling_up == True) and (time.time()-pulling_up_timer < 4))): #debug purposes
				rotationActual = orzel.get_rotation_angle()
				if we_are_pulling_up == True:
					print(rotationActual)
				timeOld = timeNew
				timeNew = time.time()
				dt = timeNew - timeOld
				rotationError = rotationTarget - rotationActual
				rotationErrorChange = rotationError - rotationErrorOld
				rotationErrorDerivative = rotationErrorChange/dt
				rotationErrorArea = rotationError*dt
					
				pwm1Value = 70+ (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm1Value = max(0,min(pwm1Value,255))
				pwm1DutyCycle = int(float(pwm1Value/255)*100)
				pwm2Value =  70  - (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm2Value = max(0,min(pwm2Value,255))
				pwm2DutyCycle = int(float(pwm2Value/255)*100)
				pwm12DefaultDutyCycle = 27

				if abs(rotationError) > 0:
					pwm1.ChangeDutyCycle(pwm1DutyCycle)
					pwm2.ChangeDutyCycle(pwm2DutyCycle)
				if abs(rotationError) == 0:
					pwm1.ChangeDutyCycle(pwm12DefaultDutyCycle)
					pwm2.ChangeDutyCycle(pwm12DefaultDutyCycle)
				time.sleep(0.005)
				rotationErrorOld = rotationError
			#here we pull up
			if we_are_pulling_up == False:
				pulling_up_timer = time.time()
				we_are_pulling_up = True
				print('pulling up')
			if (time.time()-pulling_up_timer) > 3.25:
				print('I pulled up, requesting new command')
				orzel.change_action('request')
				pwm1.ChangeDutyCycle(0)
				pwm2.ChangeDutyCycle(0)
				
		while orzel.get_action == 'request':
			time.sleep(1)
		'''
		
		'''
	#=======================TURN LEFT=======================================================
		elif orzel.get_movement_state() == 'turn_left':
			print('enetring turn left function')
			GPIO.output(dir1_pin,GPIO.HIGH)#right wheel forward when high
			GPIO.output(dir2_pin,GPIO.HIGH) #left wheel backward when high
			
			rotationTarget = orzel.get_rotation_target()
			rotationActual = orzel.get_rotation_angle()
			rotationError = rotationTarget - rotationActual
			while rotationError > 3: #left is 90deg  
				time.sleep(0.005)
				rotationActual = orzel.get_rotation_angle()
				timeOld = timeNew
				timeNew = time.time()
				dt = timeNew - timeOld
				rotationError = rotationTarget - rotationActual
				rotationErrorChange = rotationError - rotationErrorOld
				rotationErrorDerivative = rotationErrorChange/dt
				rotationErrorArea = rotationError*dt
				
				pwm1Value = (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm1Value = max(0,min(pwm1Value,255))
				pwm1DutyCycle = int(float(pwm1Value/255)*100)
				pwm2Value = (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm2Value = max(0,min(pwm2Value,255))
				pwm2DutyCycle = int(float(pwm2Value/255)*100)
				pwm1.ChangeDutyCycle(pwm1DutyCycle)
				pwm2.ChangeDutyCycle(pwm2DutyCycle)
				
				rotationErrorOld = rotationError
			pwm1.ChangeDutyCycle(0)
			pwm2.ChangeDutyCycle(0)
			print('turning left finshed, requesting new command')
			orzel.change_movement_state('request')
			time.sleep(1)
	#==============================TURN RIGHT==============================
		elif orzel.get_movement_state() == 'turn_right':
			print('entering turn right function')
			pwm1.ChangeDutyCycle(0)
			pwm2.ChangeDutyCycle(0)
			GPIO.output(dir1_pin,GPIO.LOW)#right wheel backward when low
			GPIO.output(dir2_pin,GPIO.LOW) #left wheel forward when low
			rotationTarget = orzel.get_rotation_target()
			rotationActual = orzel.get_rotation_angle()
			rotationError = rotationTarget - rotationActual
			print(rotationError)
			print('entered loop')
			while rotationError < -3:
				rotationActual = orzel.get_rotation_angle()
				timeOld = timeNew
				timeNew = time.time()
				dt = timeNew - timeOld
				rotationError = rotationTarget - rotationActual
				rotationErrorChange = rotationError - rotationErrorOld
				rotationErrorDerivative = rotationErrorChange/dt
				rotationErrorArea = rotationError*dt
				
				print(f"rotationError ={rotationError}, rotationAngle = {rotationActual}")
				
				pwm1Value = (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm1Value = max(0,min(pwm1Value,255))
				pwm1DutyCycle = int(float(pwm1Value/255)*100)
				pwm2Value = (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm2Value = max(0,min(pwm2Value,255))
				pwm2DutyCycle = int(float(pwm2Value/255)*100)
				pwm1.ChangeDutyCycle(pwm1DutyCycle)
				pwm2.ChangeDutyCycle(pwm2DutyCycle)
				time.sleep(0.005)
				rotationErrorOld = rotationError
			pwm1.ChangeDutyCycle(0)
			pwm2.ChangeDutyCycle(0)
			print('turning right finshed, requesting new command')
			orzel.change_movement_state('request')
			time.sleep(1)
	#============================TURN AROUND========================================
		elif orzel.get_movement_state() == 'turn_around':
			print('enetring turn around function')
			GPIO.output(dir1_pin,GPIO.LOW)#right wheel backward when low
			GPIO.output(dir2_pin,GPIO.LOW) #left wheel forward when low
			
			rotationTarget = orzel.get_rotation_target()
			rotationActual = orzel.get_rotation_angle()
			rotationError = rotationTarget - rotationActual
			while rotationError < -3:
				time.sleep(0.005)
				rotationActual = orzel.get_rotation_angle()
				timeOld = timeNew
				timeNew = time.time()
				dt = timeNew - timeOld
				rotationError = rotationTarget - rotationActual
				rotationErrorChange = rotationError - rotationErrorOld
				rotationErrorDerivative = rotationErrorChange/dt
				rotationErrorArea = rotationError*dt
				
				pwm1Value = (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm1Value = max(0,min(pwm1Value,255))
				pwm1DutyCycle = int(float(pwm1Value/255)*100)
				pwm2Value = (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
				pwm2Value = max(0,min(pwm2Value,255))
				pwm2DutyCycle = int(float(pwm2Value/255)*100)
				pwm1.ChangeDutyCycle(pwm1DutyCycle)
				pwm2.ChangeDutyCycle(pwm2DutyCycle)
				
	
				rotationErrorOld = rotationError
			pwm1.ChangeDutyCycle(0)
			pwm2.ChangeDutyCycle(0)
			print('turning around finished, requesting new command')
			orzel.change_movement_state('request')
			time.sleep(1)'''
