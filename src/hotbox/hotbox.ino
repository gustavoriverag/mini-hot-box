#include <PID_v1.h>
#include <MAX6675.h>
#include <utils.h>

// Definir termocupla ambiente caliente y frío
#define AMBIENTE_C 9
#define AMBIENTE_F 20

// Pines PWM caliente y frío
const int pwm_c = 2;
const int pwm_f = 3;

// Array de n termocuplas
const size_t n_termocuplas = 22;

// Using pins from 22 to 44
const int THC_PINS[n_termocuplas] = {22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43};

// Se crean los objetos de las termocuplas
MAX6675 termocuplas[n_termocuplas];
float temps[n_termocuplas];

// Variable para lectura de temperatura
float temp;

Thermistor t_calefactor(A0);
float therm;

//Variables PID caliente
double setpoint_c, temp_c, output_c;
//Parametros PID caliente
double kp_c = 0.2, ki_c = 1.5, kd_c = 0.1;

PID pidCaliente(&temp_c, &output_c, &setpoint_c, kp_c, ki_c, kd_c, P_ON_M, DIRECT);

//Variables PID frío
double setpoint_f, temp_f, output_f;
//Parametros PID frío
double kp_f = 0.2, ki_f = 1.5, kd_f = 0.1;

PID pidFrio(&temp_f, &output_f, &setpoint_f, kp_f, ki_f, kd_f, P_ON_M, REVERSE);

uint32_t lastSample = 0;
uint32_t lastSend = 0;

int sampleTime = 1000;
int sendTime = 5000;
int samples = 0;

uint32_t periodoFrio = 60000;
uint32_t tiempoFrio = 0;
// 0: Inicial, PID manual, apagado
// 1: PID manual, transmitiendo datos
// 2: PID automático, transmitiendo datos
int state = 0;

bool newCommand = false;
const byte numChars = 32;
char receivedChars[numChars];

void stateChange(int st){
    state = st;
    if (state == 0){
      pidCaliente.SetMode(MANUAL);
      pidFrio.SetMode(MANUAL);
      analogWrite(pwm_c, 0);
      analogWrite(pwm_f, 0);
    }

    if (state == 1){
      pidCaliente.SetMode(MANUAL);
      pidFrio.SetMode(MANUAL);
      output_c = 0;
      output_f = 0;
    }

    if (state == 2){
      tiempoFrio = millis();
      pidCaliente.SetMode(AUTOMATIC);
      // pidFrio.SetMode(AUTOMATIC);
      output_f = 255;
      // output_c = 255;
    }
}

void parseCommand(){
  //basado en https://forum.arduino.cc/t/serial-input-basics-updated/382007
  char rc;
  static byte ndx = 0;
  char c;
  while (Serial.available() > 0){
    if (newCommand == false) {
    c = Serial.read();
    newCommand = true;
    } else {
      rc = Serial.read();
      if (rc == '\n') {
        receivedChars[ndx] = '\0'; // terminate the string
        ndx = 0;
        newCommand = false;
        switch (c)
        {
        case 's':
          stateChange(atoi(receivedChars));
          break;
        case 'c':
          if (state == 1) {
            output_c = atoi(receivedChars);
          }
          break;
        case 'f':
          if (state == 1) {
            output_f = atoi(receivedChars);
          }
          break;
        case 'p':
          if (receivedChars[0] == 'c'){
            kp_c = atof(receivedChars+1);
            pidCaliente.SetTunings(kp_c, ki_c, kd_c);
          } else if (receivedChars[0] == 'f'){
            kp_f = atof(receivedChars+1);
          }
          break;
        case 'i':
          if (receivedChars[0] == 'c'){
            ki_c = atof(receivedChars+1);
            pidCaliente.SetTunings(kp_c, ki_c, kd_c);
          } else if (receivedChars[0] == 'f'){
            ki_f = atof(receivedChars+1);
            
          }
          break;
        case 'd':
          if (receivedChars[0] == 'c'){
            kd_c = atof(receivedChars+1);
            pidCaliente.SetTunings(kp_c, ki_c, kd_c); 
          } else if (receivedChars[0] == 'f'){
            kd_f = atof(receivedChars+1);
          }
          break;
        default:
          break;
        }
        return;
      }
      if (ndx < numChars) {
        receivedChars[ndx] = rc;
        ndx++;
      }
    }
  }
}

void setup() {
  
  // Inicializar serial
  Serial.begin(115200);

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

  pidCaliente.SetOutputLimits(0, 255);
  pidFrio.SetOutputLimits(0, 255);

  // Inicializar PWM
  pinMode(pwm_c, OUTPUT);
  pinMode(pwm_f, OUTPUT);
}

void loop() {
  parseCommand();

  if (state == 0){
    return;
  }

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

// State send
  if (millis() - lastSend < sendTime){
    return;
  }
  lastSend = millis();

  // Calcular PID Caliente
  if (therm/samples > 80){
    output_c = 0;
  } else {
    temp_c = temps[AMBIENTE_C]/samples;
    pidCaliente.Compute();
  }

  // Calcular PID
  if (state != 1){
    // temp_f = temps[AMBIENTE_F]/samples;
    // pidFrio.Compute();
    if (millis() - tiempoFrio > periodoFrio){
      if (output_f == 0){
        output_f = 255;
        periodoFrio = 60000;
      } else {
        output_f = 0;
        periodoFrio = 30000;
      }
      tiempoFrio = millis();
    }
  }

  analogWrite(pwm_c, output_c);
  analogWrite(pwm_f, output_f);


  for (int i = 0; i < n_termocuplas; i++){
    Serial.print(temps[i]/samples);
    Serial.print(",");
    temps[i] = 0;
  }

  Serial.print(output_c);
  Serial.print(",");

  Serial.print(therm/samples);
  Serial.print(",");
  therm = 0;

  Serial.print(output_f);
  Serial.print("\n");

  samples = 0;
}
