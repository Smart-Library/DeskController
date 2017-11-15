import config_loader
from config_loader import CONFIG
import desk

# Load the remote simulator if we are not within the raspberry pi environment
try:
    import RPi.GPIO as GPIO
except ImportError:
    # Load stub module and start simulator
    from rpi_simulator import GPIO as GPIO


class DeskPinTable:
    """
    This class is responsible for mapping desk objects to GPIO pins, and registering pin events
    """

    # In this mapping, each entry is a tuple containing the desk id, the pin, and the respective desk object
    # The purpose of desk id in the tuple is used for easy lookup of desks
    # The pin is a mapping to the desk sensor via GPIO
    # The desk object is used for performing additional operations on the desk if necessary
    __desk_mapping = []

    def __init__(self):
        """
        Initialize the DeskPinTable object. Register all pin event callbacks
        """
        self.__load_desk_dictionary()

        # Set board numbering mode
        # See the following for GPIO pin numbers:
        # https://www.raspberrypi.org/documentation/usage/gpio/images/a-and-b-gpio-numbers.png
        GPIO.setmode(GPIO.BCM)

        self.__register_pin_events()

    def __load_desk_dictionary(self):
        """
        Load the config file and initialize the desk mapping object
        :return: None
        """

        # Get all desks config
        all_desks = config_loader.CONFIG.desks

        # Get info for each desk
        for d in all_desks:

            # Append id, pin, desk object to map
            self.__desk_mapping.append((d.id, d.pin, desk.Desk(d.name, d.id)))

            # Print additional information in debug mode
            if CONFIG.debug_config.enabled:
                print("Added Desk to DeskPinTable: [ID]:", d.id, "[Name]:", d.name, "[Pin]:", d.pin)

    def __register_pin_events(self):
        """
        This method is used for detecting a rising / falling edge on the GPIO pins that are in use by the sensors
        :return: None
        """

        for (desk_id, pin, desk_obj) in self.__desk_mapping:
            if pin >= 0:

                # Set GPIO numbering system
                GPIO.setup(pin, GPIO.IN)

                # The following method uses rising / falling edge detection to detect an event on a pin
                # The callback that will be called when an event is raised will be desk_obj.input_received
                # So that each individual desk can handle input from its pin
                # TODO: Add some type of custom debouncing functionality, or use bouncetime = 200 below
                GPIO.add_event_detect(pin, GPIO.BOTH, lambda channel, desk_obj=desk_obj: desk_obj.input_received(channel, GPIO.input(channel)), bouncetime=50)

    def get_desk_from_id(self, desk_id):
        """
        Lookup a Desk Object given it's ID
        :param desk_id: The Desk ID to look for
        :return: The Desk object if the ID corresponds to a Desk, or None
        """
        t = filter(lambda info: desk_id == info[0], self.__desk_mapping)

        for (d_id, pin, d_obj) in t:
            return d_obj

    def get_pin_from_id(self, desk_id):
        """
        Lookup a Desk Pin given it's ID
        :param desk_id: The Desk ID to look for
        :return: The Desk Pin if the ID corresponds to a Desk, or None
        """
        t = filter(lambda info: desk_id == info[0], self.__desk_mapping)

        for (d_id, pin, d_obj) in t:
            return pin
