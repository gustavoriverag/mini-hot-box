#include <utils.h>

int cant_datos = 26;

VoltageSensor v_sensor(A2);

void setup() 
{
    Serial.begin(9600);

}

void loop()
{
    Serial.println(analogRead(A2));
    delay(10);
}
