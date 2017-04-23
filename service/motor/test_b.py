#!/usr/bin/python3
from motor import Motor
import time

if __name__ == "__main__":

    speed = -15

    m0 = Motor(0)
    m1 = Motor(1,-1)

    try:
        while 1:
            print(m0.get_position(), m1.get_position())
            time.sleep(0.25)
            m0.set_velocity(speed)
            m1.set_velocity(speed)

    except KeyboardInterrupt:
        m0.close()
        m1.close()