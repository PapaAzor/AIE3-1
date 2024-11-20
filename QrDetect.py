from picamera2 import Picamera2
import cv2
import socket
from pyzbar.pyzbar import decode
import numpy as np

# Camera settings
width = 1280
height = 720
window_name = 'PiCamera QR Code'
delay = 1

# TCP server settings (C server)
SERVER_IP = '192.168.156.196'  # IP address of the C server
PORT = 8000  # Port used by the C server

# Function to send data to the C server via TCP
def send_to_c_server(data):
    try:
        # Create a socket and connect to the C server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))
        sock.sendall(data.encode())  # Send QR data as a string
        sock.close()  # Close the socket after sending the data
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
    """Processes the frame to detect QR codes."""
    decoded_info = decode(frame)
    if decoded_info:
        for obj in decoded_info:
            qr_data = obj.data.decode('utf-8')
            print(f"Detected QR Code: {qr_data}")
            
            # Send QR data to C server
            send_to_c_server(qr_data)
            
            # Draw bounding box around detected QR code
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
    return frame

# Main loop
try:
    while True:
        # Capture frame from PiCamera
        frame = piCam.capture_array()

        # Process the frame for QR codes
        frame = qr_func(frame)

        # Display the frame
        cv2.imshow(window_name, frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
finally:
    # Cleanup
    piCam.stop()
    cv2.destroyAllWindows()
