from flask import Flask, render_template,jsonify, request, g #json for convertion, request obvious and g for storing data(typically databvase)
import socket
import sqlite3

app = Flask(__name__)

ROBOT_IP = '192.168.0.100'  #example
ROBOT_PORT = 8000  #port for the TCP server

def get_db():
    if 'db' not in g:
        g.db=sqlite3.connect("sia.db")
        return g.db 
    
@app.teardown_appcontext#func called after every request (event if there was an error)
def close_db(exception): #Exception because of a standard practice
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

#sends commands 
def send_command(command):
    #use socket.socket(addr,type) then connect and send 
#    try:
#        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#            s.connect((ROBOT_IP, ROBOT_PORT))
#            s.sendall(command.encode('utf-8'))

    #print(f"Simulating sending command: {command}")
    pass

startSet=False
endSet=False
resetSet=False
endPoint=[0,0]
startPoint=[0,0]

@app.route('/move/<endpoint>')
def move(endpoint):
    endPoint[0]=endpoint[0]
    endPoint[1]=endpoint[2]#endpoint is sent as a string I guess so [1] would return a ','
    global endSet
    endSet=True
    
    send_command(endpoint)
    #print("Received data:", endpoint) 
    findingWay(startPoint,endPoint)
    return {"status": "success", "message": f"Command received: {endpoint}"}, 200 
    
@app.route('/setStartingPosition/<coordinates>')
def setStartingPosition(coordinates):
    
    startPoint[0]=coordinates[0]
    startPoint[1]=coordinates[2]#same as for endpoint
    global startSet
    startSet= True
    x, y = coordinates.split(',')
    findingWay(startPoint,endPoint)
    #print(f"Starting position received: ", coordinates)
    return f"Starting position set to ({x}, {y})"


def findingWay(start,end):
    if(startSet==True and endSet==True):
        print("Need to find way from: ",startPoint," to: ",endPoint)
    else :
        #print("endpoint:", endPoint)
        #print(endSet)
        #print("starPoint: ",startPoint)
        #print(startSet)
        pass
    

#reset function
@app.route('/reset/<resetSet>')
def reset(resetSet):
    global startSet
    global startPoint
    global endSet
    global endPoint
    print(f"received reset request with : {resetSet}")
    
    endPoint=[0,0]
    startPoint=[0,0]
    startSet=False
    endSet=False
    resetSet=0
    print("stratpoint:",startSet)
    print("endpoint:",endSet)
    return f"Reset set to {resetSet}"
  


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
