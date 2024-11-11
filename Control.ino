#include "Wire.h"
#include <MPU6050_light.h>
#define dir_1 7 
#define pwm_1 6 
#define dir_2 4
#define pwm_2 3

MPU6050 mpu(Wire);

unsigned long timer = 0;
int angle;
int rotationTarget=0;
int rotationActual;
int rotationError;
int pwmValue1;
int pwmValue2;

double straight(){
  
  digitalWrite(dir_1,HIGH); //RIGHT WHEEL FORWARD WHEN HIGH
  digitalWrite(dir_2,LOW); //LEFT WHEEL BACKWARD WHEN HIGH
  
  rotationError = rotationTarget-rotationActual;
  pwmValue1 = 140 + (2*rotationError);
  pwmValue2 = 140 - (2*rotationError);

  if(abs(rotationError) == 0){
    Serial.println("condition 1");
    Serial.println(rotationError);
    analogWrite(pwm_2, 140); 
    analogWrite(pwm_1, 140);
  }

  if(abs(rotationError) > 0){
    Serial.println("condition 2");
    Serial.println(rotationError);
    analogWrite(pwm_2, pwmValue2); 
    analogWrite(pwm_1, pwmValue1);
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

  mpu.update();
  rotationActual = int(mpu.getAngleZ());
  Serial.print("\tZ : ");
	Serial.println(rotationActual);
  timer = millis(); 
  rotationError = rotationTarget-rotationActual;
  
  straight();
 }
