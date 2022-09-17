# Author: Raf, Sako

# Imports
import serial
import re
import rospy
from std_msgs.msg import Int32
import radarCommands

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

def main ():
	print("--OPS243 Radar--")
	print("Initializing serial: ", port, " @ ", baud)

	readSpeed()
	readRange()

	# After verifying above works
	
	#speed = readSpeed()
	#range = readRange()
	
	# After verifying above works
	
	# Add ros

	#pubSpeed = rospy.Publisher('radarSpeed', Int32, queue_size = 10)
	#pubRange = rospy.Publisher('radarRange', Int32, queue_size = 10)
	#rospy.init_node('radar', anonymous = True)
	#rate = rospy.Rate(freq)
	#while not rospy.is_shutdown():
		#currSpeed = readSpeed()
		#currRange = readRange()
		
		#rospy.loginfo(currSpeed)
		#pubSpeed.publish(currSpeed)
		
		#rospy.loginfo(currRange)
		#pubRange.publish(currRange)	

def readSer ():
	radarRead = ser.readline()
	radarReadStr = str(radarRead.decode("utf-8"))
	if (len(radarRead) != 0):
		result = re.sub("[^0-9 . - ]"," ", radarReadStr)
	return result

def readSpeed ():
	send_serial_cmd(range_off)
	send_serial_cmd(speed_on1)
	send_serial_cmd(speed_units)
	send_serial_cmd(speed_limit)
	
	result = readSer()
	print("Speed", result)
	#return result

def readRange ():
	send_serial_cmd(speed_off)
	send_serial_cmd(range_on1)
	send_serial_cmd(range_units)
	send_serial_cmd(range_limit)
	
	result = readSer()
	print("Range", result)
	#return result

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
