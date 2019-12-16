/*codigo calibracion del sistema
#include "HX711.h"

#define DOUT  A1
#define CLK  A0

HX711 balanza(DOUT, CLK);

void setup() {
  Serial.begin(9600);
  Serial.println(balanza.read());
  balanza.set_scale(); // sensor sin escala
  balanza.tare(0);  //El peso actual es considerado Tara.
  Serial.println("Coloque un peso conocido:");
  
}
void loop() {

  Serial.print("Valor de lectura:  ");
  Serial.println(balanza.get_value(10),0);
  delay(100);
} 
fin codigo calibracion*/
/*procedimiento calibracion
promedio 2143270 
peso real = 3000
prom/peso = 714.42
fin pocedimiento*/


//////////////////configuracion sensor/////////////////
#include "HX711.h"
#define DOUT  A1
#define CLK  A0
HX711 balanza(DOUT, CLK);
/////////////////////////////////////////////////////

//int LED = 13;
int i=0;

void calibracion(){
   // Serial.print("calibrando");
    int factorCalibracion=40;
    int calibracion=0;
  //lectura de datos para su calibracion
    for (int i=0; i<factorCalibracion; i++){
      calibracion+=balanza.read();
    // Serial.println(".");
      delay(20);
    }
  //  Serial.println(".");
    calibracion/=factorCalibracion;
    balanza.tare(calibracion);  //valor de calibracion.  
   // Serial.println("Calibracion Terminada");
    Serial.println('r');    
  }
  
void setup() {
  balanza.set_scale(749.42); // escala
  Serial.begin(9600);
  //calibracion();
}

double obtenerPeso(){
  return balanza.get_units(1);
  }
double promedio(){
  return balanza.get_units(30);
  }
void loop() {

  if (Serial.available()){
    char data = Serial.read();
   // delay(80);
    //Serial.println(data);
    //flushSerial();
  switch(data){
    case 'c': 
      calibracion();
      //Serial.println();
      //digitalWrite(LED,HIGH);  
      //Serial.flush();
    break;
    case 'p': 
      Serial.println(promedio());
      //digitalWrite(LED,HIGH);  
      Serial.flush();
    break;
    case 'g': 
      Serial.println(obtenerPeso());
      //digitalWrite(LED,LOW);      
      Serial.flush();
    break;
    default:
      Serial.println(data);
      Serial.flush();
    }
   
    }
}

void flushSerial(){
    while(Serial.available()) {
    char s=Serial.read();
    }
  }
