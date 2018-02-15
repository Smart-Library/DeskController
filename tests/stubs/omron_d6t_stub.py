from random import Random


class PiStub:
    __TEST_HANDLE = 7357
    __test_data = [[0xff, 0x0, 0xdd, 0x0, 0xdc, 0x0, 0xe0, 0x0, 0xe6, 0x0, 0xd9, 0x0, 0xd8, 0x0, 0xdd, 0x0, 0xe2, 0x0, 0xd5, 0x0, 0xd5, 0x0, 0xd8, 0x0, 0xdc, 0x0, 0xcf, 0x0, 0xd1, 0x0, 0xd4, 0x0, 0xd5, 0x0, 0x8f],
                   [0xff, 0x0, 0x9, 0x1, 0x2c, 0x1, 0x4b, 0x1, 0x55, 0x1, 0x51, 0x1, 0x55, 0x1, 0x56, 0x1, 0x57, 0x1, 0x56, 0x1, 0x54, 0x1, 0x56, 0x1, 0x58, 0x1, 0x54, 0x1, 0x54, 0x1, 0x55, 0x1, 0x56, 0x1, 0x44]]

    def __init__(self, host='', port=''):
        print("Called stub initializer. host = " + str(host) + ", port = " + str(port))
        self.__rand = Random()


    def i2c_open(self, i2c_bus, i2c_address, i2c_flags=0):
        print(f'i2c Connection has been opened. i2c_bus = {str(i2c_bus)}, ' +
              f'i2c_address = {str(i2c_address)}, i2c_flags = {str(i2c_flags)}')
        return self.__TEST_HANDLE

    def i2c_close(self, handle):
        print(f'i2c connection has been closed. handle = {str(handle)}')
        return 0

    def i2c_write_device(self, handle, data):
        print(f'Writing to i2c connection: handle = {str(handle)}, data = {str(data)}')

    def i2c_read_device(self, handle, count):
        print(f'Reading from i2c connection: handle = {str(handle)}, count = {str(count)}')

        # Generate fake data
        return count, self.__test_data[self.__rand.randint(0, 1)]

    def get_pigpio_version(self):
        return -1
