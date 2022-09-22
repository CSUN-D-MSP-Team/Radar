# Author: Raf, Sako

# Imports
import serial
import re
import rospy
from std_msgs.msg import Int32

# Parameters
# TODO: Integrate as ros params

baud = 115200
port = '/dev/ttyACM0'
freq = 10

# Serial interface
ser = serial.Serial (
	port = port,
	baudrate = baud,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1,
	writeTimeout = 2
)
ser.flushInput()
ser.flushOutput()

# Global variables
oldRange = 0

def main ():
	print("--OPS243 Radar--")
	print("Initializing serial: ", port, " @ ", baud)

	while (1):
		radarSpeed = readSpeed()
		radarRange = readRange()
		print("Speed:", radarSpeed, "\nRange:", radarRange)

		# TODO: Add ROS publishers

def readSer ():
	radarRead = ser.readline()
	radarReadStr = str(radarRead.decode("utf-8"))
	return radarReadStr

def readSpeed ():
	global oldSpeed	
	result = readSer()
	if (not(result.find('"mps"') == -1)):
			result = re.sub("[^0-9 . - ]","", result)
		return result
	else:
		# Speed data not returned so just return -1
		return -1	

def readRange ():
	global oldRange
	result = readSer()
	if (not(result.find('"m"') == -1)):
		result = re.sub("[^0-9 . - ]","", result)
		oldRange = result
		return result
	else:
		# Speed data was returned so just return old range value
		return oldRange

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
