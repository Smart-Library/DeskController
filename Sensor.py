import pigpio
import time

class Sensor:
    MAX_RETRIES = 5

    def __init__(self, bus, address, start_command):
        self.__bus = bus
        self.__address = address
        self.__start_command = start_command

        print("Attempting to connect to Raspberry Pi GPIO...")
        self.__piGPIO = pigpio.pi('pi3.local')  # Connect remotely to pi GPIO

        if not self.__piGPIO.connected:
            print("Failed to connect to pi GPIO daemon")
            exit(-1)

        print("Successfully Connected!\n")

        self.__piGPIOver = self.__piGPIO.get_pigpio_version()
        time.sleep(0.1)  # Wait

        self.__retries = 0
        self.__result = 0

        for i in range(0, self.MAX_RETRIES):
            time.sleep(0.05)  # Wait a short time
            self.__handle = self.open_connection()
            if self.__handle > 0:
                self.__result = self.__piGPIO.i2c_write_device(self.__handle, [self.__start_command])
                break
            else:
                print('\n***** I2C initialization error ***** class=' + self.__class__.__name__ + 'handle=' + str(self.__handle) + ' retries=' + str(self.__retries))
                self.__retries += 1

    def open_connection(self):
        return self.__piGPIO.i2c_open(self.__bus, self.__address) # open I2C device with respective bus and address

    def close_connection(self):
        return self.__piGPIO.i2c_close(self.__handle)

    def read_raw_data(self):
        return self.__piGPIO.i2c_read_device(self.__handle, self.buffer_length())

    def buffer_length(self):
        raise NotImplementedError('This method must be implemented in the subclasses')

    def occupied_status(self):
        raise NotImplementedError('This method must be implemented in the subclasses')
