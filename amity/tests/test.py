import unittest
import sys
import sqlite3
import os

from io import StringIO

from ..amity import Amity
from amity.database.database_file import Database
from amity.Person import Fellow, Staff
from amity.Room import LivingSpace, Office


class Test_Amity(unittest.TestCase):

    def setUp(self):
        # Creates an object (amity) that calls class Amity_allocation.
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()
        self.amity.all_persons = {
                'staff': [Staff('Daisy Wanjiru'), Staff('Lavender Ayodi')],
                'fellow': [Fellow('Maureen Wangui')]
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
        self.amity.all_unallocated = ['Lavender Ayodi']
        self.amity.all_rooms = {
                'living_space': [LivingSpace('php'), LivingSpace('scala')],
                'office': [Office('hogwarts'),
                           Office('Narnia'), Office('camelot')]
                }

    def test_create_living_space(self):
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

    def test_create_office_space(self):
        '''
        This tests if the length of the list of office increases after
        the new rooms have been created
        '''
        counter = len(self.amity.all_rooms['office'])
        self.amity.create_room('O', ['narnia'])
        # office list length before adding new rooms
        self.assertGreater(len(self.amity.all_rooms['office']), counter)

    def test_rejects_wrong_room_type(self):
        self.amity.create_room('Wrong_input', ['narnia'])
        message = sys.stdout.getvalue().strip()
        self.assertIn('invalid input.', message)

    def test_rejects_office_name_if_already_exists(self):
        '''
        Check if office name already exists.
        '''
        self.amity.create_room('O', 'hogwarts')
        message = sys.stdout.getvalue().strip()
        self.assertIn('hogwarts room already exists...', message)

    def test_rejects_living_space_name_if_already_exists(self):
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

    def test_add_person_staff_rejects_request_for_accomodation(self):
        '''

        '''
        self.amity.add_person('S', 'Clare C', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('...Staff can not be allocated a Living Space..',
                      message)

    def test_add_person_fellow_allocates_accomodation(self):
        self.amity.add_person('F', 'Lee ndungu', 'Y')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Lee ndungu has been added...', message)

    def test_random_allocations_of_living_space(self):
        fellow = Fellow('John Doe')
        self.amity.random_living_space(fellow)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Successful.', message)

    def test_add_person_fellow_no_accomodation(self):
        count = len(self.amity.all_unallocated)
        self.amity.add_person('F', 'Mary mary', 'N')
        self.assertGreaterEqual(len(self.amity.all_unallocated), count)

    def test_rejects_person_if_they_already_exists(self):
        self.amity.add_person('S', 'Daisy Wanjiru', 'N')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Daisy Wanjiru already exists...', message)

    def test_reallocate_person(self):
        person_name = 'Daisy Wanjiru'
        new_room_name = 'Narnia'
        self.amity.reallocate_staff(person_name, new_room_name)
        self.assertIn(person_name,
                      self.amity.all_allocations['office']['Narnia'])

    def test_reallocate_fellow(self):
        person_name = 'Maureen Wangui'
        new_room_name = 'scala'
        self.amity.reallocate_fellow(person_name, new_room_name)
        self.assertIn(person_name,
                      self.amity.all_allocations['living_space']['scala'])

    def test_remove_person_from_previous_allocation_office(self):
        person_name = 'Maureen Wangui'
        self.amity.remove_person_from_previous_allocation_office(person_name)
        self.assertNotIn(person_name,
                         self.amity.all_allocations['office']['camelot'])

    def test_remove_person_from_previous_allocation_living_space(self):
        person_name = 'Maureen Wangui'
        self.amity.remove_person_from_previous_allocation_living_space(
            person_name)
        self.assertNotIn(person_name,
                         self.amity.all_allocations['living_space']['php'])

    def test_print_room_living_space(self):
        living_space_name = 'php'
        living_space = LivingSpace('php')
        living_space.occupants = ['Test User']
        self.amity.print_room(living_space_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('LIVING SPACE NAME: php', message)

    def test_print_room_office(self):
        self.amity.add_person('Test User', 'S', 'N')
        Office('camelot').occupants = ['Test User']
        self.amity.print_room('camelot')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Test User', message)

    def test_empty_offices(self):
        key = 'hogwarts'
        self.amity.check_empty_offices(key)
        message = sys.stdout.getvalue().strip()
        self.assertIn('has no allocations at the moment...', message)

    def test_print_allocations_on_screen(self):
        filename = None
        self.amity.print_allocations(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Daisy Wanjiru,\tMaureen Wangui', message)

    def test_print_unallocated_on_screen(self):
        filename = None
        self.amity.print_unallocated(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Lavender Ayodi', message)

    def test_load_people_from_a_txt_file(self):
        filename = 'Load_People'
        self.amity.load_people(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Successful', message)

    def test_load_people_from_non_existent_txt_file(self):
        filename = 'This_does_not_exit.txt'
        self.amity.load_people(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('That file does not exist... Please try again.', message)

    def test_save_state(self):
        db_name = 'testAmityDB'
        self.amity.save_state(db_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Saved', message)

    def test_load_state(self):
        db_name = 'testAmityDB'
        self.amity.load_state(db_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Loaded successfully...', message)

    def test_print_all_persons_on_screen(self):
        filename = None
        self.amity.print_all_persons(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Lavender Ayodi', message)

    def test_print_all_persons_into_a_txt_file(self):
        filename = 'test_all_person'
        self.amity.print_all_persons(filename)
        for line in filename:
            if 'Lavender Ayodi' in line:
                return True

    def test_print_all_rooms_on_screen(self):
        filename = None
        self.amity.print_all_rooms(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('hogwarts', message)

    def test_print_all_rooms_into_a_txt_file(self):
        filename = 'test_all_rooms'
        self.amity.print_all_rooms(filename)
        for line in filename:
            if 'hogwarts' in line:
                return True

if __name__ == "__main__":
    unittest.main()
