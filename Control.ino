
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
