import smbus
import time


class Temp:

    def __init__(self, bus_id, temp_address):
        self.bus_id = bus_id
        self.temp_address = temp_address
        self.bus = smbus.SMBus(self.bus_id)

    @staticmethod
    def __twos_complement_to_dec16(raw_value):
        if raw_value >= 0x8000:
            return -((65535 - raw_value) + 1)
        else:
            return raw_value

    def get_temperature_raw(self):
        register = 0x20  # OUT_TEMP_L
        raw_data = self.bus.read_word_data(self.temp_address, register)
        return self.__twos_complement_to_dec16(raw_data) - 25*16

    def get_temperature(self):
        register = 0x20  # OUT_TEMP_L
        raw_data = self.bus.read_word_data(self.temp_address, register)
        return (self.__twos_complement_to_dec16(raw_data) - 25*16)/16.0

    def is_tda(self):
        register = 0x1E  # STATUS_REG
        mask = '00000100'
        raw_data = self.bus.read_byte_data(self.gyro_address, register)
        return (raw_data & int(mask, 2)) != 0

if __name__ == "__main__":
    buss_id = 2
    address = 0x6b

    t = Temp(buss_id, address)

    try:
        while 1:
            print("Temperature: {0}".format(t.get_temperature()))
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass