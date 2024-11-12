start_x=1 #start x position
start_y=1 #start y position
cur_x=0 #current x position 
cur_y=0 #current y position

#pickup points 
pickup1_x=1 #target 1 x position
pickup1_y=1 #target 1 y position
pickup2_x=5 #target 2 x position
pickup2_y=4 #target 2 y position

#dropoff points 
dropoff1_x=7
dropoff1_y=2
dropoff2_x=1
dropoff2_y=1

#lenghts
lenghts1=0 #start to pickup 1

lenghts2=0 #start to pickup 2

lenght11=0 #from pickup 1 to dropoff 1

lenght22=0 #from pickup 2 to dropoff2

lenghtD1P2=0 # distance from dropoff1 to pickup2

lenghtD2P1=0 # distance from dropoff2 to pickup1

lenght=0
instructions=[]

def dist_fun(x1,y1,x2,y2):
    cur_x=x1
    cur_y=y1
    tar_x=x2
    tar_y=y2
    lenght=0
    while cur_x!=tar_x:
     while cur_y!=tar_y:
        if tar_y>cur_y:
            lenght+=1
            cur_y+=1
        if tar_y<cur_y:
            lenght+=1
            cur_y-=1  
     if tar_x>cur_x:
            lenght+=1
            cur_x+=1
     if tar_x<cur_x:
            lenght+=1
            cur_x-=1 
    return lenght

def dist_way(x1,y1,x2,y2):
    cur_x=x1
    cur_y=y1
    tar_x=x2
    tar_y=y2
    lenght=0
    while cur_x!=tar_x:
     while cur_y!=tar_y:
        if tar_y>cur_y:
            instructions.append('u')
            
            cur_y+=1
        if tar_y<cur_y:
            instructions.append('d')
            cur_y-=1  
     if tar_x>cur_x:
            instructions.append('r')
            cur_x+=1
     if tar_x<cur_x:
            instructions.append('l')
            cur_x-=1 


#lenghts
lenghts1=dist_fun(start_x, start_y,pickup1_x, pickup1_y) #start to pickup 1

lenghts2=dist_fun(start_x, start_y,pickup2_x, pickup2_y) #start to pickup 2

lenght11=dist_fun(pickup1_x, pickup1_y,dropoff1_x, dropoff1_y) #from pickup 1 to dropoff 1

lenght22=dist_fun(pickup2_x, pickup2_y,dropoff2_x, dropoff2_y) #from pickup 2 to dropoff 2

lenghtD1P2=dist_fun(dropoff1_x, dropoff1_y,pickup2_x, pickup2_y) # distance from dropoff1 to pickup2

lenghtD2P1=dist_fun(dropoff2_x, dropoff2_y,pickup1_x, pickup1_y) # distance from dropoff2 to pickup1

Way1=lenghts1+lenght11+lenghtD1P2+lenght22
Way2=lenghts2+lenght22+lenghtD2P1+lenght11
if Way1<=Way2: #write the instructions to follow path 1
        dist_way(start_x, start_y,pickup1_x, pickup1_y)
        dist_way(pickup1_x, pickup1_y,dropoff1_x, dropoff1_y)
        dist_way(dropoff1_x, dropoff1_y,pickup2_x, pickup2_y)
        dist_way(pickup2_x, pickup2_y,dropoff2_x, dropoff2_y)
else: #write the instructions to follow path 2
        dist_way(start_x, start_y,pickup2_x, pickup2_y)
        dist_way(pickup2_x, pickup2_y,dropoff2_x, dropoff2_y)
        dist_way(dropoff2_x, dropoff2_y,pickup1_x, pickup1_y)
        dist_way(pickup1_x, pickup1_y,dropoff1_x, dropoff1_y)
        
print(instructions)
drive=[]
def list_dir(instructions):
    direction='u'
    while(instructions.__len__()>0):
        first=instructions[0]
        instructions.pop(0)
        if(first==direction):
            drive.append('F')
        elif(first=='u'):
            if(direction=='l'):
                drive.append('R')
            if(direction=='r'):
                drive.append('L')
            if(direction=='d'):
                drive.append('T')
            direction='u'
                
        elif(first=='d'):
            if(direction=='l'):
                drive.append('L')
            if(direction=='r'):
                drive.append('R')
            if(direction=='u'):
                drive.append('T')
            direction='d'
                
        elif(first=='l'):
            if(direction=='d'):
                drive.append('R')
            if(direction=='u'):
                drive.append('L')
            if(direction=='r'):
                drive.append('T')
            direction='l'
                
        else:
            if(direction=='u'):
                drive.append('R')
            if(direction=='d'):
                drive.append('L')
            if(direction=='l'):
                drive.append('T')
            direction='r'

        
   
    
list_dir(instructions)
print(drive)