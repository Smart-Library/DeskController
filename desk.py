import threading

'''
This class will essentially be a model for a desk, containing desk name, id, etc.
Note: pin information will be stored in desk_map
'''


class Desk:
    __id = -1
    __desk_name = ""
    __occupied = False
    __desk_observers = None

    # Use this for synchronizing the input_received function, since pin interrupt callbacks are async,
    # we get some weird behaviour if we dont synchronize it
    __lock = threading.Lock()

    '''
    Initialize Desk Object
    '''
    def __init__(self, desk_name, id=-1, occupied=False):
        self.__desk_name = desk_name
        self.__occupied = occupied
        self.__id = id
        self.__desk_observers = set()

    '''
    Print Desk Info  *such wow*
    '''
    def print_info(self):
        print "Desk Name:", self.__desk_name, ", Currently Occupied:", self.__occupied

    '''
    Gets whether or not this desk object is currently occupied
    '''
    def get_occupied(self):
        with self.__lock:
            return self.__occupied

    '''
    Get Desk ID
    '''
    def get_id(self):
        return self.__id

    '''
    Get Desk Name
    '''
    def get_name(self):
        return self.__desk_name

    '''
    Register an observer for occupancy events
    '''
    def register_occupied_change_event(self, obj):
        if obj not in self.__desk_observers:
            self.__desk_observers.add(obj)

    '''
    Register an observer for occupancy events
    '''
    def unregister_occupied_change_event(self, obj):
        self.__desk_observers.remove(obj)

    '''
    Input Received from GPIO pins
    '''
    def input_received(self, pin, value):

        # Use a thread lock for synchronizing this method so that no weird behaviour occurs
        # This also ensures that all subscribers get notified correctly and in order
        with self.__lock:
            self.__occupied = value == 1
            print "Desk Occupied: ", value

            for sub in self.__desk_observers:
                sub.desk_occupied_changed(self, self.__occupied)


'''
Protocol for subscribing to desk events
'''


class DeskObserver:
    def desk_occupied_changed(self, sender, new_val):
        pass
