from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import picar
import time
import math

BASE_SPEED = 60
BASE_ANGLE = 90
ANGLE_OFFSET = 15


Kp = 7
Ki = 0.1
Kd = 1

picar.setup()
lf = Line_Follower.Line_Follower()
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

def init():
	bw.stop()
	fw.turn_straight()
	current_angle = 90

def stop():
	bw.stop()
	fw.turn_straight()
	current_angle = 90

# Scale sensor ouput to min_scale and max_scale
def scale(value, index, min_scale=14, max_scale=45):
	old_min = [8, 10, 12, 12, 12] # minimum values for each sensor
	old_max = [34, 37, 41, 37, 39] # maximum values for each sensor

	new_value = ((value - old_min[index]) / (old_max[index] - old_min[index])) * (max_scale - min_scale) + min_scale
	return new_value

def get_sensor_readings():
	analog = lf.read_analog()
	for i in range(0, len(analog)):
		analog[i] = scale(analog[i], i)
	return analog

# Get line estimate from polynomial interpolation 
# Computes line distance from one sensor
def get_line_distance(x):
	poly_array =   [6.2505e-04, 0.0282, -0.1471]
	if (x < 14): return 0
	elif (x < 19): return (x - 14) / 10
	elif (x > 45): return 2.6

	else:
		degree = len(poly_array)
		y = 0
		for i in range(1, degree+1):
			y = y + poly_array[i-1] * pow(x, degree - i)
		return y

# Combine all line distances to get a position estimate
def get_position(sensor_array, threshold=2.5):
	min_pos = sensor_array.index(min(sensor_array))
	dist_arr = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
	threshold = 35

	distance = get_line_distance(sensor_array[min_pos])
	sensor_distance = dist_arr[min_pos]
	final_dist = 0

	if (min_pos == 0 and sensor_array[1] < threshold): final_dist = sensor_distance + distance
	else: final_dist = sensor_distance

	if(min_pos == 1 and sensor_array[2] < sensor_array[0]): final_dist = sensor_distance + distance
	else: final_dist = sensor_distance

	if(min_pos == 2 and sensor_array[3] < sensor_array[1]): final_dist = sensor_distance + distance
	else: final_dist = sensor_distance

	if(min_pos == 3 and sensor_array[4] < sensor_array[2]): final_dist = sensor_distance + distance
	else: final_dist = sensor_distance

	if(min_pos == 4 and sensor_array[3] > threshold): final_dist = sensor_distance + distance
	else: final_dist = sensor_distance

	return final_dist

	'''
	prediction_arr = [0, 0, 0, 0, 0, 0]
	dist_arr = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
	#distances = [2.3, 1.2, 0.2, -0.7, -1.8]
	#print(sensor_array)

	for number, reading in enumerate(sensor_array):
		distance = get_line_distance(reading)
		#print(number, distance)
		#distance = distances[number]

		if distance <= threshold:
			pos_index = math.ceil(max(0, min(5, number + distance)))
			neg_index = math.ceil(min(5, max(0, number - distance)))
			prediction_arr[int(pos_index)] += 1
			prediction_arr[int(neg_index)] += 1
	pos =  prediction_arr.index(max(prediction_arr))
	#print(prediction_arr)

	final_dist = dist_arr[pos]
	count = 0
	final = 0
	for number, reading in enumerate(sensor_array):
		distance = get_line_distance(reading)
		#distance = distances[number]

		if (distance <= threshold):
			pos_candidate = abs((number - 2 + distance) - final_dist)
			neg_candidate = abs((number - 2 - distance)  - final_dist)
			#print(pos_candidate, neg_candidate)
			final += min(pos_candidate, neg_candidate)
			count += 1

	if count == 0: return 0
	final = final / count
	#print(final_dist - final)
	#print(final)
	return final
	'''
def clip(val, min=-20, max=20):
	if val < min: val = min
	if val > max: val = max
	return val

def compute_kalmaan_gain(estimate_err, measure_error=1):
	return estimate_err / (estimate_err + measure_error)

def compute_kalmaan_estimate(estimate_prev, meaure_current, gain):
	return estimate_prev + gain * (meaure_current - estimate_prev)

def compute_kalmaan_estimate_error(estimate_err_prev, gain):
	return (1 - gain) * estimate_err_prev

def follow_line():
	bw.speed = BASE_SPEED
	integral_error = 0
	previous_error = 0
	start_time = time.time()
	end_time = start_time
	estimate_err = 0.5
	estimate_prev = 0
	time_diff = 0
	actual_start = time.time()

	while True:
		sensor_reading = get_sensor_readings()
		error = get_position(sensor_reading)
		gain = compute_kalmaan_gain(estimate_err)
		estimate_prev = compute_kalmaan_estimate(estimate_prev, error, gain)
		estimate_err = compute_kalmaan_estimate_error(estimate_err, gain)
		error = estimate_prev

		integral_error += error

		end_time = time.time()
		time_diff = end_time - start_time
		start_time = end_time

		angle = Kp*error + Ki*integral_error + Kd*(error - previous_error)*time_diff
		previous_error = error
		
		angle = clip(angle)
		if angle > 0: angle += ANGLE_OFFSET
		print(angle, round(time.time() - actual_start, 3), 0, 0)
		fw.turn(BASE_ANGLE + angle)



if __name__ == '__main__':
	try:
		init()
		follow_line()
	except KeyboardInterrupt:
		stop()


