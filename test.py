import unittest
import sys
import os

from amity.amity import Amity


class Test_Amity(unittest.TestCase):

    def setUp(self):
        # Creates an object (amity) that calls class Amity_allocation.
        self.amity = Amity()

    def test_create_living_space(self):
        '''
        This tests if the length of the living space list of living space increases after 
        the new rooms have been created

        '''
        # Checks the length of the living space list before adding new rooms
        self.counter = len(self.amity.all_rooms['living_space'])
        self.amity.create_room('l', ['php'])
        # Checks the length of the living space list after adding new rooms and confirms if it is greater than the previous
        self.assertGreater(len(self.amity.all_rooms['living_space']), self.counter)

    def test_create_office_space(self):
        '''
        This tests if the length of the list of office increases after 
        the new rooms have been created
        '''
        # office list length before adding new rooms
        self.counter = len(self.amity.all_rooms['office'])
        self.amity.create_room('o', ['hogwarts', 'narnia'])
        # office list length before adding new rooms
        self.assertGreater(len(self.amity.all_rooms['office']), self.counter)

    def test_rejects_office_name_if_already_exists(self):
        '''
        Check if office name already exists.
        '''
        self.assertEqual(self.amity.create_room('o', ['hogwarts']),
                         '!!!!...Office already exists...!!!!')

    def test_rejects_living_space_name_if_already_exists(self):
        '''
        Check if living_space name already exists.
        '''
        self.assertEqual(self.amity.create_room('l', ['Scala', 'Go']), '!!!!...Living space already exists...!!!!')


if __name__ == "__main__":
    unittest.main()
