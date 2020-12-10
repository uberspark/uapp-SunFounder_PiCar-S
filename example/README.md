# Line Follower Modification for Using a C Module 

## Overview:
This is an extension of the SunFounder_Picar-S repository with some additional files added.


## Main Files added to the original code :
#### line_follower_clib.py <br/>
#### config <br/>

## Preparation of the software on the Raspberry Pi

#### sudo apt-get install python3-smbus
#### sudo apt-get install python-rpi.gpio python3-rpi.gpio
#### sudo apt-get install python-setuptools

#### git clone --recursive https://github.com/sunfounder/SunFounder_Line_Follower
#### git clone --recursive https://github.com/uberspark/uapp-SunFounder_PiCar-S
#### git clone https://github.com/uberspark/uobjcoll-SunFounder_Line_Follower
#### cd ~/SunFounder_PiCar-S
#### sudo .install_dependencies
#### cd cd uobjcoll-SunFounder_Line_Follower/
#### git checkout uobjcoll
#### make
#### cd ~/cd uapp-SunFounder_PiCar-S/example
#### git checkout uobjcoll

## Enable i2c for the line following sensor
#### raspi-config
#### Go to Advanced Options - Enable i2c
#### Save changes

## Check that address 0x11 is read. This is the line following card with the i2c sensor:

### i2cdetect -y 1  
0 1 2 3 4 5 6 7 8 9 a b c d e f  
00: – -- – -- – -- – -- – -- – -- – -- – --  
10: – 11 – -- – -- – -- – -- – -- – -- – --  
20: – -- – -- – -- – -- – -- – -- – -- – --  
30: – -- – -- – -- – -- – -- – -- – -- – --  
40: 40 – -- – -- – -- – 48 – -- – -- – -- –  
50: – -- – -- – -- – -- – -- – -- – -- – --  
60: – -- – -- – -- – -- – -- – -- – -- – --  
70: 70 – -- – -- – -- –  

## Line Following example  
The line followinf example can be tested by using the original script line_follower.py and line_follower_clib.py  
#### python3 line_follower.py
#### python3 line_follower_clib.py
The code in line_follower_clib.py is very similar to the original line_follower.py.  
The difference is that the line_follower_clib.py calls a C shared library in order to read from the i2c sensor  
 on the line follower module.


