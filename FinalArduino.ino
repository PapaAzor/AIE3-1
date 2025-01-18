#include "Wire.h"
#include <MPU6050_light.h>
#include "A4988.h"
#include <Arduino.h>

MPU6050 mpu(Wire);
unsigned long timer = 0;

int Step = 9; //GPIO14---D5 of Nodemcu--Step of stepper motor driver
int Dire = 8; //GPIO2---D4 of Nodemcu--Direction of stepper motor driver
const int spr = 200; //Steps per revolution
int RPM = 50; //Motor Speed in revolutions per minute
int Microsteps = 1; //Stepsize (1 for full steps, 2 for half steps, 4 for quarter steps, etc)
A4988 stepper(spr, Dire, Step);

String pullUpState;

void setup() {
  Serial.begin(9600);

   pinMode(Step, OUTPUT); //Step pin as output
  pinMode(Dire,  OUTPUT); //Direcction pin as output
  digitalWrite(Step, LOW); // Currently no stepper motor movement
  digitalWrite(Dire, LOW);

  stepper.begin(RPM, Microsteps);

  Wire.begin();

  byte status = mpu.begin();
  delay(1000); // this is time for the sensor to calibrate
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("666");

  
}

void loop() {
  /*
  stepper.rotate(160);
  delay(5000);
  stepper.rotate(-160);
  delay(5000);
  */
  mpu.update();
  
  //if((millis()-timer)>10){
    if(Serial.available()>0){
      Serial.println(mpu.getAngleZ());
      timer = millis();
      delay(10);
    }
    
 // }
}
