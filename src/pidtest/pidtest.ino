const int pwm_pin = 1;
const int termo_pin = 3;

void setup() {
  Serial.begin(112500);
  pinMode(pwm_pin, OUTPUT);
  pinMode(termo_pin, INPUT);
}

void loop() {
    if (Serial.available()) {
        int pwm = Serial.parseInt();
        Serial.print("PWM: ");
        Serial.println(pwm);

        analogWrite(pwm_pin, pwm);
    }
    Serial.println(analogRead(termo_pin));
}