#include <thermistor.h>

Thermistor::Thermistor(uint8_t a_pin) {
  _pin = a_pin;
  _lastCallTime = 0;
  for (int i=0; i< NUMSAMPLES; i++) {
    _samples[i] = 0;
  }
}

float Thermistor::readThermistor() {
  uint8_t i = 0;
  float average;
  // take N samples in a row, with a slight delay
  while (i < NUMSAMPLES) {
    if (millis() - _lastCallTime >= 10) {
      _lastCallTime = millis();
      _samples[i] = analogRead(_pin);
      i++;
    }
  }
  // average all the samples out
  average = 0;
  for (i=0; i< NUMSAMPLES; i++) {
     average += _samples[i];
  }
  average /= NUMSAMPLES;
  
  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
  float steinhart;
  steinhart = average / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert absolute temp to C
  
  return steinhart;
}

VoltageSensor::VoltageSensor(uint8_t a_pin) {
  _pin = a_pin;
}

float VoltageSensor::readVoltage() {
  float voltage_adc = analogRead(_pin) * (VCC / ADC_MAX);
  return voltage_adc * (R1 + R2) / R2;
}

CurrentSensor::CurrentSensor(uint8_t a_pin) {
  _pin = a_pin;
}

float CurrentSensor::readCurrent() {
    float current = (VCC/2 - analogRead(_pin) * VCC) / ADC_MAX / ACS712_SENSITIVITY;
  return current;
} 