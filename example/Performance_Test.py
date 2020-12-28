# ctypes_test.py
import ctypes
import pathlib
import os 
from SunFounder_Line_Follower import Line_Follower
import time
from timeit import Timer 

if __name__ == "__main__":
    print("Performance Test Application Running")
    def f():
       return 1
    lf = Line_Follower.Line_Follower()
    print("Call Python i2c read_digital()")
    t = Timer(lambda: lf.read_digital())
    print(t.timeit(number=1))
    # Load the shared library into ctypes
    print("Load the C shared library")
    libname = os.path.abspath(".") + "/../../uobjcoll-SunFounder_Line_Follower/" + "libLine_Follower.so";
    print(libname)
    c_lib = ctypes.CDLL(libname)
    print("Call C library i2c read_digital()")
    t = Timer(lambda: c_lib.read_digital())
    print(t.timeit(number=1))
