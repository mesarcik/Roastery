#include <OneWire.h>
#include <DallasTemperature.h>
//#include "MegunoLink.h"
//#include "Filter.h"

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 8
#define TEMPERATURE_PRECISION 9

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// arrays to hold device addresses
DeviceAddress insideThermometer, outsideThermometer, middleThermometer;



float array [120];
int counter = 0;
float adjustment_counter = 0.25;
float counter_counter = 0;

//// Create a new exponential filter with a weight of 5 and an initial value of 0. 
//ExponentialFilter<float> exp_smoothing_filter(5, array[0]);

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
  populate();
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
  delay(950);
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

void populate(void){
  array[0] = 100;
  for (int i = 1; i < 120; i++){
    array[i] = array[i-1] + 0.25 + float(random(-20, 10))/100.0;
  }

}

void loop(void)
{ 

//   for (int i = 0; i<sizeof(array)/sizeof(float);i++){
//       Serial.println(array[i]); 
////        exp_smoothing_filter.Filter(array[i]);
////        Serial.println(exp_smoothing_filter.Current());
//        delay(900);
//   }
//    Serial.println(counter);
//    if (counter < 200){
////      counter = counter +float(ran`dom(-50, 100))/100.0;
//        if (counter_counter > 119){
//          adjustment_counter = adjustment_counter +0.25;
//          counter_counter =0;
//        }
//
//        counter = counter + adjustment_counter; //+ +float(random(-10, 10))/100.0;
//        counter_counter +=1;
//    }else{
//      counter = 30;
//    }
    // #####ASSUMED DELAY OF 
    if (counter > 119){
      counter =0;
    }
    Serial.println(array[counter]);
    counter +=1;

    
    delay(1000);
//    delay(95);
  

    
}
