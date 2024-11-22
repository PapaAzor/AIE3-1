#include <stdio.h>
#include <string.h>



int mapway[2]={0,0};
char startPos[2]={'3','4'};
int startPosReceived[2]={0,0};
char endPos[2]={'1','1'};
int endPosReceived[2]={0,0};
char instructions[127]={'0'};
int a=0;
    int main() {
    for (int i = 0; i<2; i++) {
        startPosReceived[i] = startPos[i]- '0';  // Convert char to int by subtracting '0'
         printf("startPosReceived[%d] = %d\n", i, startPosReceived[i]);
    }
    
      for (int i = 0; i<2; i++) {
        endPosReceived[i] = endPos[i]- '0';  // Convert char to int by subtracting '0'
        printf("endPosReceived[%d] = %d\n", i, endPosReceived[i]);
    }
for (int i = 0; i<2; i++) {
     printf("directions[%d] = %d\n",i,mapway[i]=endPosReceived[i]-startPosReceived[i]);
  }
  mapway[1]=endPosReceived[1]-startPosReceived[1];
  mapway[0]=endPosReceived[0]-startPosReceived[0];
  
while(mapway[0]!=0)
    {
     if (mapway[0]>0)
     {mapway[0]=mapway[0]-1;
        instructions[a]='r';
         a++;
        
     }
     else
     {mapway[0]=mapway[0]+1;
          instructions[a]='l';
         a++;
          
     }
    }
    while(mapway[1]!=0)
    {
     if (mapway[1]>0)
     {mapway[1]=mapway[1]-1;
          instructions[a]='u';
     
         a++;
     }
     else
     {mapway[1]=mapway[1]+1;
          instructions[a]='d';
         a++;
     }
    }
instructions[a]='e';
for (int i = 0; i < 128; i++) 
  {
      if(instructions[i]=='e')
      {break;}
    printf("%c\n", instructions[i]);
  }
  
}
