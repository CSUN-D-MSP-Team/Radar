################################################################################################
#Imports
################################################################################################

#all of these libraries aside from time/ datetime came with the dev code
    #time and datetime added for time stamping 
import os
import sys
from time import *
from decimal import *
import serial
import serial.tools.list_ports 
import re
from datetime import datetime, timedelta
import datetime
import time
from platform import system 



################################################################################################
#radar setting macros
################################################################################################

#counting objects command
Ops241b_algo_call = 'N?'

#speed reporting settings
speed_units = 'uM'          #reports in m/s
inbound_only = 'R+'         #only records inbound objects speed
#sample_frequency = "SI"     #rate at which samples are taken (currently at 1k/s)
#sample_frequency = "SV"    #rate at which samples are taken (currently at 5k/s)
#sample_frequency = "SC"    #rate at which samples are taken (currently at 100k/s)
sample_frequency = "S2"    #rate at which samples are taken (currently at 20k/s)
#sample_frequency = "SX"     #rate at which samples are taken (currently at 10k/s)

#speed_limit = 'M>0'         #report values greater than 0
speed_limit = 'R>1'         #report values greater than 0 
speed_on = 'OS'
speed_off =  'Os'
speed_on1 = 'O2'

#range reporting settings
range_units = 'uM'          #reports range in units of meters
#range_limit = 'M>0'         #report range values greater than 0
range_limit = 'r>1'         #report range values greater than 0

range_on = 'OD'
range_off = 'Od'

#universal commands
module_info = '??'
baud_rate = 'I2'
#power_mode = "PA"           #normal operating mode
power_mode = 'PA' 
invalid_type = 'BZ'         #reports invalid data as a "0"
wait_between = 'WI'         #no wait between reports
range_on1  = 'o2'

object_detection = 'IG'

magnitude_on='oM'
magnitude_off='om'

################################################################################################
#initialize serial coms
################################################################################################
ser = serial.Serial(
    port = '/dev/ttyACM0',                      #assigns USB ports 
    baudrate = 19200,                           #default baud rate for radar
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1,
    writeTimeout = 2
)
ser.flushInput()
ser.flushOutput()



################################################################################################
#function definitions
################################################################################################

# filter algo
def Filter ():
     Ops241_rx_bytes = ser.readline()
   #  print(Ops241_rx_bytes)  #use this line of code to debug the incoming data 
     Ops241_rx_bytes_length = len(Ops241_rx_bytes)
     if (rmd == 0):
         units = " m/s"
         tp = "Speed:"
         
     else :
         units = " m"
         tp = "Range:"
     if (Ops241_rx_bytes_length != 0) :
            Ops241_rx_str = str(Ops241_rx_bytes.decode("utf-8"))
            
            #result = re.sub("[^0-9 . -] ","",Ops241_rx_str)
            result = re.sub("[^0-9 . - ]","  ", Ops241_rx_str)

            print(tp)
            print(result + units + "\n")
          #  print(result + "\n")
     if (rmd != 0):
         print(str(datetime.now()))
                #send_serial_cmd(Ops241b_algo_call)
                #objects = ser.readline()
                #print("\n" +  str(objects))
         print ("___________________________________")
         



# sendSerialCommand: function for sending commands to the OPS-241A module
def send_serial_cmd(command) :
    data_for_send_str = command
    data_for_send_bytes = str.encode(data_for_send_str)
    ser.write(data_for_send_bytes)
    # Initialize message verify checking
    ser_message_start = '{'
    ser_write_verify = False
    # Print out module response to command string
    while not ser_write_verify :
        data_rx_bytes = ser.readline()
        data_rx_length = len(data_rx_bytes)
        if (data_rx_length != 0) :
            data_rx_str = str(data_rx_bytes)
            if data_rx_str.find(ser_message_start) :
                ser_write_verify = True
   
################################################################################################
#main loop:
################################################################################################ 
from datetime import datetime, timedelta
import time
import re

#send_serial_cmd(object_detection)

send_serial_cmd(speed_limit)
send_serial_cmd(range_limit)

send_serial_cmd(power_mode)
send_serial_cmd(invalid_type)
send_serial_cmd(wait_between)
send_serial_cmd(sample_frequency)
send_serial_cmd(baud_rate)

#send_serial_cmd(speed_limit)

#send_serial_cmd(magnitude_on)

send_serial_cmd(speed_on1)
send_serial_cmd(range_on1)

#send_serial_cmd(speed_units)
#send_serial_cmd(range_units)


count = 1   
while 1:
        count += 1
        rmd = count % 2
        #trigger alternation based on start bit
                      
        if rmd == 0:
            send_serial_cmd(range_off)
            send_serial_cmd(speed_units)
            send_serial_cmd(speed_on)
            send_serial_cmd(speed_on1)
            #send_serial_cmd(speed_units)
            #send_serial_cmd(object_detection)
            
            send_serial_cmd(speed_limit)
            
        else:
            send_serial_cmd(speed_off)
            send_serial_cmd(range_units)
            send_serial_cmd(range_on)
            send_serial_cmd(range_on1)
           # send_serial_cmd(range_units)
            #send_serial_cmd(object_detection)
            
            send_serial_cmd(range_limit)
            
            
            
        Filter()
        #print (send_serial_cmd(Ops241b_algo_call))      
