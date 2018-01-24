from time import sleep
from config.config import CONFIG
import pigpio
from tests.stubs.omron_d6t_stub import PiStub


class Sensor:
    _MAX_RETRIES = 5
    __pi_gpio_instance = None

    def __init__(self, bus, address, start_command, buffer_length):
        self.__bus = bus
        self.__address = address
        self.__start_command = start_command
        self.__buffer_length = buffer_length

        self.__pi = Sensor.__get_pi_gpio()
        sleep(0.1)

        self.__retries = 0
        self.__result = 0

        for i in range(0, self._MAX_RETRIES):
            self.__handle = self.open_connection()
            if self.__handle > 0:
                self.__result = self.write_raw_data(self.__handle, [self.__start_command])
                break
            else:
                print('\n***** I2C initialization error ***** class=' + self.__class__.__name__ + 'handle=' + str(self.__handle) + ' retries=' + str(self.__retries))
                self.__retries += 1

                # Sleep between retries
                sleep(0.05)

    @property
    def occupied_status(self):
        """
        Method responsible for returning the result of the subclass own determination of the 
        desk's occupied status

        :return: Boolean value of the occupied status of each desk
        """
        raise NotImplementedError('This method must be implemented in the subclasses')

    def open_connection(self):
        return self.__pi.i2c_open(self.__bus, self.__address)

    def close_connection(self):
        return self.__pi.i2c_close(self.__handle)

    def read_raw_data(self):
        return self.__pi.i2c_read_device(self.__handle, self.__buffer_length)

    def write_raw_data(self, handle, start_command):
        return self.__pi.i2c_write_device(handle, start_command)

    @staticmethod
    def __get_pi_gpio():
        """
        Creates one instance of pigpio.pi() so that we are not establishing
        a connection for each sensor. We only need one connection across all sensors
        to the pi. Hence, we treat __pi.gpio.instance as a singleton instance, and
        use this method to obtain the singleton instance.

        :return: pigpio.pi instance
        """
        if Sensor.__pi_gpio_instance is None:
            print("Attempting to connect to Raspberry Pi GPIO...")
            Sensor.__pi_gpio_instance = pigpio.pi('pi3.local')

            if not Sensor.__pi_gpio_instance.connected:
                print("Failed to connect to pi GPIO daemon")
                if CONFIG.debug_config.enabled:
                    print("Using GPIO stub.")
                    Sensor.__pi_gpio_instance = PiStub('pi3.local')
                else:
                    exit(-1)

            print("Successfully Connected! (Version: " + str(Sensor.__pi_gpio_instance.get_pigpio_version()) + ")\n")

        return Sensor.__pi_gpio_instance
