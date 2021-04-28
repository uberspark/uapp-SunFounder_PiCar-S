
from SunFounder_Line_Follower import Line_Follower
import picar
import time
import sys, getopt

if __name__ == '__main__':
	argv = sys.argv[1:]
	cal_time = 0
	try:
		opts, args = getopt.getopt(argv,"t:",["calibration_time="])
	except getopt.GetoptError:
		print ('calibrate.py -t <calibration_time>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-t", "--calibration_time"):
			cal_time = float(arg)

	picar.setup()
	lowest = 1024
	highest = 0
	start_time = time.time()

	while((float)(time.time() - start_time) < cal_time):
		lf = Line_Follower.Line_Follower()
		sensor_data = lf.read_analog()
		this_min = min(sensor_data)
		this_max = max(sensor_data)

		lowest = min(lowest, this_min)
		highest = max(highest, this_max)

	print("Threshold: " + str((highest - lowest) / 2))
