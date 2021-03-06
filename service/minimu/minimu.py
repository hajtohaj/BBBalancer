from gyroscope import Gyroscope
from accelerometer import Accelerometer
from fifo import Fifo
from temperature import Temperature
from time import sleep
import numpy as np
import sys


class Minimu:
    VERSION = 'minimu9v5'

    def __init__(self, buss_id, address):
        self.gyro = Gyroscope(buss_id, address)
        self.gyro_full_scale = 245
        self.acc = Accelerometer(buss_id, address)
        self.acc_full_scale = 2
        self.fifo = Fifo(buss_id, address)
        self.temp = Temperature(buss_id, address)

    def enable(self, odr=104):
        self.gyro.enable(odr)
        self.gyro_full_scale = self.gyro.get_full_scale_selection()
        self.acc.enable(odr)
        self.acc_full_scale = self.acc.get_full_scale_selection()
        self.fifo.enable(odr)

    def disable(self):
        self.gyro.disable()
        self.acc.disable()
        self.fifo.disable()

    def read_fifo_raw(self):
        data = np.array(self.fifo.get_data(), dtype=np.int)
        return data

    def read_fifo(self):
        data = np.array(self.fifo.get_data(), dtype=np.double)
        try:
            data[:, :3] *= 1
        except IndexError:
            sleep(0.1)
            data = np.array(self.fifo.get_data(), dtype=np.double)

        data[:, :3] *= self.gyro_full_scale
        data[:, -3:] *= self.acc_full_scale
        data[data > 0] /= 32767
        data[data < 0] /= 32768
        return data

    def read_temperature(self):
        return self.temp.get_temperature()

if __name__ == "__main__":
    buss_id = 2
    fifo_address = 0x6b

    np.set_printoptions(precision=3)

    mm = Minimu(buss_id, fifo_address)
    mm.enable(104)

    try:
        while 1:
            np.savetxt(sys.stdout.buffer, mm.read_fifo(), fmt='%i', delimiter='; ')
            sleep(1)

    except KeyboardInterrupt:
        mm.disable()
