import serial
import time
def serial_read(orzel,serial):
	print('starting calibration')
	while True:
		if serial.in_waiting > 0:
			msg = serial.readline().decode('utf-8', errors='ignore').rstrip()
			#print(msg)
			if msg == '666':
				orzel.calibrate(True)
				print('calibration complete')
				break
	#print('2nd loop')
	while True:
		if serial.in_waiting > 0:
			msg = serial.readline().decode('utf-8', errors='ignore').rstrip()
			orzel.change_rotation_angle(float(msg))
			
			#print(orzel.get_rotation_angle())
