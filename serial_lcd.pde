#include <LiquidCrystal.h>
#include <LCDKeypad.h>

LCDKeypad lcd;

const int bufferlen = 52;
int screen = 0;
char str[bufferlen + 1];
bool stringComplete = false;
int counter = 0;

void setup()
{
  lcd.begin(16, 2);
  Serial.begin(9600);
  lcd.setCursor(0, 0);
}
void(* resetFunc) (void) = 0; //declare reset function @ address 0

void renderScreen()
{
  Serial.write(str);

  char copy[bufferlen + 1];
  strncpy(copy, str, bufferlen);
  char *data1 = strtok(copy, ",");
  char *data2 = strtok(NULL, ",");
  char *data3 = strtok(NULL, ",");

  lcd.clear();
  switch (screen) {
    case 0:
      lcd.print("Air Quality");
      lcd.setCursor(0, 1);
      lcd.print(data1);
      Serial.write(data1);
      break;
    case 1:
      lcd.print("2.5nm AQI");
      lcd.setCursor(0, 1);
      lcd.print(data2);
      break;
    case 2:
      lcd.print("10nm AQI");
      lcd.setCursor(0, 1);
      lcd.print(data3);
      break;
    default:
      lcd.print("error");
      break;
  }

}

void displayOff()
{
  pinMode(10, OUTPUT);
  digitalWrite(10, LOW);
}

void displayOn()
{
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
}

void loop()
{
  int initialScreen = screen;
  switch (lcd.buttonBlocking()) {
    case KEYPAD_LEFT:
      displayOff();
      break;
    case KEYPAD_RIGHT:
      displayOn();
      break;
    case KEYPAD_DOWN:
      if (screen != 2) {
        screen ++;
      }
      break;
    case KEYPAD_UP:
      if (screen != 0) {
        screen --;
      }
      break;
    case KEYPAD_SELECT:

      break;
  }
  if (initialScreen != screen)
  {
    renderScreen();
  }
}

void serialEvent()
{
  if (Serial.available() > 0) {
    // get the new byte:
    char inChar = (char)Serial.read();

    if (inChar == '\n' || counter > bufferlen) {
      str[counter++] = 0;
      renderScreen();
      counter = 0;
    }
    else {
      str[counter++] = inChar;
    }

  }
}