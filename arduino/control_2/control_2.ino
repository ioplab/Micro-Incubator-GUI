/*
 * Version: 0511
 * Project Author: Jerry
 * collaberator: Jacky
 * 
 * work: clean code, modify transmission data format
 */

#include "max6675.h"
#include <NDIRZ16.h>
#include <SoftwareSerial.h>

/* Arduino UNO Pin D2 (Software Serial Rx) <===> Adaptor's Green  Wire (Tx)
 * Arduino UNO Pin D3 (Software Serial Tx) <===> Adaptor's Yellow Wire (Rx) */
SoftwareSerial mySerial(2,3);
NDIRZ16 mySensor = NDIRZ16(&mySerial);
 
int ktcSO  = 8;
int ktcCS  = 9;
int ktcCLK = 10;
int LED_init = 13; 
int LED = 7; 
int air = 4;

int         i = 0;
String      s = "";
float temp_rv = 0.0;
float temp_th = 25.0;
float  air_rv = 0.0;
float  air_th = 50000;

MAX6675 ktc(ktcCLK, ktcCS, ktcSO);

void setup() {
  pinMode(LED_init, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(air, OUTPUT);
  Serial.begin(115200);
  mySerial.begin(9600);
  digitalWrite(LED_init, HIGH);
  //delay(10000);  
  digitalWrite(LED_init, LOW);
  delay(500);
}
 
void loop() {
  // 檢查是否有資料可供讀取
  s = "";
  while (Serial.available()) {
    char c = Serial.read();
    if(c!='\n'){
      s += c;
    }
    delay(5);
  }
  
  // 根據收到的字元決定要打開或關掉 LED
  switch (s[0]) {
    case 't': 
      temp_th = s.substring(1).toFloat();
      delay(1);
      break;
    case 'a': 
      air_th = s.substring(1).toFloat();
      delay(1);
      break;
  }
  
  // prepare read data from sensor
  if(mySensor.measure())
  
  delay(300); 

  // read sensor value
  temp_rv = ktc.readCelsius();
  air_rv  = mySensor.ppm;
  
  // heater
  if(temp_rv < temp_th)
  {
    digitalWrite(LED, HIGH);
  }
  else
  {
    digitalWrite(LED, LOW);
  }

  // co2 pressure
  if (air_rv < air_th)
  {
    digitalWrite(air, HIGH);
  }
  else
  {
    digitalWrite(air, LOW);
  }

  // send data by UART
  Serial.println(String(temp_rv)+","+String(air_rv)); 
}
