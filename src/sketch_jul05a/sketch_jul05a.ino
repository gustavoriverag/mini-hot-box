void setup() {
  // put your setup code here, to run once:
  pinMode(3, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(5000);
  analogWrite(3, 128);
  delay(5000);
  analogWrite(3, 0);

}
