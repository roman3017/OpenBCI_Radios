/*
* RFduinoBLE1.ino roman3017
* reads up to 16 bytes delimited by @ from serial port and forwards them to BLE
*/

#include <RFduinoBLE.h>

//int baudrate = 74880;
int baudrate = 57600;
//int baudrate = 38400;
//int baudrate = 19200;
//int baudrate = 9600;

int notificationLED = 2;
char buf[20];
int idx = 0;
int flag = false;

void setup()
{
  override_uart_limit = true;
  Serial.begin(baudrate);
  pinMode(notificationLED, OUTPUT);
  RFduinoBLE.begin();
}

void loop()
{
  if (flag) {
    while (! RFduinoBLE.send(buf, sizeof(buf)))
      /* noop */;
    flag = false;
  }
  else RFduino_ULPDelay(10);
}

void serialEvent()
{
  digitalWrite(notificationLED, HIGH);
  while (Serial.available()) {
    char ch = (char)Serial.read();
    buf[idx] = ch;
    idx = (idx+1)%sizeof(buf);
    if (ch == '@') {
      idx = 0;
      flag = true;
    }
  }
  digitalWrite(notificationLED, LOW);
}
