#!/usr/bin/env python

# Simple demo of reading color data with the TCS34725 sensor.
# Will read the color from the sensor and print it out along with lux and
# color temperature.
# Author: Tony DiCola
# License: Public Domain
#
import time

# Import the TCS34725 module.
# Install TCS34725 module from https://github.com/adafruit/Adafruit_Python_TCS34725
import Adafruit_TCS34725

import rospy
from rgbsensor.msg import rgbdata
from geometry_msgs.msg import PoseStamped

# Create a TCS34725 instance with default integration time (2.4ms) and gain (4x).
import smbus
	
# tcs = Adafruit_TCS34725.TCS34725()
f= open("rgbc_record.txt","w+")

def vrpnDataObserver(vrpnData):

	xpos = vrpnData.pose.position.x
	ypos = vrpnData.pose.position.y

	# Read the R, G, B, C color data.
	r, g, b, c = tcs.get_raw_data()
	#r = 0
	#g = 0
	#b = 0
	#c = 0
	#color_temp = 0
	#lux = 0

	# Calculate color temperature using utility functions.  You might also want to
	# check out the colormath library for much more complete/accurate color functions.
	color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)

	# Calculate lux with another utility function.
	lux = Adafruit_TCS34725.calculate_lux(r, g, b)

	# Print out the values.
	print('Color: red={0} green={1} blue={2} clear={3}'.format(r, g, b, c))

	# Print out color temperature.
	if color_temp is None:
    		print('Too dark to determine color temperature!')
		color_temp = -1
	else:
    		print('Color Temperature: {0} K'.format(color_temp))

	# Print out the lux.
	print('Luminosity: {0} lux'.format(lux))

	f.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\r\n" % (r,g,b,c,color_temp,lux,xpos,ypos))



# Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
tcs.set_interrupt(False)

rospy.init_node('rgbsensor')

vrpnSub = rospy.Subscriber('/vrpn_client_node/tb0/pose', PoseStamped, vrpnDataObserver);

rospy.spin()

f.close()
# Enable interrupts and put the chip back to low power sleep/disabled.
tcs.set_interrupt(True)
tcs.disable()
