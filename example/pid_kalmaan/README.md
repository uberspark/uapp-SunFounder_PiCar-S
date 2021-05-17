# PID Control Algorithm with Line Position Estimation
This is a work in progress and is currently implemented in python. Later the error computing functions that use kalman filter will be shifted to uberObject friendly C code base and a shred library will be generated. The PID shared library can be used once the error is computed using line position estimation.

## Usage
- python3 pid_line_follower.py will execute the standalone python file.
- 'def scale(value, index, min_scale=14, max_scale=45)' functions scales th input sensor readings between min_scale and max_scale. The actual sensor min and sensor max are hardcode in a form of a list in the function. Depending on the surface, user may need to update these values.
- Note: the calibrate functionanilty can be modified to print sensorwise min and max values.

## Limitations
- Settling time for discontinous and sudden changes in the position of the line allows the car to leave the line.
- To accomodate this, the linear velocity has been reduced to allow low response times to work with line following applications.
- Tweaks in the algorithm and PID tuning will be needed to make it work perfectly.

### Detailed algorithm can be found in the report