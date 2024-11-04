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

class Thermistor
{
    private:
        uint8_t _tpin;
    public:
        Thermistor(uint8_t a_pin);
        float readThermistor();
};

#endif