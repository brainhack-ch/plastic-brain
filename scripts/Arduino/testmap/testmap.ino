// BrainHack 2019
// Manik Victor Jorge Elif Jelena Italo Gaetan
//
// print all led in black except the one you choose via
// the serial port (ID = [0,NBLED-1])

#include <Adafruit_NeoPixel.h>
#define PIN 6     // the pin that transmit the signal to led strip
#define NBLED 200 // the number of LED in the strip
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);

uint32_t c=0, black = 0;

void setup(){
    Serial.begin(9600);
    // Init the 2 colors that will be used
    black = strip.Color(0,0,0);
    c = strip.Color(220,0,0);
    // Init Leds
    strip.begin();
}

void loop(){
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
