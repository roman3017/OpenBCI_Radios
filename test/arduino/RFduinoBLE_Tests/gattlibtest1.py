# gattlibtest1.py by roman3017
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
BAUDRATE = 57600
#BAUDRATE = 38400
#BAUDRATE = 19200
#BAUDRATE = 9600

DEVICE = "hci0"
MACADDR = "D1:D3:5E:4E:B8:37"
TYPE = "random"

ser = serial.Serial(
	port=PORT,
	baudrate=BAUDRATE,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS)

def transferData():
	data = "0123456789abcdefqwe@"
	ser.write(str(data))
	#print "data sent: [", data, "]", time.time()
	print "s",
	Timer(0.05, transferData, ()).start()

class Response(GATTResponse):
	def on_response(self, data):
		#print "response received: [", data, "]", time.time()
		print "r",

class Requester(GATTRequester):
	def on_notification(self, handle, data):
		#print "notification received: [", data, "]", hex(handle), time.time()
		print "n",
	def on_indication(self, handle, data):
		#print "indication received: [", data, "]", hex(handle), time.time()
		print "i",

def main():
	if ser.isOpen():
		ser.close()
	ser.open()
	if ser.isOpen():
		transferData()

	req = Requester(MACADDR, False, DEVICE)
	req.disconnect()
	req.connect(True, TYPE)

	#res = Response()
	#req.read_by_handle_async(0xe, res)
	req.write_by_handle(0xf, bytes("10"))

	while True:
		time.sleep(1.0)
		print ""

if __name__ == "__main__":
  main()

