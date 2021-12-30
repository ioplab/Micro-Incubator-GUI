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

int   i = 0;
float temp_rv = 0.0;
float temp_th = 0.0;
float air_rv = 0.0;
float air_rh = 50000;

MAX6675 ktc(ktcCLK, ktcCS, ktcSO);

void setup() {
  pinMode(LED_init, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(air, OUTPUT);
  Serial.begin(115200);
  mySerial.begin(9600);
  digitalWrite(LED_init, HIGH);
  delay(10000);  
  digitalWrite(LED_init, LOW);
  delay(500);
}
 
void loop() {
  /* prepare read data from sensor */
  if(mySensor.measure())
  
  delay(300); 

  /* read sensor value */
  temp_rv = ktc.readCelsius();
  air_rv    = mySensor.ppm;
  
  /* heater */
  if(temp_rv < temp_th)
  {
    digitalWrite(LED, HIGH);
  }
  else
  {
    digitalWrite(LED, LOW);
  }

  /* co2 pressure */
  if (air_rv < air_rh)
  {
    digitalWrite(air, HIGH);
  }
  else
  {
    digitalWrite(air, LOW);
  }

  /* send data to UART*/
  Serial.println(String(temp_rv)+","+String(air_rv)); 
}
