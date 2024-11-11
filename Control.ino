#include "Wire.h"
#include <MPU6050_light.h>
#define dir_1 7 
#define pwm_1 6 
#define dir_2 4
#define pwm_2 3

MPU6050 mpu(Wire);
unsigned long timer = 0;
int angle;

double straight(){

  mpu.update();
  angle = int(mpu.getAngleZ());
  Serial.print("\tZ : ");
    Serial.println(angle);
  timer = millis(); 

  digitalWrite(dir_1,HIGH); //RIGHT WHEEL FORWARD WHEN HIGH
  digitalWrite(dir_2,LOW); //LEFT WHEEL BACKWARD WHEN HIGH
  //float multiplier=abs(angle/100)+1;
  int correction=0;
  if(angle==0){
    Serial.println("condition 1");
  analogWrite(pwm_2, 140); 
  analogWrite(pwm_1, 140);
  }
  if(angle>0){
    Serial.println("condition 2, " );
    correction=angle;
    Serial.print("correction");
    analogWrite(pwm_2, 140+angle); 
    analogWrite(pwm_1, 140-angle);
  }
   if(angle<0){
    Serial.println("condition 3");
    correction=angle;
    Serial.print("correction");
    analogWrite(pwm_2, 140-abs(angle)); 
    analogWrite(pwm_1, 140+abs(angle));
  }




  delay(10);
}

void setup(){ 

  Serial.begin(9600);
  Wire.begin();

  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050

  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");

  pinMode(pwm_1,OUTPUT); 
  pinMode(dir_1,OUTPUT); 
  pinMode(pwm_2,OUTPUT); 
  pinMode(dir_2,OUTPUT); 

 } 
 void loop(){

  straight();
 }
