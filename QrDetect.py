from picamera2 import Picamera2
import cv2
import socket
from pyzbar.pyzbar import decode #bacause opencv's QR decode didnt work without building from scratch 
import numpy as np
import sys  #  for clean exit
import time

# Camera settings
width = 1280
height = 720
window_name = 'PiCamera QR Code'
delay = 1
QrDetected=0


SERVER_IP = '192.168.156.196' 
PORT = 8000  


def send_to_c_server(data):
    try:
        #pass the socket
        shared_socket_fd = int(sys.argv[1])  
        print(f"Using shared socket FD: {shared_socket_fd}")
        
        shared_socket = socket.fromfd(shared_socket_fd, socket.AF_INET, socket.SOCK_STREAM)    
        shared_socket.sendall(data.encode())
        print("Data sent to C server: ", data)
    except Exception as e:
        print(f"Failed to send data to server: {e}")

# Initialize Picamera2
piCam = Picamera2()

# Configure the camera
piCam.preview_configuration.main.size = (width, height)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

def qr_func(frame):
    global QrDetected  # Declare QrDetected as global
    """Processes the frame to detect QR codes."""
    decoded_info = decode(frame)
    if decoded_info:
        for obj in decoded_info:
            qr_data = obj.data.decode('utf-8')
            print(f"Detected QR Code: {qr_data}")
            
            send_to_c_server(qr_data)
            
            # Draw bounding box around detected QR code
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            QrDetected = 1 
                        
    return frame

try:
    while True:
        
        frame = piCam.capture_array()
        frame = qr_func(frame)

        cv2.imshow(window_name, frame)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
        if(QrDetected==1):
            break
finally:
    # Cleanup
    piCam.stop()
    cv2.destroyAllWindows()
    sys.exit(0)  # Ensure exit in case of failure
