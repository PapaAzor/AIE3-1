import RPi.GPIO as GPIO
import time
#this is here until we put it in main (when we put all together)
#this file will be a threaded function
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

#-----------------------------------------

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

def forward():
	#tutaj zabieramy wartoss z objektu do rotationactual, ktore zamniemy na orzel.rotation_value
	GPIO.output(dir1_pin,GPIO.HIGH)#right wheel forward when high
	GPIO.output(dir2_pin,GPIO.LOW) #left wheel forward when low
	timeOld = timeNew
	timeNew = time.time()
	dt = timeNew - timeOld
	rotationError = rotationTarget - rotationAcual
	rotationErrorChange = rotationError - rotationErrorOld
	rotationErrorDerivative = rotationErrorChange/dt
	rotationErrorArea = rotationError*dt
	
	pwm1Value = 140+ (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
	pwm1Value = max(0,min(pwm1Value,255))
	pwm1DutyCycle = int(pwm1Value/255)*100
	pwm2Value = 140 - (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea)
	pwm2Value = max(0,min(pwm2Value,255))
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
	
	
	
