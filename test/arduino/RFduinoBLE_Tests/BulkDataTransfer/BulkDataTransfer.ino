/*
 Copyright (c) 2013 OpenSourceRF.com.  All right reserved.

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

/*
This sketch demonstrates how to do error free bulk data
transfer over Bluetooth Low Energy 4.

The data rate should be approximately:
  - 32 kbit/sec at 1.5ft (4000 bytes per second)
  - 24 kbit/sec at 40ft (3000 bytes per second)

This sketch sends a fixed number of 20 byte packets to
an iPhone application.  Each packet is different, so
that the iPhone application can verify if any data or
packets were dropped.
*/

#include <RFduinoBLE.h>

//int baudrate = 74880;
//int baudrate = 60000;
//int baudrate = 57600;
//int baudrate = 38400;
//int baudrate = 19200;
int baudrate = 9600;

#define PKTSIZE 20
// send 500 20 byte buffers = 10000 bytes
int packets = 500;
char buf[PKTSIZE];

// flag used to start sending
int flag = false;

// variables used in packet generation
int ch;
int packet;

int start;

void setup() {
  Serial.begin(baudrate);
  Serial.println("Waiting for connection...");
  RFduinoBLE.begin();
  RFduinoBLE.updateConnInterval(8, 20);
  Serial.print(RFduinoBLE.getConnInterval());
  Serial.println("s");
}

void RFduinoBLE_onConnect() {
  packet = 0;
  ch = 'A';
  start = 0;
  flag = true;
  Serial.println("Sending");
  // first send is not possible until the iPhone completes service/characteristic discovery
}

void loop() {
  if (flag)
  {
    // generate the next packet
    for (int i = 0; i < sizeof(buf); i++)
    {
      buf[i] = ch;
      ch++;
      if (ch > 'Z')
        ch = 'A';
    }

    // send is queued (the ble stack delays send to the start of the next tx window)
    while (! RFduinoBLE.send(buf, sizeof(buf)))
      ;  // all tx buffers in use (can't send - try again later)

    if (! start)
      start = millis();

    packet++;
    if (packet >= packets)
    {
      int end = millis();
      float secs = (end - start) / 1000.0;
      int bps = ((packets * sizeof(buf)) * 8) / secs;
      Serial.println("Finished");
      Serial.println(start);
      Serial.println(end);
      Serial.print(secs);
      Serial.println("s");
      Serial.print(bps / 1000.0);
      Serial.println("kbps");
      Serial.print(RFduinoBLE.getConnInterval());
      Serial.println("s");
      flag = false;
    }
  }
}

