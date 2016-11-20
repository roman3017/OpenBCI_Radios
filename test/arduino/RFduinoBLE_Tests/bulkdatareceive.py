# gattlibtest2.py by roman3017
# https://bitbucket.org/OscarAcena/pygattlib
# apt-get install libbluetooth-dev
# pip install gattlib

from gattlib import GATTRequester, GATTResponse
from threading import Timer
import time
import serial
import sys

PORT = "/dev/ttyUSB1"
#BAUDRATE = 74880
#BAUDRATE = 57600
#BAUDRATE = 38400
#BAUDRATE = 19200
BAUDRATE = 9600

PKTSIZE = 20
DEVICE = "hci0"
MACADDR = "D1:D3:5E:4E:B8:37"
TYPE = "random"
SEC = "low"
PSM = 0
MTU = PKTSIZE+7+3

ser = serial.Serial(
	port=PORT,
	baudrate=BAUDRATE,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS)

class Response(GATTResponse):
	def on_response(self, data):
		#print "response received: /", data, "/", time.time()
		print "r",

class Requester(GATTRequester):
	def on_notification(self, handle, data):
		#print "notification received: /", data[3:], "/", hex(handle), time.time(), len(data)
		print ".",

	def on_indication(self, handle, data):
		#print "indication received: /", data, "/", hex(handle), time.time()
		if (PKTSIZE==len(data)): print "i",
		else: print data

def main():
	if ser.isOpen():
		ser.close()
	ser.open()

	req = Requester(MACADDR, False, DEVICE)
	req.disconnect()
	req.connect(True, TYPE, SEC, PSM, MTU)

	#res = Response()
	#req.read_by_handle_async(0xe, res)
	req.write_by_handle(0xf, bytes("10"))

	while True:
		print ser.readline()

if __name__ == "__main__":
  main()
