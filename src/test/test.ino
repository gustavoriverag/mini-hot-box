int cant_datos = 26;

void setup() 
{
    Serial.begin(9600);
}

void loop()
{
    for (int i=0;i<cant_datos;i++){

        Serial.print(random(10,20));
        if (i == cant_datos-1){
            Serial.println();
        }
        else{
            Serial.print(",");
        }
    }
    delay(1000);
}
