# Bang bang controller implementation

## C library
The C library is created by the Makefile on the Raspberry Pi target by just typing make.  
The code is in bangbang.c and it has one public function called by the Python code and two private functions used internally.  

## Python script
The Python script was modified to load the bangbang.so library and to call the calculate_speed_angle() function.

## Symbolic links
The Python script needs to have equivalent symbolic links like the script in the example folder pointing to the Python libraries from SunFounder.  
Use the following syntax in order to create the two symbolic links:  
**ln -s /path_to_folder/folder/ local_name**

