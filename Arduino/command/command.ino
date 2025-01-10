// Uduino Default Board
#include<Uduino.h>
Uduino uduino("uduinoBoard"); // Declare and name your object

// Servo
#include <Servo.h>
#define MAXSERVOS 8


void setup()
{
  Serial.begin(9600);

#if defined (__AVR_ATmega32U4__) // Leonardo
  while (!Serial) {}
#elif defined(__PIC32MX__)
  delay(1000);
#endif

  /*
  uduino.addCommand("s", SetMode);
  uduino.addCommand("d", WritePinDigital);
  uduino.addCommand("a", WritePinAnalog);
  uduino.addCommand("rd", ReadDigitalPin);
  uduino.addCommand("r", ReadAnalogPin);
  uduino.addCommand("br", BundleReadPin);
  uduino.addCommand("b", ReadBundle);
  uduino.addInitFunction(DisconnectAllServos);
  uduino.addDisconnectedFunction(DisconnectAllServos);
  */
}

void ReadBundle() {
  char *arg = NULL;
  char *number = NULL;
  number = uduino.next();
  int len = 0;
  if (number != NULL)
    len = atoi(number);
  for (int i = 0; i < len; i++) {
    uduino.launchCommand(arg);
  }
}

void SetMode() {
  int pinToMap = 100; //100 is never reached
  char *arg = NULL;
  arg = uduino.next();
  if (arg != NULL)
  {
    pinToMap = atoi(arg);
  }
  int type;
  arg = uduino.next();
  if (arg != NULL)
  {
    type = atoi(arg);
    PinSetMode(pinToMap, type);
  }
}

void PinSetMode(int pin, int type) {
  //TODO : vérifier que ça, ça fonctionne
  if (type != 4)
    DisconnectServo(pin);

  switch (type) {
    case 0: // Output
      pinMode(pin, OUTPUT);
      break;
    case 1: // PWM
      pinMode(pin, OUTPUT);
      break;
    case 2: // Analog
      pinMode(pin, INPUT);
      break;
    case 3: // Input_Pullup
      pinMode(pin, INPUT_PULLUP);
      break;
    case 4: // Servo
      SetupServo(pin);
      break;
  }
}

void WritePinAnalog() {
  int pinToMap = 100;
  char *arg = NULL;
  arg = uduino.next();
  if (arg != NULL)
  {
    pinToMap = atoi(arg);
  }

  int valueToWrite;
  arg = uduino.next();
  if (arg != NULL)
  {
    valueToWrite = atoi(arg);

    if (ServoConnectedPin(pinToMap)) {
      UpdateServo(pinToMap, valueToWrite);
    } else {
      analogWrite(pinToMap, valueToWrite);
    }
  }
}

void WritePinDigital() {
  int pinToMap = -1;
  char *arg = NULL;
  arg = uduino.next();
  if (arg != NULL)
    pinToMap = atoi(arg);

  int writeValue;
  arg = uduino.next();
  if (arg != NULL && pinToMap != -1)
  {
    writeValue = atoi(arg);
    digitalWrite(pinToMap, writeValue);
  }
}

void ReadAnalogPin() {
  int pinToRead = -1;
  char *arg = NULL;
  arg = uduino.next();
  if (arg != NULL)
  {
    pinToRead = atoi(arg);
    if (pinToRead != -1)
      printValue(pinToRead, analogRead(pinToRead));
  }
}

void ReadDigitalPin() {
  int pinToRead = -1;
  char *arg = NULL;
  arg = uduino.next();
  if (arg != NULL)
  {
    pinToRead = atoi(arg);
  }

  if (pinToRead != -1)
    printValue(pinToRead, digitalRead(pinToRead));
}

void BundleReadPin() {
  int pinToRead = -1;
  char *arg = NULL;
  arg = uduino.next();
  if (arg != NULL)
  {
    pinToRead = atoi(arg);
    if (pinToRead != -1) {
      if (pinToRead < 13)
        printValue(pinToRead, digitalRead(pinToRead));
      else
        printValue(pinToRead, analogRead(pinToRead));
    }
  }
}

