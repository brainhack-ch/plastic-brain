#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 200
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);


int i=0;
uint32_t c=0, black = 0, colors[6];
int currColor = 0;
int colorIndex = 0;

 
static char input_led [NBLED*3] ; 

void setup ()
  {
   colorIndex = 0;
   currColor = 1;
   black = strip.Color(0,0,0);
   colors[0] = strip.Color(100,0,0);
   colors[1] = strip.Color(70,70,0);
   colors[2] = strip.Color(0,100,0);
   colors[3] = strip.Color(0,70,70);
   colors[4] = strip.Color(0,0,100);
   colors[5] = strip.Color(70,0,70);
   c=colors[0];

   // Init Leds
   strip.begin();
  } // end of setup

void oneByOne(){
  for(i=0;i<NBLED;i++)
     {
       if (i == colorIndex)
         strip.setPixelColor(i,c);
       else
         strip.setPixelColor(i,black);
     }
     strip.show();
}

void loop()
  {
  if (colorIndex >= NBLED){
    colorIndex = 0;
    c = colors[currColor];
    currColor++;
    if (currColor >= 6)
      currColor = 0;
  }
  oneByOne();
  colorIndex++;
  delay(5000);
}  
