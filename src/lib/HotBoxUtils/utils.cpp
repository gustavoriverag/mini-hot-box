#include <Arduino.h>
#include <utils.h>

Thermistor::Thermistor(uint8_t a_pin) {
  _tpin = a_pin;
}

float Thermistor::readThermistor() {
  uint8_t i = 0;
  float reading = analogRead(_tpin);

  // convert the value to resistance
  reading = 1023 / reading - 1;
  reading = SERIESRESISTOR / reading;
  float steinhart;
  steinhart = reading / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert absolute temp to C
  
  return steinhart;
}