#!/usr/local/bin/python
##!/usr/bin/python
# #!/usr/bin/env python2.6
##############################################################################
#  spui.py
#  
#
#  Created by Jeffrey Evans on 8/3/12.
#  Copyright (c) 2012 Purdue University. All rights reserved.
#
# A Simple Python User Interface
#
# Written for Python 2.x, NOT Python 3
#
##############################################################################

# imports are here
import sys
import serial
import optparse
import datetime

# Functions here
##############################################################################
## Menu Display function
#
# Function displays the menu to user, then tests user input for validity
#
  
def displayMenu(menu):
  for item in menu:
    print '%s' % item

  selection = raw_input('Select a menu item: ')
  return (selection)
##############################################################################

##############################################################################
## Put String to Serial Port
#
# Function sends character string to serial port
#

  
def puts(s):
  for c in list(str(s)):
    ser.write(c)
##############################################################################

##############################################################################
## Process User Selection
#
# Function processes user selection
# Selection can be any single character, allowing for easy expansion
#
  
def processSelection(s):
  text = ''
  # D = D for display message
  if s == 'D':
    print "Sending Display a message command\t"
    ser.write('D')
    text = ser.read(1)
    print "Received %s from target, waiting for message.\n" % text
    msg = ser.readline()
    if msg == "s\n":
      print "Target is stopped! Cannot send message, put target in RUN state and try again\n"
    else:
      print '%s' % msg

  # S = Stop - Red LED should turn off and amber should flash at slower rate
  elif s == 'S':
    print "Sending Stop command\t" 
    ser.write('S')
    text = ser.read(1)
    print "Received %s from target\n" % text

  # R - Restart - Amber LED should turn off and red should restart	
  elif s == 'R':
    print "Sending Restart Command\t"
    ser.write('R')
    text = ser.read(1)
    print "Received %s from target\n" % text

  # Q - quit - exit the program on each side	
  elif s == 'Q':
    print "Sending Quit Command\t"
    ser.write('Q')
    text = ser.read(1)
    print "Received %s from target\n" % text
    return 1

  # selection not valid - 
  else:
    print "\nInvalid selection %s, try again.\n" % s
    #return displayMenu(menu)

  ser.flush()
  return 0
#processSelection(displayMenu(menu))

##############################################################################

p = optparse.OptionParser()

##############################################################################
## add options here
# port identifier for the PC host
p.add_option("-p", "--port ", 
             action="store",
             type="string",
             dest="port", 
             help="port: COM1, name (/dev/tty.usbserial-A20e1mk3)",
             metavar=" PORT")

# rate for the port in bps (9600, 19200, etc)
p.add_option("-r", "--rate ", 
             action="store",
             type="int",
             dest="rate", 
             help="bit rate in bps (19200)",
             metavar=" RATE")

# a timeout value (default usually works (10)
p.add_option("-t", "--timeout ", 
             action="store",
             type="int", dest="timeout", 
             help="Timeout in seconds (10)",
             metavar=" TIMEOUT")

# a log file 
p.add_option("-f", "--file ", 
             action="store",
             type="string",
             dest="logfile", 
             help="logfile name FILE",
             metavar=" FILE")

# verbose setting
p.add_option("-v", "--verbose", 
             action="store_false",
             dest="verbose", 
             help="verbose mode",
             metavar="VERBOSE")

# set up default values
p.set_defaults(port="COM3", 
               rate=9600,
               timeout=10,
               logfile="NULL",
               verbose=0) 

##############################################################################
## print a banner, then config options, allow for bail out before continuing
# setup a menu print it out, then take input from the keyboard (raw-input) 
# and send it over the serial port
# Main
if __name__ == '__main__':

  print __doc__
  print "Simple Python User Interface (SPUI)... parsing options...\n"

  opt, args = p.parse_args()

  print "port   : ", opt.port
  print "rate   : ", opt.rate
  print "timeout: ", opt.timeout
  print "file   : ", opt.logfile
  print "verbose: ", opt.verbose


  # provide a bailout to the user
  bail = raw_input("\nThese are your settings, continue (y/n): ")
  if bail == "n" or bail == "N":
    print "You pressed %s, quitting..." % bail
    sys.exit()
  else:
    print "You pressed %s, continuing..." % bail
    if opt.logfile != "NULL":
        f = open(opt.logfile, "w+")

  print __doc__
  print "\tOpening serial port...."

  # Open Serial port, verify, flush, restart, then test
  try:
    # This is a more robust way to open, but sometimes confuses ceratin machines
    #ser = serial.Serial(port=opt.port, baudrate=opt.rate, 
    #                xonxoff=0, rtscts=1, timeout=opt.timeout)
    ser = serial.Serial(port=opt.port, baudrate=opt.rate, timeout=opt.timeout)
    
    #try:
    #ser.open()
    if ser.isOpen():
        # Flush inputs and outputs
        ser.flushInput()   
        ser.flushOutput() 
        # Invoke restart - an LED should be flashing @ 1Hz
        ser.write('r') 
        # Test for echo, if the echo worked, it will return an 'r'
        text = ser.read(1)
        if (text == "r"):
            print "Target echoed properly, life is good."
        else:
            print "Communication problem, target did not echo properly."

  #except serial.SerialException, e:
  except serial.SerialException:
    print "Failed to open serial port %s: " % (ser.name)
    print "Check Connections, restart target device and try again."
    sys.exit()


# Need to enumerate the menu outside of the display menu function
  menu = ['[D]isplay a message','[S]top', '[R]estart','[Q]uit']

##############################################################################
## when here the code calls display menu then processes selection,
# looking for "done" flag when the "quit" item is selected, after which
# we clean up and exit  
  done = 0
  while done == 0:
      cmd = displayMenu(menu)
      done = processSelection(cmd)
      if opt.logfile != "NULL":
        now = datetime.datetime.now()
        t = now.ctime()
        f.write("%s,\t%s,\t%1d\n" % (t,cmd,done))
 
# file and serial port cleanup
  if opt.logfile != "NULL":
    f.close()
  ser.flushInput()
  ser.flushOutput()
  ser.close()
  print "Goodbye."

  print "Exiting Normally"
  sys.exit(0)

else:
  print "Nothing to do, but quit"
  sys.exit(0)
  
# end of file
