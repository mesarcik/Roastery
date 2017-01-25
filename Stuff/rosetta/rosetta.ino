#include <OneWire.h>
#include <DallasTemperature.h>
#include "MegunoLink.h"
#include "Filter.h"

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 8
#define TEMPERATURE_PRECISION 9

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses
DeviceAddress insideThermometer, outsideThermometer, middleThermometer;



float array [] = {200,199.75,199.5,199,198.5,198,197.75,197.5,197.25,197,196.75,196.5,196.25,196,195.75,195.5,195.25,195,194.75,194.5,194.25,194,194.5,194.75,195,195.25,195.5,195.75,196,196.5,196.75,197,197.25,197.5,197.75,198,198.25,198.5,198.75,199,199.25,199.5,199.75,200};
float counter = 30;

//// Create a new exponential filter with a weight of 5 and an initial value of 0. 
ExponentialFilter<float> exp_smoothing_filter(5, array[0]);

void setup(void)
{
  
  digitalWrite(4, HIGH);
  delay(200); 
  pinMode(4, OUTPUT);  
  
  // start serial port
  Serial.begin(9600);
 // Serial.println("Dallas Temperature IC Control Library Demo");

  // Start up the library
  //sensors.begin();
  delay(2000);

//   while(counter < 10){
//          for (int i = 0; i<sizeof(array)/sizeof(float);i++){ 
//            exp_smoothing_filter.Filter(array[counter]);
//          }
//          counter++;
//
//       }

  

  // method 1: by index
 // if (!sensors.getAddress(insideThermometer, 0)) Serial.println("Unable to find address for Device 0"); 


}

// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    // zero pad the address if necessary
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

// function to print the temperature for a device
void printTemperature(DeviceAddress deviceAddress, char name)
{
  delay(250);
  float tempC = sensors.getTempC(deviceAddress);
  Serial.println(tempC);
 }

// function to print a device's resolution
void printResolution(DeviceAddress deviceAddress)
{
  Serial.print("Resolution: ");
  Serial.print(sensors.getResolution(deviceAddress));
  Serial.println();    
}



void loop(void)
{ 

//   for (int i = 0; i<sizeof(array)/sizeof(float);i++){
//       Serial.println(array[i]); 
////        exp_smoothing_filter.Filter(array[i]);
////        Serial.println(exp_smoothing_filter.Current());
//        delay(900);
//   }
    Serial.println(counter);
    if (counter < 200){
//      counter = counter +float(random(-50, 100))/100.0;
        counter = counter + 0.25+ +float(random(-50, 50))/100.0;
    }else{
      counter = 30;
    }
    
    delay(900);
  

    
}
