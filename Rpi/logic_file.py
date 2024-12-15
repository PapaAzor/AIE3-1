import time
def logic(orzel):
	while orzel.if_calibrated() != True:
		time.sleep(1)
	#orzel.update_movement_array(['F','R','F','R','F','T','F','L']) 
	orzel.update_movement_array(['F','L']) 
	orzel.change_rotation_target(0)  #program zaczyna sie od domyslnie 0 stopni - forward
	orzel.new_movement_array = True #tu trzeba dorobic thread safe funkcje w klasie 
	while True:
		if orzel.new_movement_array == True:
			array = orzel.get_movement_array()
			print(array)
			orzel.new_movement_array = False
			i=0
			for i in range(0,len(array)): 
				while orzel.get_movement_state() != 'request':
					time.sleep(0.25)
				print('Movement state update started')
				command = array[i]
				current_target = orzel.get_rotation_target()
				if command == 'F':
					orzel.change_movement_state('forward')
					print(f"new movement_state = FORWARD , target = {orzel.get_rotation_target()}")
				elif command == 'L':
					orzel.change_rotation_target(current_target+90)
					orzel.change_movement_state('turn_left')
					print(f"new movement_state = TURN LEFT , target = {orzel.get_rotation_target()}")
				elif command == 'R':
					orzel.change_rotation_target(current_target-90)
					orzel.change_movement_state('turn_right')
					print(f"new movement state = TURN RIGHT, target = {orzel.get_rotation_target()}")
				elif command == 'T':
					orzel.change_rotation_target(current_target+180)
					orzel.change_movement_state('turn_around')
					print(f"turning around, target = {orzel.get_rotation_target()}")
				elif command == 'P':
					pass
					#print('switching into pickup mode')# or if currently in pickup mode, into drive mode
					#tutaj odpala sie logika do paczki
					#trzeba bedzie zmienic thread to kamery zeby patrzyl na wartosc nowej zmiennej w obiekcie i w ten sposob decydowal czy odpala tracking czy QR detection
				else:
					pass#raise error?
				#for debugging
				#orzel.change_action('request')
			while orzel.get_movement_state() != 'request':
				time.sleep(1)
			print('command array empty, waiting for new')
		
		
		else:
			time.sleep(0.3)
			
