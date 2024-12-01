import cv2
from time import sleep
from numpy import array
from picamera2 import Picamera2


def dot_tracker(piCam, tracking_object):
    while True:
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
        
        if (tracking_object.get_movement_state()== 'forward'):
            print('dot tracker - ON')
            sleep(0.1) # sleep HAS to be here
            while tracking_object.get_movement_state() == 'forward':
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
                       
                    reached_border_value = int(0.9*HEIGHT)
                    cv2.line(frame,(int(WIDTH/2),0),(int(WIDTH/2),HEIGHT),(0,0,255),1)
                    cv2.line(frame, (0,reached_border_value),(WIDTH,reached_border_value),(0,0,255),1)

                    cv2.line(frame,(int(WIDTH/2),reached_border_value),(object_position_x,object_position_y),(0,255,0),2)
                
                    if object_position_y  > reached_border_value:
                        tracking_object.change_movement_state('pulling_up')#here the tracker will terminate and return a that we have reached the next dot
                        print('dot reached, tracker OFF')
                    else:
                        tracking_object.change_movement_state('forward')
        
                sleep(0.05)
