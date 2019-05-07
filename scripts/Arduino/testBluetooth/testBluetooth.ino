#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 200
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);

#include <SoftwareSerial.h>
#define rxPin 11 // Broche 11 en tant que RX, à raccorder sur TX du HC-05
#define txPin 10 // Broche 10 en tant que TX, à raccorder sur RX du HC-05
// Init Bluetooth
SoftwareSerial mySerial(rxPin, txPin);
uint32_t c=0, black = 0;

void setup()
{
  // define pin modes for tx, rx pins:
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  mySerial.begin(38400);
  Serial.begin(38400);

  black = strip.Color(0,0,0);
  c = strip.Color(220,0,0);
  // Init Leds
  strip.begin();
}
void loop()
{
int i = 0;
char someChar[32] = {0};
// when characters arrive over the serial port...
if(Serial.available()) {
  if(Serial.available() > 0){
      int LED = Serial.readString().toInt();
      Serial.println(LED);
      one(LED);
  }
}

void one(int num){
  for(int i=0;i<NBLED;i++)
  {
    if (i == num)
      strip.setPixelColor(i,c);
    else
      strip.setPixelColor(i,black);
  }
  strip.show();
}
