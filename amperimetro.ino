#include "EmonLib.h"

EnergyMonitor SCT013;

int pinSCT = A0;   //Pino analógico conectado ao SCT-013
int tensao = 127;
int potencia;

void setup()   
{
  SCT013.current(pinSCT, 211.45);
  Serial.begin(9600);
}

void loop()
{
  double Irms = SCT013.calcIrms(1480);   // Calcula o valor da Corrente

  potencia = Irms * tensao;   // Calcula o valor da Potencia Instantanea
  
  Serial.print("{\"Corrente\":  "+(String)Irms+", \"Potencia\": "+(String)potencia+"}");   // Envia saida no formato json

  delay(1000);
}