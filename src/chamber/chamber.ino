#include <PID_v1.h>

#include <MAX6675.h>


#define AMBIENTE 3


const int pwm = 1;

const size_t n_termocuplas = 8;
const int THC_PINS[n_termocuplas] = {3,4,5,6,7,8,9,10};



MAX6675 termocuplas[n_termocuplas];

//Variables PID
double setpoint, input, output;
//Parametros PID
double kp = 2, ki = 5, kd = 1;

PID myPID(&input, &output, &setpoint, kp, ki, kd, P_ON_M, DIRECT);

void setup() {
  
  // Inicializar serial
  Serial.begin(112500);

  // Inicializar termocuplas
  for (int i=0;i<n_termocuplas;i++){
    termocuplas[i].setPin(THC_PINS[i]);
  }

  // Inicializar PID
  input = termocuplas[AMBIENTE].readTempC();
  setpoint = 30;
  
  // Inicializar PWM
  pinMode(pwm, OUTPUT);

}

void loop() {
  
  // Leer temperatura
  for (int i=0;i<n_termocuplas;i++){
    if (i == AMBIENTE){
      input = termocuplas[i].readTempC();
    }
    Serial.print("Usar formato de salida serialmonitor");
  }

  // Calcular PID
  myPID.Compute();
  analogWrite(pwm, output);
}
