// BrainHack 2019
// Manik Victor Jorge Elif Jelena Italo Gaetan
//
// convert and transmit the data into ligth. Different colormap
// can be used.
//
// next : bleutooth and power bank

#include <Adafruit_NeoPixel.h>
#define PIN 6        // the pin that transmit the signal to led strip
#define NBLED 191    // the number of LED in the strip
#define COLORMAP 1   // 1. Blue2Red 2. toSunlight 3. spectrum (default is 1)
#define MAXCOLOR 200 // use that if you want to change the intensity of the ligth (range : [1;255])
// Init de Adafruit
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NBLED, PIN, NEO_GRB + NEO_KHZ800);

uint32_t led_tab[NBLED]; // the tab that store the led position EEG power

char reading;
bool status_led;
uint8_t led_value_from_0_to_255;

// reset all the led to zero
void flushligth() {
  for (int i = 0; i < NBLED; i++)
  {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
  }
  strip.show();
}

// transmit the value of the led to the plastic brain
void printligth() {
  for (int i = 0; i < NBLED; i++)
  {
    strip.setPixelColor(i, led_tab[i]);
  }
  strip.show();
}

void setup() {
  // Init serial connection
  Serial.begin(115200);
  //Init Leds to zero (no ligth)
  strip.begin();
  
  flushligth();
  printligth();

  // checking led initialisation
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, status_led); status_led = !status_led;
}

void loop() {
  // data is read at each loop
  if (Serial.available() > 0) {
    if (reading == 'S') {
      digitalWrite(LED_BUILTIN, status_led); status_led = !status_led;

      for (int i = 0; i < NBLED; i++) {
        while (!Serial.available());             // Wait the buffer
        led_value_from_0_to_255 = Serial.read(); // retrieve the value of led i
        
        // select the color associate with the choose colormap
        if (COLORMAP == 1) { // 1. Blue2Red 
          led_tab[i] = strip.Color(led_value_from_0_to_255, 0, (255 - led_value_from_0_to_255));
    
        } else if (COLORMAP == 2) { // 2. toSunlight 
          if (i < NBLED / 2) {
            led_tab[i] = strip.Color(led_value_from_0_to_255, 0, 0);
          } else {
            led_tab[i] = strip.Color(led_value_from_0_to_255, round(((led_value_from_0_to_255 - 255 / 2) * 2)), 0);
          }
    
        } else if (COLORMAP == 3) { // 3. spectrum
          if (i < 255 / 3) {
            led_tab[i] = strip.Color((255 - led_value_from_0_to_255), (led_value_from_0_to_255), 0);
          } else if (i < 2 * 255 / 3) {
            led_tab[i] = strip.Color(0, (255 - led_value_from_0_to_255), (led_value_from_0_to_255));
          } else {
            led_tab[i] = strip.Color((led_value_from_0_to_255), 0, (255 - led_value_from_0_to_255));
          }
    
        } else { // default. Blue2Red
          led_tab[i] = strip.Color(led_value_from_0_to_255, 0, (255 - led_value_from_0_to_255));
        } 
      }
      digitalWrite(LED_BUILTIN, status_led); status_led = !status_led;
      printligth(); 
    } else { // flush the buffer
      reading = Serial.read();
    }
  }
}
