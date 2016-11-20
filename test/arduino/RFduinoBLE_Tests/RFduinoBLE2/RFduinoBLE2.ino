/*
* RFduinoBLE2.ino roman3017
* reads up to 33 bytes delimited by @ from serial port and forwards 15 bytes to BLE
*/

#include <RFduinoBLE.h>

#define BUFSIZE 20

//int baudrate = 74880;
int baudrate = 57600;
//int baudrate = 38400;
//int baudrate = 19200;
//int baudrate = 9600;

char buf[6*BUFSIZE];
int notificationLED = 2;
int idx;
int flag;
int count;

void RFduinoBLE_onConnect() {
  digitalWrite(notificationLED, HIGH);
  idx = 0;
  count = 0;
  flag = false;
  digitalWrite(notificationLED, LOW);
}

void setup()
{
  override_uart_limit = true;
  Serial.begin(baudrate);
  RFduinoBLE.begin();
  RFduinoBLE.updateConnInterval(8, 10);
  pinMode(notificationLED, OUTPUT);
  digitalWrite(notificationLED, LOW);
}

void loop()
{
  if (flag) {
    int i = 0;
//    for(i = 0; i < 6; i++)
      while (! RFduinoBLE.send(buf+i*BUFSIZE, BUFSIZE));
    flag = false;
  }
  //else RFduino_ULPDelay(10);
}

void serialEvent()
{
  digitalWrite(notificationLED, HIGH);
  while (Serial.available()) {
    char ch = (char)Serial.read();
    buf[idx] = ch;
    idx = (idx+1)%sizeof(buf);
    if (ch == '@') {
      count = (count+1)%6;
//      if (0==count)
      {
      idx = 0;
      flag = true;
      }
    }
  }
  digitalWrite(notificationLED, LOW);
}
