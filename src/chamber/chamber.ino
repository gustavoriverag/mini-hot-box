#include <PID_v1.h>
#include <MAX6675.h>
#include <thermistor.h>

// Definir termocupla ambiente caliente y frío
#define AMBIENTE_C 0
#define AMBIENTE_F 1

// Pines PWM caliente y frío
const int pwm_c = 1;
const int pwm_f = 2;

// Array de n termocuplas
const size_t n_termocuplas = 8;
const int THC_PINS[n_termocuplas] = {3,4,5,6,7,8,9,10};

// Se crean los objetos de las termocuplas
MAX6675 termocuplas[n_termocuplas];

// Variable para lectura de temperatura
float temp;

Thermistor t_calefactor(A0);
float therm;

//Variables PID caliente
double setpoint_c, temp_c, output_c;
//Parametros PID caliente
double kp_c = 2, ki_c = 5, kd_c = 1;

PID pidCaliente(&temp_c, &output_c, &setpoint_c, kp_c, ki_c, kd_c, P_ON_M, DIRECT);

//Variables PID frío
double setpoint_f, temp_f, output_f;
//Parametros PID frío
double kp_f = 2, ki_f = 5, kd_f = 1;

PID pidFrio(&temp_f, &output_f, &setpoint_f, kp_f, ki_f, kd_f, P_ON_M, REVERSE);

void setup() {
  
  // Inicializar serial
  Serial.begin(112500);

  // Inicializar termocuplas
  for (int i=0;i<n_termocuplas;i++){
    termocuplas[i].setPin(THC_PINS[i]);
  }

  // Inicializar PID
  temp_c = termocuplas[AMBIENTE_C].readTempC();
  setpoint_c = 30;

  temp_f = termocuplas[AMBIENTE_F].readTempC();
  setpoint_f = 10;
  
  // Inicializar PWM
  pinMode(pwm_c, OUTPUT);
  pinMode(pwm_f, OUTPUT);
}

void loop() {
  Serial.print("Ensayo,");
  // Leer temperatura
  for (int i=0;i<n_termocuplas;i++){
    temp = termocuplas[i].readTempC();
    if (i == AMBIENTE_C){
      temp_c = temp;
    } else if (i == AMBIENTE_F){
      temp_f = temp;
    }
    Serial.print(temp);
    Serial.print(",");
  }

  // Leer temperatura calefactor
  therm = t_calefactor.readThermistor();
  Serial.print(therm);
  Serial.print(",");

  // Calcular PID Caliente
  pidCaliente.Compute();
  analogWrite(pwm_c, output_c);
  Serial.print(pwm_c);
  Serial.print(",");

  // Calcular PID
  pidFrio.Compute();
  analogWrite(pwm_f, output_f);
  Serial.print(pwm_f);
  Serial.print(",");
}
