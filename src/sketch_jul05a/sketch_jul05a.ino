#include <MAX6675.h>

MAX6675 termo(2);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // termo.setPin(34);
  // analogWrite(3, 128);
  delay(1000);
  Serial.println("Redy");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(termo.readTempC());
  delay(1000);
}
