#!/usr/bin/env python
'''
**********************************************************************
* Filename    : bangbang_line_follower.py
* Description : An example for sensor car kit to follow line
* Author      : Dream
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Dream    2016-09-21    New release
**********************************************************************
'''

from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import time
import picar
import ctypes
import pathlib
import sys
import os
import numpy


# This is the beginning of the script
# Initialize the access to the C library
banglibname = os.path.abspath(".") + "/" + "libbangbang.so"
bang_lib = ctypes.CDLL(banglibname)
bang_lib.calculate_angle_speed.argtypes = [ ctypes.c_int, ctypes.c_int, ctypes.c_int]

picar.setup()
rslt = bang_lib.lib_init()
if rslt == -1:
	print("lib_init() failed")
	exit()

REFERENCES = [200, 200, 200, 200, 200]
forward_speed = 90
backward_speed = 70
turning_angle = 40
current_angle = 0
off_track_count = 0
step=0
a_step = 2
b_step = 8
c_step = 24
d_step = 40

max_off_track_count = 40

delay = 0.0005

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()
lf.references = REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45


def main():
	global turning_angle

	bw.speed = forward_speed
	bw.forward()
	lt_status_now = []
	step = 0
	start_time_ms = time.time() * 1000
	while True:
        ### clib call
		lt_status_now = []
		dt_list = bang_lib.read_digital()
		ptr = ctypes.cast(dt_list,ctypes.POINTER(ctypes.c_int))
		for i in range(0,5):
			lt_status_now.append(ptr[i])
		#diff_ms = (time.time() * 1000) - start_time_ms
		#print(str(lt_status_now)[1:-1] + ", " + str(diff_ms))
		off_track_count = 0
		if lt_status_now == [0,0,0,0,0]:
			off_track_count += 1
			if off_track_count > max_off_track_count:
				tmp_angle = (turning_angle-90)/abs(90-turning_angle)
				tmp_angle *= fw.turning_max
				bw.speed = backward_speed
				bw.backward()
				fw.wheel.write(tmp_angle)
				current_angle = tmp_angle

				### clib call
				bang_lib.wait_tile_center()
				bw.stop()

				fw.wheel.write(turning_angle)
				current_angle = turning_angle
				time.sleep(0.2)
				bw.speed = forward_speed
				bw.forward()
				time.sleep(0.2)
			else:
				off_track_count = 0
		else:
			bang_list = bang_lib.calculate_angle_speed(forward_speed,turning_angle,step)
			ptr = ctypes.cast(bang_list,ctypes.POINTER(ctypes.c_int))
			bw.speed = ptr[5]
			step = ptr[6]
			turning_angle = ptr[7]

		fw.wheel.write(turning_angle)
		current_angle = turning_angle
		time.sleep(delay)

def destroy():
	bw.stop()
	fw.turn(90)
	rslt = bang_lib.lib_exit()
	if rslt == -1:
		print("lib_exit() failed")

if __name__ == '__main__':
	try:
		while True:
			main()
	except KeyboardInterrupt:
		destroy()
