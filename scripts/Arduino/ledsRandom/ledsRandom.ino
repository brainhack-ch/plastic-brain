#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 144
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);


int i=0;
uint32_t c=0, black = 0, colors[NBLED];
int currColor = 0;
int colorIndex = 0;

 
static char input_led [NBLED*3] ; 

void oneByOne(){
  for(i=0;i<NBLED;i++)
     {
         strip.setPixelColor(i,100,50,0);//colors[(3*i+3*offset)%NBLED]);
     }
     strip.show();
}

void setup ()
  {
   colorIndex = 0;

   /*for(i=0;i<NBLED;i++)
     colors[i] = strip.Color(random(2,50),random(2,60),random(2,40));*/


   // Init Leds
   strip.begin();
   strip.show();
   //oneByOne();
  } // end of setup

void loop()
  {
  if (colorIndex >= NBLED){
    colorIndex = 0;
  }
  oneByOne();
  colorIndex++;
  delay(400);
}  


