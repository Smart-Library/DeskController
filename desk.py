class Desk:
    """
    This class will essentially be a model for a desk, containing desk name, id, etc.
    Note: pin information will be stored in desk_map
    """

    def __init__(self, desk_name, desk_id=-1, occupied=False):
        """
        Initialize a new desk object
        :param desk_name: Name of desk
        :param desk_id: ID of desk (associated with server)
        :param occupied: Boolean of occupancy status
        """

        self.__desk_name = desk_name
        self.__occupied = occupied
        self.__id = desk_id
        self.__desk_observers = set()

    def __str__(self):
        """
        Return Desk Info  *such wow*
        :return: String
        """

        return "Desk Name: '" + self.__desk_name + "', Currently Occupied: " + self.__occupied

    @property
    def occupied(self):
        """
        :return: Whether or not this desk object is currently occupied
        """

        return self.__occupied

    @property
    def desk_id(self):
        """
        :return: Desk ID
        """

        return self.__id

    @property
    def name(self):
        """
        :return: Desk Name
        """

        return self.__desk_name

    def add_observer(self, obj):
        """
        Register an observer for occupancy events. Must implement the
        DeskObserver protocol
        :param obj: The object that will subscribe to desk events
        :return: None
        """

        if isinstance(obj, DeskObserver):
            self.__desk_observers.add(obj)

    def remove_observer(self, obj):
        """
        Stop an observer from receiving desk occupancy events
        :param obj: The object that should be removed
        :return: None
        """
        self.__desk_observers.discard(obj)

    def input_received(self, pin, value):
        """
        Input callback for pin events from GPIO.
        Calls all subscribed objects to notify.
        :param pin: The pin that received the event
        :param value: The value of the pin
        :return: None
        """

        self.__occupied = value == 1

        # Notify all subscribers
        for sub in self.__desk_observers:
            sub.desk_occupied_updated(self, self.__occupied)


class DeskObserver:
    """
    Protocol for subscribing to desk events
    """

    def desk_occupied_updated(self, sender, new_val):
        """
        :param sender: The Desk Object that is sending the event whose occupancy has been updated
        :param new_val: A boolean value of whether the desk is occupied
        :return: None
        """
        raise NotImplementedError("This method must be overridden by the subclass")
