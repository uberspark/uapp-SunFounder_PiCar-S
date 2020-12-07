# Line Follower Modification for Using a C Module 

## Overview:
This is an extension of the SunFounder_Picar-S repository with some modules added:
line_follower_clib.py 
It is necessary to create the following symbolic links so that the necessary Python modules can be found:
rwxrwxrwx 1 pi pi   29 Dec  1 17:27 picar -> ../../SunFounder_PiCar/picar/
lrwxrwxrwx 1 pi pi   58 Dec  1 16:52 SunFounder_Line_Follower -> ../../SunFounder_PiCar-S/example/SunFounder_Line_Follower/


## Main Files :
line_follower_clib.py <br/>
config <br/>

##Method of Operation
The code in line_follower_clib.py is very similar to the original line_follower.py.
The difference is that the line_follower_clib.py calls a C shared library in order to read from the i2c sensor on the line follower module.


