import sqlite3
import cv2
from flask import Flask, render_template,jsonify, request, g #json for convertion, request obvious and g for storing data(typically databvase)
import socket

width = 1280
height = 720
camera_id = 0
delay = 1
window_name = 'OpenCV QR Code'

qcd = cv2.QRCodeDetector()
cam = cv2.VideoCapture(camera_id)

cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,15)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

def get_db():
    
    db=sqlite3.connect("sia.db")
    return db
        
    
def scan_qr(qr_code):
    db = get_db()
    cursor = db.cursor() # something that allows interaction with the database
    
    cursor.execute('SELECT shape, x_position, y_position FROM qr_positions WHERE qr_data = ?', (qr_code,))
    result = cursor.fetchone()

    if result:
        shape, x_pos, y_pos = result  
        return shape, x_pos, y_pos
    return None  
        
def qr_func(ret,frame):
    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    
                    result=scan_qr(s)
                    
                    if result:
                        shape, x_pos, y_pos = result
                        #print(f"Shape: {shape}, X: {x_pos}, Y: {y_pos}")
                        return x_pos,y_pos
                    
                 

get_db()
while True:
    
    ret, frame = cam.read()
    qr_func(ret,frame)
    #print(qr_func(ret,frame))
    
    cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyWindow(window_name)
