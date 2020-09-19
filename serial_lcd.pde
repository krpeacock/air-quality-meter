//Sample using LiquidCrystal library
#include <LiquidCrystal.h>
 
// select the pins used on the LCD panel
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
 
// define some values used by the panel and buttons
int last_message = 0;
int lcd_key     = 0;
int adc_key_in  = 0;
int prev_screen = 99;
int current_screen = 0;
String inputString = "";        // a String to hold incoming data
String prev_data = "";
String serialData [ 3 ];
String line1 = "";
int interrupt_count = 0;
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
 checkUpdateDisplay();
}
void(* resetFunc) (void) = 0; //declare reset function @ address 0

void loop()
{
  interrupt_count ++;
  if(interrupt_count > 32000)
  {
//    prev_data = "";
//    prev_screen = 99;
//    lcd.begin(16, 2);
//    checkUpdateDisplay();
//    interrupt_count = 0;
      resetFunc();  //call reset
  }
  lcd_key = read_LCD_buttons();
  if(lcd_key != last_message){
   last_message = lcd_key;
   Serial.print(lcd_key); 
  }
}

void checkUpdateDisplay()
{
 if(current_screen == prev_screen)
 {   
    lcd.setCursor(0, 1); // bottom left
    lcd.write(" ");
    lcd.write(" ");
    lcd.write(" ");
    lcd.setCursor(0,1);
    for(auto x : serialData[current_screen])
    {
      lcd.write(x);
    }
 }
 else {
   lcd.clear();
   line1 = "Air Quality 2.5";
   for(auto x : line1)
    {
      lcd.write(x);
    }
    lcd.setCursor(0,1);
    if(serialData[current_screen]){
      lcd.print(serialData[current_screen]);
    }
 }
 prev_screen = current_screen;
 prev_data = serialData[current_screen];
}

void serialEvent()
{
  memset(serialData,0,sizeof serialData); 
  while (Serial.available()) {
    inputString = '\0';
    // wait a bit for the entire message to arrive
    delay(100);
    while (Serial.available() > 0) {
      // display each character to the LCD
      char inChar = (char)Serial.read();
      inputString += inChar;
    }
    int i = 0;
    for(auto x : inputString)
    {
      if(x == ','){
        i ++;
        break;
      }
      serialData[i] += x;
    }
    checkUpdateDisplay();
  }
}