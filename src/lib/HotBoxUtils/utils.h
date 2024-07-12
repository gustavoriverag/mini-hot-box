#ifndef utils_h
#define utils_h

#include <Arduino.h>

#define THERMISTORNOMINAL 100000      
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25   

// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 3950
// the value of the 'other' resistor
#define SERIESRESISTOR 10000    

#define ACS712_SENSITIVITY 0.66
#define VCC 5
#define ADC_MAX 1023
#define N_SAMPLES 5

#define R1             30000.0 // resistor values in voltage sensor (in ohms)
#define R2             7500.0  // resistor values in voltage sensor (in ohms)

class Thermistor
{
    private:
        uint8_t _tpin;
    public:
        Thermistor(uint8_t a_pin);
        float readThermistor();
};

class VoltageSensor
{
    private:
        uint8_t _vpin;
    public:
        VoltageSensor(uint8_t a_pin);
        float readVoltage();
};

class CurrentSensor
{
    private:
        uint8_t _cpin;
    public:
        CurrentSensor(uint8_t a_pin);
        float readCurrent();
};

#endif