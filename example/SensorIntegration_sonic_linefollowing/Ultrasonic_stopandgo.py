from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance

from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import time
import picar

picar.setup()

REFERENCES = [200, 200, 200, 200, 200]
# calibrate = True
calibrate = False
forward_speed = 40
backward_speed = 40
turning_angle = 40

max_off_track_count = 40

delay = 0.0005
force_turning = 0    # 0 = random direction, 1 = force left, 2 = force right, 3 = orderdly

back_distance = 10
turn_distance = 20
slow_distance = 40
slower_distance = 30

timeout = 10
last_angle = 90
last_dir = 0

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()

lf.references = REFERENCES
fw.ready()
bw.ready()
fw.turning_max = 45

# collect data of distance and speed
f1 = 'distant0.txt'
f2 = 'speed.txt'
with open(f1, 'a') as file:
    file.write('time distance\n')
with open(f2, 'a') as file:
    file.write('time speed\n')


def straight_run():
        while True:
                bw.speed = 70
                bw.forward()
                fw.turn_straight()


def setup():
        if calibrate:
                cali()


def main():
        global turning_angle
        global forward_speed
        off_track_count = 0
        bw.speed = forward_speed

        a_step = 3
        b_step = 10
        c_step = 30
        d_step = 45
        bw.forward()
        while True:
                lt_status_now = lf.read_digital()
                print(lt_status_now)
                # decting obstacle
                distance = ua.get_distance()
                if distance > 0: 
                        
                        start = time.time()
                        with open(f1,'a') as file:
                            file.write(str(start) + ' ' + str(distance) + '\n')
                            print(str(distance) + 'cm')
                        with open(f2,'a') as file:
                            file.write(str(start) + ' ' + str(forward_speed) + '\n')
                        count = 0
                        if distance < turn_distance: # wait for the removal of object
                                bw.stop()
                                time.sleep(1)
                        else:
                                # print('Line following')
                                if slower_distance < distance < slow_distance:
                                    bw.forward()
                                    forward_speed = 32
                                    bw.speed = forward_speed
                                elif turn_distance <= distance <= slower_distance:
                                    bw.forward()
                                    forward_speed = 25
                                    bw.speed = forward_speed
                                else: 
                                    bw.forward()
                                    forward_speed = 40
                                    bw.speed = forward_speed
                                # print('Line following')
                                # Angle calculate
                                if lt_status_now == [0, 0, 1, 0, 0]:
                                        step = 0
                                elif lt_status_now == [0, 1, 1, 0, 0] or lt_status_now == [0, 0, 1, 1, 0]:
                                        step = a_step
                                elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
                                        step = b_step
                                elif lt_status_now == [1, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 1]:
                                        step = c_step
                                elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
                                        step = d_step

                                # Direction calculate
                                if lt_status_now == [0, 0, 1, 0, 0]:
                                        off_track_count = 0
                                        fw.turn(90)
                                # turn right
                                elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
                                        off_track_count = 0
                                        turning_angle = int(90 - step)
                                # turn left
                                elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
                                        off_track_count = 0
                                        turning_angle = int(90 + step)
                                elif lt_status_now == [0, 0, 0, 0, 0]:
                                        off_track_count += 1
                                        if off_track_count > max_off_track_count:
                                                # tmp_angle = -(turning_angle - 90) + 90
                                                tmp_angle = (turning_angle - 90) / abs(90 - turning_angle)
                                                tmp_angle *= fw.turning_max
                                                bw.speed = backward_speed
                                                bw.backward()
                                                fw.turn(tmp_angle)

                                                lf.wait_tile_center()
                                                bw.stop()

                                                fw.turn(turning_angle)
                                                time.sleep(0.2)
                                                bw.speed = forward_speed
                                                bw.forward()
                                                time.sleep(0.2)
                                else:
                                        off_track_count = 0
                        # print("distance: %scm" % distance)
                else:                                           # forward
                        fw.turn_straight()
                        if count > timeout:  # timeout, stop;
                                bw.stop()
                        else:
                                bw.backward()
                                bw.speed = forward_speed
                                count += 1
                fw.turn(turning_angle)
                time.sleep(delay)


def destroy():
        bw.stop()
        fw.turn(90)


def stop():
        bw.stop()
        fw.turn_straight()

if __name__ == '__main__':
        try:
                try:
                        while True:
                                setup()
                                main()
                # straight_run()
                except Exception as e:
                        print(e)
                        print('error try again in 5')
                        destroy()
                        time.sleep(5)
        except KeyboardInterrupt:
                destroy()
