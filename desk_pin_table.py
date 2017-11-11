import desk
import config_loader
from config_loader import ConfigKeys

# Load the remote simulator if we are not within the raspberry pi environment
try:
    import RPi.GPIO as GPIO
except ImportError:
    from rpi_simulator import GPIO as GPIO


'''
This class is responsible for loading the global configuration, and mapping desk objects to GPIO pins
'''


class DeskPinTable:

    # In this mapping, each entry is a tuple containing the desk id, the pin, and the respective desk object
    # The purpose of desk id in the tuple is used for easy lookup of desks
    # The pin is a mapping to the desk sensor via GPIO
    # The desk object is used for performing additional operations on the desk if necessary
    __desk_mapping = []

    # Global Configuration object
    __conf = None

    def __init__(self):
        self.__conf = config_loader.get_global_config().get_properties()
        self.__load_desk_dictionary()

        # Set board numbering mode
        # See the following for GPIO pin numbers:
        # https://www.raspberrypi.org/documentation/usage/gpio/images/a-and-b-gpio-numbers.png
        GPIO.setmode(GPIO.BCM)

        self.register_pin_events()

    '''
    Load the id, pin, desk object mapping
    '''
    def __load_desk_dictionary(self):
        # Get all desks config
        all_desks = self.__conf[ConfigKeys.DESKS_ARRAY]

        # Get info for each desk
        for d in all_desks:
            desk_id = d[ConfigKeys.DESK_ID]
            name = d[ConfigKeys.DESK_NAME]
            pin = d[ConfigKeys.DESK_SENSOR_PIN]

            # Append id, pin, desk object to map
            self.__desk_mapping.append((desk_id, pin, desk.Desk(name, desk_id)))

            # Print additional information in debug mode
            if self.__conf[ConfigKeys.DEBUG_MODE]:
                print "[ID]:", desk_id, "[Name]:", name, "[Pin]", pin

    '''
    This method is used for detecting a rising / falling edge on the GPIO pins that are in use by the sensors
    '''
    def register_pin_events(self):
        for (desk_id, pin, desk_obj) in self.__desk_mapping:
            if pin >= 0:

                # Set GPIO numbering system
                GPIO.setup(pin, GPIO.IN)

                # The following method uses rising / falling edge detection to detect an event on a pin
                # The callback that will be called when an event is raised will be desk_obj.input_received
                # So that each individual desk can handle input from its pin
                # TODO: Add some type of custom debouncing functionality, or use bouncetime = 200 below
                GPIO.add_event_detect(pin, GPIO.BOTH, lambda channel, desk_obj=desk_obj: desk_obj.input_received(channel, GPIO.input(channel)), bouncetime=50)

        return None

    '''
    Use Desk mapping to lookup a desk object given a desk ID
    '''
    def get_desk_from_id(self, id):
        for (desk_id, pin, desk_obj) in self.__desk_mapping:
            if id == desk_id:
                return desk_obj