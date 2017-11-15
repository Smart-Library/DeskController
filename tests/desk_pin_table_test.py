import unittest
import desk_pin_table


class DeskPinTableTest(unittest.TestCase):

    def setUp(self):
        self.__desk_pin_table = desk_pin_table.DeskPinTable()

    def test_valid_get_desk_from_id(self):
        desk_obj = self.__desk_pin_table.get_desk_from_id(1)
        self.assertEqual(desk_obj.desk_id, 1)

        desk_obj = self.__desk_pin_table.get_desk_from_id(2)
        self.assertEqual(desk_obj.desk_id, 2)

    def test_correct_pin_mapping(self):
        pin = self.__desk_pin_table.get_pin_from_id(1)
        self.assertEqual(pin, 2)

        pin = self.__desk_pin_table.get_pin_from_id(2)
        self.assertEqual(pin, 3)

    def test_invalid_get_desk_from_id(self):
        desk_obj = self.__desk_pin_table.get_desk_from_id(-1)
        self.assertEqual(desk_obj, None)

        desk_obj = self.__desk_pin_table.get_desk_from_id(3)
        self.assertEqual(desk_obj, None)
