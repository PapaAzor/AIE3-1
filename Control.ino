#include "Wire.h"
#include <MPU6050_light.h>
#include <Arduino.h>


#define dir_1 7 
#define pwm_1 6 
#define dir_2 4
#define pwm_2 3

MPU6050 mpu(Wire);


unsigned long timer = 0;
float angle;
float rotationTarget=0;
float rotationActual;

float rotationError;
float rotationErrorOld=0;
float rotationErrorNew=0;
float rotationErrorChange=0;
float rotationErrorDerivative=0;

float rotationErrorArea=0;

int miliOld=0;
int miliNew=0;
int dt=0;

int pwmValue1;
int pwmValue2;
int k1=15;
int k2=500;
float k3=0.30; 



double straight(){
  
  digitalWrite(dir_1,HIGH); //RIGHT WHEEL FORWARD WHEN HIGH
  digitalWrite(dir_2,LOW); //LEFT WHEEL BACKWARD WHEN HIGH

  miliOld=miliNew;
  miliNew=millis();
  dt=miliNew-miliOld;
  
  rotationError = rotationTarget-rotationActual;
  rotationErrorNew=rotationError;

  rotationErrorChange=rotationErrorNew-rotationErrorOld;
  rotationErrorDerivative=rotationErrorChange/dt;

  rotationErrorArea=rotationError*dt;

  pwmValue1 = 140 + (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea);
  pwmValue2 = 140 - (k1*rotationError+k2*rotationErrorDerivative+k3*rotationErrorArea);
  pwmValue1=constrain(pwmValue1,0,255);
  pwmValue2=constrain(pwmValue2,0,255);

  if(abs(rotationError) == 0){
   
    analogWrite(pwm_2, 140); 
    analogWrite(pwm_1, 140);
  }

  if(abs(rotationError) > 0){
   
    analogWrite(pwm_2, pwmValue2); 
    analogWrite(pwm_1, pwmValue1);
  }
  
  //Serial.println(0);
  Serial.print(millis()/1000.0);
  Serial.print(",");
  Serial.println((rotationError));
  
  
  //Serial.print("derivative= ");
  //Serial.println(rotationErrorDerivative*10);
  delay(5);
  rotationErrorOld=rotationErrorNew;

}

void setup(){ 

  Serial.begin(9600);
  Wire.begin();
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
 // Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  //Serial.println("Done!\n");
  
  pinMode(pwm_1,OUTPUT); 
  pinMode(dir_1,OUTPUT); 
  pinMode(pwm_2,OUTPUT); 
  pinMode(dir_2,OUTPUT); 

  


  miliNew=millis();

 } 
 void loop(){

  mpu.update();
  rotationActual = mpu.getAngleZ();
  //Serial.print("\tZ : ");
  //Serial.println(rotationActual);
  timer = millis(); 
  rotationError = rotationTarget-rotationActual;
  int myTime=millis()/1000.0;
  /*if(myTime<5){
    rotationTarget=0;
  }
  if(myTime>5){
    rotationTarget=270;
  }*/
  straight();
  
 }
