
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
#pin = 12

#GPIO.setup(pin,GPIO.OUT)
#GPIO.output(pin, GPIO.HIGH)
#time.sleep(1)
#GPIO.cleanup()


#def set_motors(value_dir1, value_dir2, value_pwm1, value_pwm2):
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
	
GPIO.output(dir1_pin, GPIO.HIGH) #right forward
GPIO.output(dir2_pin, GPIO.LOW)	#left forward
pwm1.ChangeDutyCycle(50)
pwm2.ChangeDutyCycle(50)
time.sleep(3)
pwm1.ChangeDutyCycle(100)
pwm2.ChangeDutyCycle(100)
time.sleep(3)
GPIO.cleanup()
