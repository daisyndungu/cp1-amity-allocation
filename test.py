import unittest
import sys
from io import StringIO
import sqlite3

from amity.amity import Amity
from amity.database import Database


class Test_Amity(unittest.TestCase):

    def setUp(self):
        # Creates an object (amity) that calls class Amity_allocation.
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()
        self.amity.all_persons = {
                'staff': ['Daisy Wanjiru'],
                'fellow': ['Maureen Wangui']
            }
        self.amity.all_allocations = {
                'office': {
                    'camelot': ['Daisy Wanjiru', 'Maureen Wangui'],
                    'hogwarts': []
                    },
                'living_space': {
                    'php': ['Maureen Wangui']
                }
                }
        self.amity.all_unallocated = []
        self.amity.all_rooms = {
                'living_space': ['php', 'scala'],
                'office': ['hogwarts', 'Narnia', 'camelot']
                }

    def test_create_living_space(self):  # pass
        '''
        This tests if the length of the living space list of living space 
        increases after the new rooms have been created

        '''
        # Checks the length of the living space list before adding new rooms
        counter = len(self.amity.all_rooms['living_space'])
        # Create new rooms
        self.amity.create_room('L', ['topaz'])
        # Checks the length of the living space list after adding new rooms and
        # confirms if it is greater than the previous
        self.assertGreater(len(self.amity.all_rooms['living_space']), counter)

    def test_create_office_space(self):  # pass
        '''
        This tests if the length of the list of office increases after
        the new rooms have been created
        '''
        counter = len(self.amity.all_rooms['office'])
        self.amity.create_room('O', ['narnia'])
        # office list length before adding new rooms
        self.assertGreater(len(self.amity.all_rooms['office']), counter)

    def test_rejects_office_name_if_already_exists(self):  # pass
        '''
        Check if office name already exists.
        '''
        self.amity.create_room('O', 'hogwarts')
        message = sys.stdout.getvalue().strip()
        self.assertIn('hogwarts room already exists...', message)

    def test_rejects_living_space_name_if_already_exists(self):  # pass
        '''
        Check if living_space name already exists.
        '''
        self.amity.create_room('L', 'php')
        message = sys.stdout.getvalue().strip()
        self.assertIn('php room already exists...', message)

    def test_add_person_staff(self):
        '''
        Tests if staff list increases after adding a new person
        '''
        # Checks the length of staffs list before adding a new person
        counter = len(self.amity.all_persons['staff'])
        # Adding a new person
        self.amity.add_person('S', ['John Doe'], 'N')
        # Checks the length of staff list after adding new rooms and confirms 
        # if it is greater than the previous
        self.assertGreater(len(self.amity.all_persons['staff']), counter)

    def test_add_person_fellow(self):
        '''
        Tests if fellow list increases after adding a new person
        '''
        # Checks the length of fellows list before adding a new person
        counter = len(self.amity.all_persons['fellow'])
        # Adding a new person
        self.amity.add_person('F', ['Jane Doe'], 'Y')
        # Checks the length of fellow list after adding new rooms and confirms
        # if it is greater than the previous
        self.assertGreater(len(self.amity.all_persons['fellow']), counter)

    def test_add_person_staff_rejects_request_for_accomodation(self):  # pass
        '''

        '''
        self.amity.add_person('S', 'Clare C', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('...Staff can not be allocated a Living Space..', message)

    def test_add_person_fellow_allocates_accomodation(self):  # pass
        self.amity.add_person('F', 'Lee ndungu', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Lee ndungu has been added...', message)

    def test_random_allocations_of_living_space(self):  # TODO
        person_name = 'John Doe'
        self.amity.random_living_space(person_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Successful.', message)

    def test_add_person_fellow_no_accomodation(self):  # TODO
        count = len(self.amity.all_unallocated)
        self.amity.add_person('F', 'Mary mary')
        self.assertGreaterEqual(len(self.amity.all_unallocated), count)

    def test_reallocate_person(self):
        person_name = 'Daisy Wanjiru'
        new_room_name = 'Narnia'
        self.amity.reallocate_staff(person_name, new_room_name)
        self.assertIn(person_name, self.amity.all_allocations['office']['Narnia'])

    def test_reallocate_fellow(self):
        person_name = 'Maureen Wangui'
        new_room_name = 'scala'
        self.amity.reallocate_fellow(person_name, new_room_name)
        self.assertIn(person_name, self.amity.all_allocations['living_space']['scala'])

    def test_remove_person_from_previous_allocation_office(self):  # TODO
        person_name = 'Maureen Wangui'
        self.amity.remove_person_from_previous_allocation_office(person_name)
        self.assertNotIn(person_name, self.amity.all_allocations['office']['camelot'])
        print('yryeye')

    def test_remove_person_from_previous_allocation_living_space(self):  # TODO
        person_name = 'Maureen Wangui'
        self.amity.remove_person_from_previous_allocation_living_space(person_name)
        self.assertNotIn(person_name, self.amity.all_allocations['living_space']['php'])

    def test_print_room_living_space(self):
        room_name = 'php'
        self.amity.print_room(room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('LIVING SPACE NAME: php', message)

    def test_print_room_office(self):
        room_name = 'camelot'
        self.amity.print_room(room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('OFFICE NAME: camelot', message)

    def test_empty_offices(self):
        key = 'hogwarts'
        self.amity.check_empty_offices(key)
        message = sys.stdout.getvalue().strip()
        self.assertIn('has no allocations at the moment...', message)

if __name__ == "__main__":
    unittest.main()
