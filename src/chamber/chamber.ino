#include <PID_v1.h>
#include <MAX6675.h>
#include <utilities.h>

// Definir termocupla ambiente caliente y frío
#define AMBIENTE_C 0
#define AMBIENTE_F 1

// Pines PWM caliente y frío
const int pwm_c = 2;
const int pwm_f = 3;

// Array de n termocuplas
const size_t n_termocuplas = 8;
const int THC_PINS[n_termocuplas] = {3,4,5,6,7,8,9,10};

// Se crean los objetos de las termocuplas
MAX6675 termocuplas[n_termocuplas];
float temps[n_termocuplas];

// Variable para lectura de temperatura
float temp;

Thermistor t_calefactor(A0);
float therm;

CurrentSensor c_sensor(A1);
float current;

VoltageSensor v_sensor(A2);
float voltage;

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

uint32_t lastSample = 0;
uint32_t lastSend = 0;

int sampleTime = 1000;
int sendTime = 5000;
int samples = 0;

void setup() {
  
  // Inicializar serial
  Serial.begin(9600);

  // Inicializar termocuplas
  for (int i=0;i<n_termocuplas;i++){
    termocuplas[i].setPin(THC_PINS[i]);
  }

  // Inicializar PID
  temp_c = termocuplas[AMBIENTE_C].readTempC();
  setpoint_c = 30;

  temp_f = termocuplas[AMBIENTE_F].readTempC();
  setpoint_f = 10;
  
  pidCaliente.SetMode(MANUAL);
  pidFrio.SetMode(MANUAL);
  // Inicializar PWM
  pinMode(pwm_c, OUTPUT);
  pinMode(pwm_f, OUTPUT);
}

void loop() {

  // State sample
  if (millis() - lastSample < sampleTime){
    return;
  }

  samples++;
  lastSample = millis();

  // Leer temperatura
  for (int i=0;i<n_termocuplas;i++){
    temp = termocuplas[i].readTempC();
    temps[i] = temps[i] + temp;
  }

  // Leer temperatura calefactor
  therm = therm + t_calefactor.readThermistor();

  // Leer voltaje
  voltage = voltage + v_sensor.readVoltage();

  // Leer corriente
  current = current + c_sensor.readCurrent();


// State send
  if (millis() - lastSend < sendTime){
    return;
  }
  lastSend = millis();

  // Calcular PID Caliente
  temp_c = temps[AMBIENTE_C]/samples;
  //pidCaliente.Compute();
  analogWrite(pwm_c, output_c);

  // Calcular PID
  temp_f = temps[AMBIENTE_F]/samples;
  //pidFrio.Compute();
  analogWrite(pwm_f, output_f);


  for (int i = 0; i < n_termocuplas; i++){
    Serial.print(temps[i]/samples);
    Serial.print(",");
    temps[i] = 0;
  }

  Serial.print(pwm_c);
  Serial.print(",");

  Serial.print(therm/samples);
  Serial.print(",");
  therm = 0;

  Serial.print(voltage/samples);
  Serial.print(",");
  voltage = 0;

  Serial.print(current)/samples;
  Serial.print(",");
  current = 0;

  Serial.print(pwm_f);
  Serial.print("\n");

  samples = 0;
}
