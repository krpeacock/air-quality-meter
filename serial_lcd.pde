//Sample using LiquidCrystal library
#include <LiquidCrystal.h>
 
// select the pins used on the LCD panel
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
 
// define some values used by the panel and buttons
int last_message = 0;
int lcd_key     = 0;
int adc_key_in  = 0;
int current_line = 0;
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

// read the buttons
int read_LCD_buttons()
{
 adc_key_in = analogRead(0);      // read the value from the sensor
 // my buttons when read are centered at these valies: 0, 144, 329, 504, 741
 // we add approx 50 to those values and check to see if we are close
 if (adc_key_in > 1000) return btnNONE; // We make this the 1st option for speed reasons since it will be the most likely result
 if (adc_key_in < 50)   return btnRIGHT; 
 if (adc_key_in < 195)  return btnUP;
 if (adc_key_in < 380)  return btnDOWN;
 if (adc_key_in < 555)  return btnLEFT;
 if (adc_key_in < 790)  return btnSELECT;  
 return btnNONE;  // when all others fail, return this...
}
 
void setup()
{
 lcd.begin(16, 2);
 Serial.begin(9600);
 // reserve 200 bytes for the inputString:
 inputString.reserve(200);
 lcd.setCursor(0,0);
}
  
void loop()
{
  lcd_key = read_LCD_buttons();
  if(lcd_key != last_message){
   last_message = lcd_key;
   Serial.print(lcd_key); 
  }
}

void serialEvent()
{
  while (Serial.available()) {
    lcd.clear();
    inputString = '\0';
    // wait a bit for the entire message to arrive
    delay(100);
    while (Serial.available() > 0) {
      // display each character to the LCD
      char inChar = (char)Serial.read();
      inputString += inChar;
    }
    for(auto x : inputString)
    {
      if(x == '\n'){
        lcd.setCursor(0,1);
      }
      else {
        lcd.write(x);
      }
    }
  }
}