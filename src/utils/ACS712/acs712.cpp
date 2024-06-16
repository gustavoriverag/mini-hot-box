#include <acs712.h>

ACS712::ACS712(int pin)
{
    _pin = pin;
}


float ACS712::readCurrent()
{
    float current = (VCC/2 - _avg() * VCC) / ACS712_SENSITIVITY;
    return current;
}

float ACS712::_avg()
{
    float sum = 0;
    int i = 0;
    float lastTime = 0;
    while (i < N_SAMPLES)
    {
        if (millis() - lastTime < 1)
        {
            continue;
        }
        lastTime = millis();
        sum += analogRead(_pin);
        i++;
    }
    return sum / N_SAMPLES / ADC_MAX;
}
