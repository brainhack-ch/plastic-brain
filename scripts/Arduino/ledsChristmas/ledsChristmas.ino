


/*
processing incoming serial data without blocking.
*/

// how much serial data we expect before a new Led (a led =16bytes max)
const unsigned int MAX_INPUT =200;
#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 144
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);


int bytesread=0, i=0;
long couleur[4];
uint32_t c=0;
int currentLed=0;
int nbled=144;
int colorIndex = 0;
char rIndex[9] = {0, 10, 17, 28, 38, 52, 78, 96, 105};
char gIndex[8] = {8, 15, 86, 25, 72, 100, 52, 36};
char bIndex[7] = {0, 6, 18, 34, 56, 72, 108};
 
static char input_led [NBLED*3] ; 

void setup ()
  {
  // Init Leds
   strip.begin();
   strip.show();
   colorIndex = 0;
  // Init Serial port
  Serial.begin (230400);
  Serial.println("LED init ok");
  for(i=0;i<NBLED;i++)
    {
    input_led[3*1]= rIndex[i%9];
    input_led[3*1+1]= gIndex[i%8];
    input_led[3*1+2]= bIndex[i%7];
    }
    nbled = NBLED;
  } // end of setup



void lightoff()
{
  c=strip.Color(0,0,0);
  for(i=0;i<nbled;i++)
    {
      strip.setPixelColor(i,c);
   }
   strip.show();
}

void lightfrombuffer(int offset=0)
{
  
  for(i=0;i<nbled;i++)
    {
      c=strip.Color(input_led[((i+offset)%nbled)*3],input_led[((i+offset)%nbled)*3+1],input_led[((i+offset)%nbled)*3+2]);
      strip.setPixelColor(i,c);
   }
   strip.show();
}

void lightshow()
{
     for(i=0;i<NBLED;i++)
     {
       c=strip.Color(rIndex[(colorIndex+i)%9], gIndex[(colorIndex+i)%8], bIndex[(colorIndex+i)%7]);
       strip.setPixelColor(i,c);
     }
     strip.show();
     colorIndex++;
}
void loop()
  {
//  // if serial data available, process it
//  if (Serial.available ())
//  {
//    nbled=Serial.read();
//    bytesread=Serial.readBytes(input_led,nbled*3);
//    if (bytesread==nbled*3)
//    {
//      lightfrombuffer();
//    }
//    else 
//    {
//      lightoff();
//    }
//  }
  if (colorIndex == 0 || colorIndex > 400){
    lightoff();
    colorIndex = 0;
  }else{
    lightshow();
    //lightfrombuffer(colorIndex);
  }
  delay(150);
  colorIndex++;
  //lightoff();
}  


