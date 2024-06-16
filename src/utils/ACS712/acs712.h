
#define ACS712_SENSITIVITY 0.66
#define VCC 3.3
#define ADC_MAX 1023
#define N_SAMPLES 1000


class ACS712 {
  public:
    ACS712(int pin);
    float readCurrent();
  private:
    int _pin;
    float _avg();
};