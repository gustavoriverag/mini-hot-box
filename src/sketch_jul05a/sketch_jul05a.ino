#include <MAX6675.h>

MAX6675 termo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  termo.setPin(22);
 
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(termo.readTempC());
}
