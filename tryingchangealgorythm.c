#include <stdio.h>
#include <string.h>
void dist_way(int startPosReceived[2],int endPosReceived[2])
{
    int mapway[2]={0,0};
  for (int i = 0; i<2; i++) {
     mapway[i]=endPosReceived[i]-startPosReceived[i];
  }
}


int mapway[2]={0,0};
char startPos[2]={2,5};
int startPosReceived[2]={0,0};
char endPos[2]={3,4};
int endPosReceived[2]={0,0};
String[] instructions;
    int main() {
    for (int i = 0; i<2; i++) {
        startPosReceived[i] = startPos[i];  // Convert char to int by subtracting '0'
         printf("startPosReceived[%d] = %d\n", i, startPosReceived[i]);
    }
    
      for (int i = 0; i<2; i++) {
        endPosReceived[i] = endPos[i];  // Convert char to int by subtracting '0'
        printf("endPosReceived[%d] = %d\n", i, endPosReceived[i]);
    }
for (int i = 0; i<2; i++) {
     printf("directions[%d] = %d\n",i,mapway[i]=endPosReceived[i]-startPosReceived[i]);
  }

}
