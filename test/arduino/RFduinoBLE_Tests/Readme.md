#BLE receiver

##Target 0: BulkDataTransfer sketch (Done)

Running BulkDataTransfer.ino sketch included with RFduino reports data rate 19200 bps = 2.4 KB/s. Moreover, getConnInterval() returns 50ms, which means we can connect 20 times per second and each connection can transmit 6 packets of 20 bytes, which gives the data rate of 20x6x20 = 2400 B/s. Calling updateConnInterval() does not seem to make any difference. So with this configuration we can transmit 120 samples per second with 20 bytes per sample.

Changing MTU can theoretically change the default packet size, which is 20 bytes. I am not able to change neither the connection interval nor MTU and hence the packet size.

The serial port together with BLE works up-to 57600 bauds or 5760 B/s. We have tried 74880 bauds but BLE would stop working. So there is no hope for 250 packets of 33 bytes per second, sinse 250x33 = 8250 > 5760 B/s.

5760 = 120x48 = 240x24 = 250x23.04

250=2x5x5x5

120=2x2x2x3x5

2x2x2x3x5x5x5=3000=250x12=120x25=100x30

lcm(120, 250) = 3000

250x24 = 120x50 = 6000 - would be the ideal but it would not work over serial 5760 bauds even if we could increase MTU

240x10 = 120x20 = 2400 - this is the best we can hope for without increasing the MTU or decreasing the connection interval

```
sudo apt-get install bluez python-bluez libbluetooth-dev
sudo pip install gattlib
git clone git@github.com:roman3017/OpenBCI_Radios.git -b ble
cd OpenBCI_Radios/test/arduino/RFduinoBLE_Tests/
sudo python bulkdatareceive.py
```

##Target 1: Serial to BLE bridge (Done)

PC creates array of 20 bytes terminated with '@' and sends it to RFduino over serial connection simulating OpenBCI.
RFduino reads up to 20 bytes delimited by '@' from the seraial port and forwards them to BLE. PC gets notified and reads the data back.

 - load RFduinoBLE1.ino to RFduino host (dongle) with Arduino IDE
 - run gattlibtest1.py as superuser
 - to interrupt, press Ctrl-C twice

```
sudo python gattlibtest1.py
```

The 20 bytes packet is sent over serial port every 50ms, which corresponds to (1000/50)*20 = 400 B/s, while having serial speed at 57.6 Kbauds. It is meant as a proof of concept to test both serial and BLE communications.

##Target 2: Speed improvement to carry data for at least 4 channels (WIP)

PC sends 20 bytes of data to RFduino over serial connection. Data starts with character 'A' and ends with character '@'. The second character is counter. RFduino returns them back over BLE. We count number of received errors under different throughputs.

 - load RFduinoBLE2.ino to RFduino host (dongle) with Arduino IDE
 - run gattlibtest2.py as superuser
 - to interrupt, press Ctrl-C twice

Since connection interval is 50ms and there are at most 6 packets per connection we can transmit 120 packets per second. The default 20 bytes packets mean the transfer rate is 20x6x20 = 2400 B/s.

```
sudo python gattlibtest2.py
```

To keep data from all 8 channels would require 3 + 8x3 = 27 bytes per packet but 57600 baud rate would not allow over 23 bytes per packet if we transfer 250 packets per second:

5760 = 120x48 = 240x24 = 250x23.04

Therefore not only the serial connection speed but also frame rate and packet size may need to be modified on the main board side to get something sensible.

If we want to keep the start, count and stop bytes + 4 channels, we need at least 3 + 4x3 = 15 bytes per packet. Yet another possibility is to use just 4-bit counter and merge it with the start byte. Then 4 channels would require 14 bytes.

First we will send and receive packets of 14 and 20 bytes with rate:

120x20 = 2400

It would be bit nicer if we could set the sample rate to 240 samples/s instead of 250 samples/s.

|packet size\delta|8ms           |9ms           |12ms          |16ms           |20ms           |
|-----------------|--------------|--------------|--------------|---------------|---------------|
|14               |10%           |8%            |6%            |4%             |3%             |
|20               |11%           |9%            |6%            |5%             |3%             |
The table shows error rates

The period between serially transmitted packets should be greater than 20x1000/2400 = 8.33ms.

Note that the transfer rate 2400 B/s means less than 10 bytes per sample with 250 samples per second (2 channels) or 19 bytes per sample with 125 samples per second (5 channels). For our goal to have at least 4 channels we will use 125 samples per second by discarding every second sample.

Q: should we increase the precision by taking the average instead of discarding odd samples?

##Target 3: Real data over BLE (TODO)

Load the code to RFduino device and get the EEG data from OpenBCI over BLE without the use of RFduino host.

##Notes

Per the specifics of the BLE protocol, if the command requires a response larger than 20
bytes, the attribute MTU size should be increased. To support the responses with data
length set to 56 (response for Get Metadata command), the attribute MTU size should be
set to 66. This can be seen from the following equation:

```
MTU size = Data Length + Bootloader command overhead + notification parameters overhead
```

Where:

 - Data Length = the response data length
 - Bootloader command overhead = 7
 - Notification parameters overhead = 3

Not following this will result in the BLE component failing to send a response to the requested command.

##References:

 - ​https://bitbucket.org/OscarAcena/pygattlib
 - https://atmosphere.anaren.com/wiki/Data_rates_using_BLE
 - http://www.cypress.com/file/220246/download