Servo myservo;
void loop()
{
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // コマンドを受信
    input.trim(); // 不要な空白を除去

    // コマンドの解析
    if (input.startsWith("d")) { // デジタルピン制御
        int spaceIndex = input.indexOf(' ');
        String pinAndValue = input.substring(spaceIndex + 1);
        int pin = pinAndValue.substring(0, pinAndValue.indexOf(' ')).toInt();
        int value = pinAndValue.substring(pinAndValue.indexOf(' ') + 1).toInt();

        digitalWrite(pin, value);
        Serial.println("Digital pin " + String(pin) + " set to " + String(value));
    } else if (input.startsWith("a")) { // アナログピン制御
        int spaceIndex = input.indexOf(' ');
        String pinAndValue = input.substring(spaceIndex + 1);
        int pin = pinAndValue.substring(0, pinAndValue.indexOf(' ')).toInt();
        int value = pinAndValue.substring(pinAndValue.indexOf(' ') + 1).toInt();

        analogWrite(pin, value);
        Serial.println("Analog pin " + String(pin) + " set to " + String(value));
    } else if (input.startsWith("rd")) { // デジタルピンの値を読み取る
        int pin = input.substring(3).toInt();
        int value = digitalRead(pin);
        Serial.println("Digital pin " + String(pin) + " is " + String(value));
    } else if (input.startsWith("r")) { // アナログピンの値を読み取る
        String pinString = input.substring(2); // ピン番号を取得 (例: "A0" または "0")
        int pin;

        if (pinString.startsWith("A")) { // アナログピン (例: A0)
            pin = pinString.substring(1).toInt(); // "A" を除いて番号を取得
            pin = pin + A0; // A0 基準のピン番号に変換
        } else { // 数字のみの場合 (例: "0")
            pin = pinString.toInt();
        }

        int value = analogRead(pin);
        Serial.println("Analog pin " + pinString + " is " + String(value));
    } else {
        Serial.println("Unknown command: " + input);
    }
  }

}

void printValue(int pin, int targetValue) {
  uduino.print(pin);
  uduino.print(" "); //<- Todo : Change that with Uduino delimiter
  uduino.println(targetValue);
  // TODO : Here we could put bundle read multiple pins if(Bundle) { ... add delimiter // } ...
}




/* SERVO CODE */
Servo servos[MAXSERVOS];
int servoPinMap[MAXSERVOS];
/*
  void InitializeServos() {
  for (int i = 0; i < MAXSERVOS - 1; i++ ) {
    servoPinMap[i] = -1;
    servos[i].detach();
  }
  }
*/
void SetupServo(int pin) {
  if (ServoConnectedPin(pin))
    return;

  int nextIndex = GetAvailableIndexByPin(-1);
  if (nextIndex == -1)
    nextIndex = 0;
  servos[nextIndex].attach(pin);
  servoPinMap[nextIndex] = pin;
}


void DisconnectServo(int pin) {
  servos[GetAvailableIndexByPin(pin)].detach();
  servoPinMap[GetAvailableIndexByPin(pin)] = 0;
}

bool ServoConnectedPin(int pin) {
  if (GetAvailableIndexByPin(pin) == -1) return false;
  else return true;
}

int GetAvailableIndexByPin(int pin) {
  for (int i = 0; i < MAXSERVOS - 1; i++ ) {
    if (servoPinMap[i] == pin) {
      return i;
    } else if (pin == -1 && servoPinMap[i] < 0) {
      return i; // return the first available index
    }
  }
  return -1;
}

void UpdateServo(int pin, int targetValue) {
  int index = GetAvailableIndexByPin(pin);
  servos[index].write(targetValue);
  delay(10);
}

void DisconnectAllServos() {
  for (int i = 0; i < MAXSERVOS; i++) {
    servos[i].detach();
    digitalWrite(servoPinMap[i], LOW);
    servoPinMap[i] = -1;
  }
}
