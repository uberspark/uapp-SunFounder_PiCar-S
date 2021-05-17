from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import picar
import time
import numpy as np

BASE_SPEED = 75
BASE_ANGLE = 90
ANGLE_OFFSET = 15
THRESHOLD = 25
WEIGHTS = [-4, -2, 0, 2, 4]
current_angle = 0

Kp = 5 
Ki = 0
Kd = 0


picar.setup()
lf = Line_Follower.Line_Follower()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

def init():
	bw.stop()
	fw.turn_straight()
	current_angle = 90
	mpu.configure()

def stop():
	bw.stop()
	fw.turn_straight()
	current_angle = 90

def get_sensor_readings():
	analog = lf.read_analog()
	digital = []
	#print(analog)
	for value in analog:
		if value < THRESHOLD: digital.append(1)
		else: digital.append(0)
	return digital

def get_error(digital):
	error = 0
	count = 0
	for index, value in enumerate(digital):
		if value == 1:
			error += WEIGHTS[index]
			count += 1

	if count == 0: return 0 # None
	return error / count

def clip(val, min=-20, max=20):
	if val < min: val = min
	if val > max: val = max
	return val

def get_accl():
	return mpu.readAccelerometerMaster()

def get_gyro():
	return mpu.readGyroscopeMaster()

def get_angles(dt, rpy, alpha=0.04):
	accel = get_accl()
	gyro = get_gyro()
	rpy[0] = (1-alpha) * (rpy[0] + gyro[0] * dt) + alpha* accel[0] 
	rpy[1] = (1-alpha) * (rpy[1] + gyro[1] * dt) + alpha* accel[1] 
	rpy[2] += gyro[2] * dt
	return rpy

def get_rot_matrix(dt, rpy):
	rpy = get_angles(dt, rpy)
	x_rot = np.array([[np.cos(rpy[0]), -np.sin(rpy[0]), 0], [np.sin(rpy[0]), np.cos(rpy[0]), 0],[0, 0, 1]])
	y_rot = np.array([[np.cos(rpy[1]), 0, np.sin(rpy[1])], [0, 1, 0], [-np.sin(rpy[1]), 0, np.cos(rpy[1])]])
	z_rot = np.array([[1, 0, 0], [0, np.cos(rpy[2]), -np.sin(rpy[2])], [0, np.sin(rpy[2]), np.cos(rpy[2])]])
	return x_rot @ y_rot @ z_rot, rpy

def estimate_velocity(dt, rpy, vel):
	rot_mat, rpy = get_rot_matrix(dt, rpy)
	rot_inv = np.linalg.inv(rot_mat)
	sensor_accl = np.array([[rpy[0]], [rpy[1]], [rpy[2]]])
	earth_accl = rot_inv @ sensor_accl + np.array([[0], [0], [1.0]])

	vel[0] += earth_accl[0] * dt
	vel[1] += earth_accl[1] * dt
	vel[2] += earth_accl[2] * dt

	return vel

def follow_line():
	bw.speed = BASE_SPEED
	integral_error = 0
	previous_error = 0
	start_time = time.time()
	end_time = start_time

	rpy = [0, 0, 0]
	vel = [0, 0, 0]

	while True:
		sensor_reading = get_sensor_readings()
		error = get_error(sensor_reading)
		integral_error += error

		end_time = time.time()
		time_diff = end_time - start_time
		start_time = end_time

		angle = Kp*error + Ki*integral_error + Kd*(error - previous_error)*time_diff
		previous_error = error
		
		angle = clip(angle)
		if angle > 0: angle += ANGLE_OFFSET
		fw.turn(BASE_ANGLE + angle)
		vel = estimate_velocity(dt, rpy, vel)
		print(vel)


if __name__ == '__main__':
	try:
		init()
		follow_line()
	except KeyboardInterrupt:
		stop()


