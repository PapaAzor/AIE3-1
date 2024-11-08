from flask import Flask, render_template, jsonify, request, g
import socket
import sqlite3

app = Flask(__name__)

# TCP configuration for the C server
TCP_IP = '192.168.28.196'  # IP for the C server
ROBOT_PORT = 8000          # Port for the C server

# Database configuration
DATABASE = "sia.db"

def get_db():
    
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Close the database connection after request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def send_to_c_server(data):
    """Sending to the c server"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_IP, ROBOT_PORT))
            s.sendall(data.encode())
        return "Data sent successfully"
    except Exception as e:
        return f"Failed to send data: {e}"

@app.route('/')
def index():
    return render_template('index.html')

# Variables to track starting and ending positions
start_set = False
end_set = False
start_point = [0, 0]
end_point = [0, 0]

@app.route('/move/<endpoint>')
def move(endpoint):
    """Set the end point and send the move command to the C server."""
    global end_set, end_point
    try:
        x, y = map(int, endpoint.split(','))
        end_point = [x, y]
        end_set = True
        send_to_c_server('e'+endpoint)  # Send endpoint data to the C server
        finding_way()
        return {"status": "success", "message": f"Command received: {endpoint}"}, 200
    except ValueError:
        return {"status": "error", "message": "Invalid endpoint format"}, 400

@app.route('/setStartingPosition/<coordinates>')
def set_starting_position(coordinates):
    
    global start_set, start_point
    try:
        x, y = map(int, coordinates.split(','))
        start_point = [x, y]
        start_set = True
        send_to_c_server('s'+str(start_point))
        finding_way()
        return {"status": "success", "message": f"Starting position set to ({x}, {y})"}, 200
    except ValueError:
        return {"status": "error", "message": "Invalid coordinates format"}, 400

def finding_way():
    
    if start_set and end_set:
        print(f"Need to find way from: {start_point} to: {end_point}")

@app.route('/reset')
def reset():
    
    global start_set, end_set, start_point, end_point
    start_point = [0, 0]
    end_point = [0, 0]
    start_set = False
    end_set = False
    return {"status": "success", "message": "Navigation reset successful"}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
