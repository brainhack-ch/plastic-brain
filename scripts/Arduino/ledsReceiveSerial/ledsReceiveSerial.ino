

/*
processing incoming serial data without blocking.
*/

// how much serial data we expect before a new Led (a led =16bytes max)
const unsigned int MAX_INPUT =200;
#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 220
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);

void setup ()
  {
  // Init Leds
   strip.begin();
   strip.show();
  // Init Serial port
  Serial.begin (230400);
  Serial.println("PlasticBrain Prêt");
  } // end of setup

  int bytesread=0, i=0;
  long couleur[4];
  uint32_t c=0;
  int currentLed=0;
  int nbled=0;
 
static char input_led [NBLED*3] ; 


void lightoff()
{
  c=strip.Color(0,0,0);
  for(i=0;i<nbled;i++)
    {
      strip.setPixelColor(i,c);
   }
   strip.show();
}

void lightfrombuffer()
{
  
  for(i=0;i<nbled;i++)
    {
      c=strip.Color(input_led[i*3],input_led[i*3+1],input_led[i*3+2]);
      strip.setPixelColor(i,c);
   }
   strip.show();
}


void loop()
  {
  // if serial data available, process it
  if (Serial.available ())
  {
    nbled=Serial.read();
    bytesread=Serial.readBytes(input_led,nbled*3);
    if (bytesread==nbled*3)
    {
      lightfrombuffer();
    }
    else 
    {
      lightoff();
    }
  }
}  


