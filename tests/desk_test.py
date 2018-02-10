import unittest
from desk import Desk, DeskObserver


class TestDeskMethods(unittest.TestCase):

    class TestObserver(DeskObserver):
        def __init__(self):
            self.__success = False
            self.__new_val = -1
            self.__sender = None
            self.__was_called = False

        def desk_occupied_updated(self, sender, new_val):
            self.__sender = sender
            self.__new_val = new_val
            self.__was_called = True

        def is_success(self, sender, val):
            if not self.__was_called:
                return False

            self.__was_called = False
            return sender is self.__sender and val == self.__new_val

    def setUp(self):
        self.__desk_id = 7357
        self.__desk_name = "Desk Test"
        self.__desk_occupied = True
        self.__desk_test_obj = Desk(self.__desk_name, self.__desk_id, self.__desk_occupied)

    def test_valid_init_and_properties(self):
        self.assertEqual(self.__desk_test_obj.occupied, self.__desk_occupied, "Test init: Setting Occupancy")
        self.assertEqual(self.__desk_test_obj.desk_id, self.__desk_id, "Test init: Setting Id")
        self.assertEqual(self.__desk_test_obj.name, self.__desk_name, "Test init: Setting Name")

    def test_valid_input_received(self):
        self.__desk_test_obj.input_received(True)
        self.assertTrue(self.__desk_test_obj.occupied, "Test input_received: Setting Occupied")

        self.__desk_test_obj.input_received(False)
        self.assertTrue(not self.__desk_test_obj.occupied, "Test input_received: Setting Not Occupied")

    def test_observer_pattern(self):
        test_observer = self.TestObserver()

        # Add observer
        self.__desk_test_obj.add_observer(test_observer)

        # Initialize initial occupied status to False, so that
        # sequential inputs trigger a notification
        self.__desk_test_obj.input_received(False)

        # Make sure observer is notified with True
        self.__desk_test_obj.input_received(True)
        self.assertTrue(test_observer.is_success(self.__desk_test_obj, True))

        # Make sure observer is notified with False
        self.__desk_test_obj.input_received(False)
        self.assertTrue(test_observer.is_success(self.__desk_test_obj, False))

        # Make sure observer is removed
        self.__desk_test_obj.remove_observer(test_observer)
        self.__desk_test_obj.input_received(False)
        self.assertFalse(test_observer.is_success(self.__desk_test_obj, False))









