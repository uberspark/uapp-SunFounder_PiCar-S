# Performance Results Document
The tests are performed with Performance_Test.py script.  
The script reads through Python a value from the line following sensor.  
It also reads the same vaue thorugh the C library.  

# Results

### 1. round-trip time for line-following sensor reading from app to sensor driver and back with normal python code and regular I2C driver

0.001472602999456285 sec

### 2. round-trip time for line-following sensor reading from app to sensor driver and back with refactored controller application and I2C driver (with our C refactoring)

0.001371612000184541 sec

### 3. round-trip time for line-following sensor reading from app to sensor driver and back with refactored controller application and I2C driver with HMAC computation

0.0015384860000153822 sec

### 4. round-trip time for line-following sensor reading from app to sensor driver and back with refactored controller application and I2C driver with HMAC computations with micro-hypervisor running underneath

0.0014791569999488274

### 5. number of sensor reads per second for steps 1, 2, 3 and 4

#### 5.1
     679 reads per second
#### 5.2
     729 reads per second
#### 5.3
     649 reads per second
#### 5.4
     676 reads per second



