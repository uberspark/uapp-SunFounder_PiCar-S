# Sensor integration of Ultrasonic sensor and line following

## Usage
- Copy the script in the /examples folder
- Execute the python script
- ```
- python3 Ultrasonic_stopandgo.py
- ```
- Before running the code, make sure calibarating the line following unit
- Running the code will generate two text file where distant0.txt collect the data
- I predefined the speed and threshold in the code which should be replaced with dynamic implementations in the future

## Limitations
- The ultrasonic sensor is only reliable detecting object within the range around 75cm, within a roughly angle of 25 degrees
