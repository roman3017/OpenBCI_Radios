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
BAUDRATE = 57600
#BAUDRATE = 38400
#BAUDRATE = 19200
#BAUDRATE = 9600

PACKETS = 1000
PKTSIZE = 20
DELTA = 0.0085
DATA = bytearray(x+ord('A') for x in range(PKTSIZE))
RUNNING = [True]
nn = [-1, 1]
ee = [ 1, 1]
SENT = [0]
RCV = []

DEVICE = "hci0"
MACADDR = "D1:D3:5E:4E:B8:37"
TYPE = "random"
SEC = "low"
PSM = 0
MTU = PKTSIZE+7+3
MTU = 0

ser = serial.Serial(
	port=PORT,
	baudrate=BAUDRATE,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS)

def transferData(cc):
	DATA[-1] = ord('@')
	DATA[1] = cc
	ser.write(str(DATA))
	SENT[0] = SENT[0]+1
	#print "data sent: /", DATA, "/", time.time()
	#print "s", cc,
	if (PACKETS == SENT[0]): RUNNING[0] = False
	else: Timer(DELTA, transferData, [(cc+1)&0xff]).start()

class Response(GATTResponse):
	def on_response(self, data):
		#print "response received: /", data, "/", time.time()
		print "r",

class Requester(GATTRequester):
	def on_notification(self, handle, data):
		#print "n",
		ardata = bytearray(data[3:])
		RCV.extend( ardata )

	def on_indication(self, handle, data):
		#print "indication received: /", data, "/", hex(handle), time.time()
		print "i",

def main():
	if ser.isOpen(): ser.close()
	ser.open()

	req = Requester(MACADDR, False, DEVICE)
	req.disconnect()
	req.connect(True, TYPE, SEC, PSM, MTU)

	#res = Response()
	#req.read_by_handle_async(0xe, res)
	req.write_by_handle(0xf, bytes("10"))

	start = time.time()
	transferData(0)
	while RUNNING[0]:
		time.sleep(0.1)
		#print "."
	end = time.time()

	#print map(chr, RCV), len(RCV), len(RCV)/PKTSIZE
	for ii in range(0, len(RCV)/PKTSIZE):
		nn[1] = RCV[PKTSIZE*ii+1]
		#print nn[1]
		if (((nn[0]+1)&0xff) != nn[1] or ord('A') != RCV[PKTSIZE*ii] or ord('@') != RCV[PKTSIZE*ii+PKTSIZE-1]):
			#print "ERROR: ", nn
			ee[0] = ee[0] + 50 #error increments twice
		ee[1] = ee[1] + 1
		nn[0] = nn[1]
	print "errors: ", ee[0]/ee[1], "%,", len(RCV)/PKTSIZE, len(RCV)*2/(end - start)

if __name__ == "__main__":
  main()

