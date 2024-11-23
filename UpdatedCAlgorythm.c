#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
int mapway[2]={0,0};
char *startPos = argv[1];
int startPosReceived[3];
char *endPos = argv[2];
int endPosReceived[2];
char instructions[127]={'0'};
char drive[127]={'0'};
int a=0;
char direction = 'u'; // Initial direction
      

      for (int i = 0; i<2; i++) {
        startPosReceived[i] = startPos[i]- '0';  // Convert char to int by subtracting '0'
         printf("startPosReceived[%d] = %d\n", i, startPosReceived[i]);
    }
    
      for (int i = 0; i<2; i++) {
        endPosReceived[i] = endPos[i]- '0';  // Convert char to int by subtracting '0'
        printf("endPosReceived[%d] = %d\n", i, endPosReceived[i]);
    }
 
  mapway[0]=endPosReceived[0]-startPosReceived[0];
  mapway[1]=endPosReceived[1]-startPosReceived[1];
    
while(mapway[0]!=0)
    {
     if (mapway[0]>0)
     { 
         mapway[0]=mapway[0]-1;
         instructions[a]='r';
         a++;
     }
     else
     {
         mapway[0]=mapway[0]+1;
         instructions[a]='l';
         a++;   
     }
    }
    
    while(mapway[1]!=0)
    {
     if (mapway[1]>0)
     {
         mapway[1]=mapway[1]-1;
         instructions[a]='u';
         a++;
     }
     else
     {
         mapway[1]=mapway[1]+1;
         instructions[a]='d';
         a++;
     }
    }
    
instructions[a]='e';
/*for (int i = 0; i < 128; i++) 
  {
      if(instructions[i]=='e')
      {break;}
    printf("%c\n", instructions[i]);
  }*/
    for (int i = 0; i < 128; i++) {
        char current = instructions[i];
        if (current == direction) {
            drive[i]='F';
        } else {
            if (current == 'u') {
                if (direction == 'l') {drive[i]='R';}
                if (direction == 'r') {drive[i]='L';}
                if (direction == 'd') {drive[i]='T';}
                direction = 'u';
            } else if (current == 'd') {
                if (direction == 'l') {drive[i]='L';}
                if (direction == 'r') {drive[i]='R';}
                if (direction == 'u') {drive[i]='T';}
                direction = 'd';
            } else if (current == 'l') {
                if (direction == 'd') {drive[i]='R';}
                if (direction == 'u') {drive[i]='L';}
                if (direction == 'r') {drive[i]='T';}
                direction = 'l';
            } else if (current == 'r') {
                if (direction == 'u') {drive[i]='R';}
                if (direction == 'd') {drive[i]='L';}
                if (direction == 'l') {drive[i]='T';}
                direction = 'r';
            }
            else{drive[i]='E';
            break;
            }
        }
    }
    /*for (int i = 0; i < 128; i++) 
  {
      if(drive[i]=='E')
      {break;}
    printf("%c\n", drive[i]);
  }*/
return 0;
}
