import unittest
from desk import Desk


class TestDeskMethods(unittest.TestCase):

    def test_get_occupied(self):
        test = Desk("Name", 7357, True)
        self.assertTrue(test.get_occupied(), "Occupancy")
