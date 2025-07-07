// Include libraries
#include <Wire.h>
#include <DFRobot_MAX30102.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "ESP_Wahaj.h"
int pwm=0;
// MAX30102 (Heart Rate, SpO2, Respiratory Rate)
DFRobot_MAX30102 particleSensor;
int32_t SPO2, heartRate;
int8_t SPO2Valid, heartRateValid;

// ECG - Analog Read
#define ECG_PIN A0

// Temperature - DS18B20
#define ONE_WIRE_BUS D6
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// MPU6050 - Sleep Activity
Adafruit_MPU6050 mpu;
float prev_x = 0, prev_y = 0, prev_z = 0;

// Setup
void setup() {
  Serial.begin(115200);

  // Initialize MAX30102
  while (!particleSensor.begin()) {
    Serial.println("MAX30102 not found");
    delay(1000);
  }
  particleSensor.sensorConfiguration(50, SAMPLEAVG_4, MODE_MULTILED, SAMPLERATE_100, PULSEWIDTH_411, ADCRANGE_16384);
  Serial.println("MAX30102 Initialized");

  // Initialize DS18B20
  sensors.begin();
  Serial.println("DS18B20 Initialized");

  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("MPU6050 not found");
    while (1) delay(10);
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("MPU6050 Initialized");
 start("Project", "12345678");
  delay(1000);
}

// Main Loop
void loop() {
  // === MAX30102 ===
      if (CheckNewReq() == 1) {
  particleSensor.heartrateAndOxygenSaturation(&SPO2, &SPO2Valid, &heartRate, &heartRateValid);
  delay(100);

  // === ECG from A0 ===
  int ecgValue = analogRead(ECG_PIN);

  // === Temperature from DS18B20 ===
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);

  // === MPU6050 ===
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float acc_change = abs(a.acceleration.x - prev_x) +
                     abs(a.acceleration.y - prev_y) +
                     abs(a.acceleration.z - prev_z);
  prev_x = a.acceleration.x;
  prev_y = a.acceleration.y;
  prev_z = a.acceleration.z;

  int sleepStatus = acc_change < 0.05 ? 0 : 1;

  // === Print Results ===
  Serial.println("------------ Health Monitoring ------------");

  Serial.print("Heart Rate    : ");
  Serial.print(heartRate);
  Serial.println(heartRateValid ? " bpm" : " (Invalid)");

  Serial.print("SpO2          : ");
  Serial.print(SPO2);
  Serial.println(SPO2Valid ? " %" : " (Invalid)");

  Serial.print("ECG Value     : ");
  Serial.println(ecgValue);

  Serial.print("Temperature   : ");
  Serial.print(tempC);
  Serial.println(" °C");

  Serial.print("Respiratory Rate (est.): ");
  Serial.println(estimateRespiratoryRate(heartRate)); // crude estimation

  Serial.print("Sleep Activity: ");
  Serial.println(sleepStatus);

  Serial.println("--------------------------------------------\n");
 String myString = String(heartRate) + "," + String(SPO2)+ "," + String(ecgValue)+ "," + String(estimateRespiratoryRate(heartRate))+ "," + String(sleepStatus)+","+String(tempC);
    returnThisStr(myString);
    delay(1000);

    String path = getPath();
    path.remove(0, 1);
    pwm = path.toInt();
  delay(2000);  // update every 2 seconds
}
}

// Rough estimation of respiratory rate (based on HR heuristic)
int estimateRespiratoryRate(int hr) {
  // Assuming normal 4:1 heart-to-breath ratio
  return hr > 0 ? hr / 4 : 0;
}
