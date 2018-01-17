from time import sleep
import pigpio

class Sensor:
    MAX_RETRIES = 5

    def __init__(self, bus, address, start_command, buffer_length):
        self.__bus = bus
        self.__address = address
        self.__start_command = start_command
        self.__buffer_length = buffer_length

        print("Attempting to connect to Raspberry Pi GPIO...")
        self.__piGPIO = pigpio.pi()  # Connect locally to pi GPIO

        if not self.__piGPIO.connected:
            print("Failed to connect to pi GPIO daemon")
            exit(-1)

        print("Successfully Connected!\n")

        sleep(0.1)  # Wait

        self.__retries = 0
        self.__result = 0

        for i in range(0, self.MAX_RETRIES):
            sleep(0.05)  # Wait a short time
            self.__handle = self.open_connection()
            if self.__handle > 0:
                self.__result = self.write_raw_data(self.__handle, [self.__start_command])
                break
            else:
                print('\n***** I2C initialization error ***** class=' + self.__class__.__name__ + 'handle=' + str(self.__handle) + ' retries=' + str(self.__retries))
                self.__retries += 1

    @property
    def occupied_status(self):
        """
        Method responsible for returning the result of the subclass own determination of the 
        desk's occupied status

        :return: Boolean value of the occupied status of each desk
        """
        raise NotImplementedError('This method must be implemented in the subclasses')

    def open_connection(self):
        return self.__piGPIO.i2c_open(self.__bus, self.__address) # open I2C device with respective bus and address

    def close_connection(self):
        return self.__piGPIO.i2c_close(self.__handle)

    def read_raw_data(self):
        return self.__piGPIO.i2c_read_device(self.__handle, self.__buffer_length)

    def write_raw_data(self, handle, start_command):
        return self.__piGPIO.i2c_write_device(self.__handle, [start_command])


