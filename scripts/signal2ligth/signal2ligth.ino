#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NBLED 191
#define COLORMAP 1 // 1. Blue2Red 2. toSunlight 3. spectrum (default is 1)
#define NCOLOR 256
#define MAXCOLOR 200
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);

uint32_t colors[NCOLOR];
uint32_t led_tab[NBLED];

char reading;
bool status_led;
uint8_t led_value_from_0_to_255;

void setmap(int colormap) {
  double q = double(MAXCOLOR) / double(NCOLOR);
  for (int i = 0; i < NCOLOR; i++)
  {
    if (colormap == 1) {
      colors[i] = strip.Color(i * q, 0, (NBLED - i - 1) * q);

    } else if (colormap == 2) {
      if (i < NBLED / 2) {
        colors[i] = strip.Color(i * q, 0, 0);
      } else {
        colors[i] = strip.Color(i * q, round(((i - NBLED / 2) * 2) * q), 0);
      }

    } else if (colormap == 3) {
      if (i < NBLED / 3) {
        colors[i] = strip.Color((NBLED - i * 3) * q, (i * 3) * q, 0);
      } else if (i < 2 * NBLED / 3) {
        colors[i] = strip.Color(0, (NBLED - i * 3) * q, (i * 3) * q);
      } else {
        colors[i] = strip.Color((i * 3) * q, 0, (NBLED - i * 3) * q);
      }

    } else {
      colors[i] = strip.Color(i * q, 0, (NBLED - i - 1) * q);
    }
  }
}

void flushligth() {
  for (int i = 0; i < NBLED; i++)
  {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
  }
  strip.show();
}

void printligth() {
  for (int i = 0; i < NBLED; i++)
  {
    strip.setPixelColor(i, led_tab[i]);
    //strip.setPixelColor(i, strip.Color(100, 0, 0));
  }
  strip.show();
}

void setup() {
  // setmap(COLORMAP);
  Serial.begin(115200);
  //Init Leds to zero (no ligth)
  strip.begin();
  flushligth();
  /* for (int i = 0; i < NBLED; i++)
    {
     led_tab[i] = strip.Color(0, 100, 0);
    }*/
  printligth();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, status_led); status_led = !status_led;
}

void loop() {
  // data -> S1533984583583458345494455
  if (Serial.available() > 0) {
    if (reading == 'S') {
      digitalWrite(LED_BUILTIN, status_led); status_led = !status_led;

      for (int i = 0; i < NBLED; i++) {
        while (!Serial.available()); // Wait the buffer
        led_value_from_0_to_255 = Serial.read();
        //led_tab[i] = colors[led_value_from_0_to_255];
        led_tab[i] = strip.Color(255 - led_value_from_0_to_255, led_value_from_0_to_255, 0);
      }
      // reading = '0';
      digitalWrite(LED_BUILTIN, status_led); status_led = !status_led;
      printligth();
    } else {
      reading = Serial.read();
    }
  }
}
