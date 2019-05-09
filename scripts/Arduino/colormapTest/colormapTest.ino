/* 
 *  colormap
 */

#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 250
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);

// put your setup code here, to run once:
  int r = 0;
  int g = 0;
  int b = 0;

  uint32_t colors[NBLED];
  int i;

void setup() {
  // Init Leds
   strip.begin();
   strip.show();

  for(i=0;i<NBLED;i++)
  {
    // BluePink
    colors[i] = strip.Color(i/4,0,NBLED/2-i/2); 
    
    // toSunlight 
    /*
    if(i < NBLED/2) {
      colors[i] = strip.Color(i*5,0,0); 
    } else {
      colors[i] = strip.Color(i*5,round((i-NBLED/2)*10),0); 
    } 
    */
    
    // spectre 
    /*
    if(i < NBLED/3) {
      colors[i] = strip.Color(NBLED-i*3,i*3,0); 
    } else if(i < 2*NBLED/3) {
      colors[i] = strip.Color(0,NBLED-i*3,i*3);
    } else {
      colors[i] = strip.Color(i*3,0,NBLED-i*3);
    }*/

  }
}

void loop() {
  // put your main code here, to run repeatedly:
  for(i=0;i<NBLED;i++)
  {
    strip.setPixelColor(i,colors[i]);
  }
  strip.show();
}
