# Author: Raf, Sako

# Imports
import os
import sys
from time import *
from decimal import *
import serial
import re
import colorsys
import pdb

# Commands

## Commands for initializing
overflow_watchdog = 'OZ'
power_mode = 'PA'
invalid_type = 'BZ'
wait_between = 'WI'
sample frequency = 'S2'
baud_rate = 'I2'

## Commands for speed
speed_on1 = 'O2'
speed_units = 'uM'
speed_limit = 'M>0'
speed_off = 'Os'

## Commands for range
range_on1 = 'o2'
range_units = 'uM' # = speed_units but ok
range_limit = 'm>0'
range_off = 'Od'

# Serial interface
ser = serial.Serial (
	port = '/dev/ttyACM0',
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1,
	writeTimeout = 2
)
ser.flushInput()
ser.flushOutput()

def main ():
	print("--OPS243 Radar--")
	print("Initializing serial /dev/ttyACM0 @ 9600..")
	
	send

def readSpeed ():
	send_serial_cmd(range_off)
	send_serial_cmd(speed_on1)
	send_serial_cmd(speed_units)
	send_serial_cmd(speed_limit)

def readRange ():
	send_serial_cmd(speed_off)
	send_serial_cmd(range_on1)
	send_serial_cmd(range_units)
	send_serial_cmd(range_limit)
	
	radarRead = ser.readline()
	if (len(radarRead) != 0):
		


def send_serial_cmd (command):
	data_for_send_str = command
	data_for_send_bytes = str.encode(data_for_send_str)
	ser.write(data_for_send_bytes)
	# Initialize message verify checking
	ser_message_start = '{'
	ser_write_verify = False
	# Print out module response to command string
	while not ser_write_verify:
		data_rx_bytes = ser.readline()
		data_rx_length = len(data_rx_bytes)
		if (data_rx_length != 0):
			data_rx_str = str(data_rx_bytes)
			if data_rx_str.find(ser_message_start):
				ser_write_verify = True

if __name__ == "__main__":
	main()
