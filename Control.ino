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
int rotationErrorOld=0;
int rotationErrorNew=0;
int rotationErrorChange=0;
int rotationErrorDerivative=0;

int rotationErrorArea=0;

int miliOld=0;
int miliNew=0;
int dt=0;

int pwmValue1;
int pwmValue2;
int k1=5;
int k2=50;
int k3=2; // ladnie bylo dla k1=10 k2=40 k3=1
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

  if(abs(rotationError) == 0){
   
    analogWrite(pwm_2, 0); 
    analogWrite(pwm_1, 0);
  }

  if(abs(rotationError) > 0){
   
    analogWrite(pwm_2, pwmValue2); 
    analogWrite(pwm_1, pwmValue1);
  }
  Serial.print(millis()/1000);
  Serial.print(",");
  //Serial.println(0);
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
  //Serial.print(F("MPU6050 status: "));
 // Serial.println(status);
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
  rotationActual = int(mpu.getAngleZ());
  //Serial.print("\tZ : ");
	//Serial.println(rotationActual);
  timer = millis(); 
  rotationError = rotationTarget-rotationActual;
  
  straight();
 }
