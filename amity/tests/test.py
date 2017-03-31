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
        self.amity.all_unallocated = {
            'office': ['Lavender Ayodi'],
            'living_space': ['Maureen Wangui']
        }
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
        count = len(self.amity.all_unallocated['living_space'])
        self.amity.add_person('F', 'Mary mary', 'N')
        self.assertGreaterEqual(len(
            self.amity.all_unallocated['living_space']), count)

    def test_rejects_person_if_they_already_exists(self):
        self.amity.add_person('S', 'Daisy Wanjiru', 'N')
        message = sys.stdout.getvalue().strip()
        self.assertIn('Daisy Wanjiru already exists...', message)

    def test_reallocate_person(self):
        person_name = 'Daisy Wanjiru'
        new_room = self.amity.all_rooms['office'][0]
        new_room_name = 'hogwarts'
        self.amity.reallocate_person(person_name, new_room_name)
        self.assertIn(person_name, new_room.occupants)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Daisy Wanjiru has been reallocated successfully...',
                      message)

    def test_reallocate_person(self):
        person_name = 'Maureen Wangui'
        new_room = self.amity.all_rooms['office'][0]
        new_room_name = 'hogwarts'
        self.amity.reallocate_person(person_name, new_room_name)
        self.assertIn(person_name, new_room.occupants)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Maureen Wangui has been reallocated successfully...',
                      message)

    def test_reallocate_fellow_to_a_living_space(self):
        person_name = 'Maureen Wangui'
        new_room = self.amity.all_rooms['living_space'][0]
        new_room_name = 'php'
        self.amity.reallocate_person(person_name, new_room_name)
        self.assertIn(person_name, new_room.occupants)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Maureen Wangui has been reallocated successfully...',
                      message)

    def test_if_staff_already_exist_in_the_new_room(self):
        person_name = 'Daisy Wanjiru'
        new_room = self.amity.all_rooms['office'][0]
        new_room.occupants.append('Daisy Wanjiru')
        new_room_name = 'hogwarts'
        self.amity.reallocate_person(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Daisy Wanjiru is already allocated in hogwarts...',
                      message)

    def test_if_staff_is_not_reallocated_to_a_living_space(self):
        person_name = 'Daisy Wanjiru'
        new_room_name = 'php'
        self.amity.reallocate_person(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('A Staff can not be allocated to a living space',
                      message)

    def test_if_fellow_already_exist_in_the_new_office(self):
        person_name = 'Maureen Wangui'
        new_room = self.amity.all_rooms['office'][0]
        new_room.occupants.append('Maureen Wangui')
        new_room_name = 'hogwarts'
        self.amity.reallocate_a_fellow(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Maureen Wangui is already allocated in hogwarts...',
                      message)

    def test_if_fellow_already_exist_in_the_new_living_space(self):
        person_name = 'Maureen Wangui'
        new_room = self.amity.all_rooms['living_space'][0]
        new_room.occupants.append('Maureen Wangui')
        new_room_name = 'php'
        self.amity.reallocate_a_fellow(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Maureen Wangui is already allocated in php...',
                      message)

    def test_remove_person_from_previous_LSpace_allocations(self): 
        person_name = 'Maureen Wangui'
        room = self.amity.all_rooms['living_space'][0]
        room.occupants.append('Maureen Wangui')
        self.assertIn('Maureen Wangui', room.occupants)
        self.amity.remove_person_from_previous_LSpace_allocations(person_name)
        self.assertNotIn('Maureen Wangui', room.occupants)

    def test_remove_person_from_previous_office_allocations(self): 
        person_name = 'Maureen Wangui'
        room = self.amity.all_rooms['office'][0]
        room.occupants.append('Maureen Wangui')
        self.assertIn('Maureen Wangui', room.occupants)
        self.amity.remove_person_from_previous_office_allocations(person_name)
        self.assertNotIn('Maureen Wangui', room.occupants)

    def test_if_new_office_is_fullwhen_reallocating_a_staff(self):
        person_name = 'Daisy Wanjiru'
        office = self.amity.all_rooms['office'][2]
        office.occupants = ['John Doe', 'TEST USER',
                            'Another Staff', 'Maureen Wangui',
                            'Jane Doe', 'Clare C']
        new_room_name = 'camelot'
        self.amity.reallocate_person(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('camelot is full. Please pick another room',
                      message)

    def test_if_new_office_is_full_when_reallocating_a_fellow(self):
        person_name = 'Maureen Wangui'
        office = self.amity.all_rooms['office'][2]
        office.occupants = ['John Doe', 'TEST USER',
                            'Another Staff', 'Daisy Wanjiru',
                            'Jane Doe', 'Clare C']
        new_room_name = 'camelot'
        self.amity.reallocate_person(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('camelot is full. Please pick another room',
                      message)

    def test_if_new_living_space_is_full(self):
        person_name = 'Maureen Wangui'
        living_space = self.amity.all_rooms['living_space'][1]
        living_space.occupants = ['John Doe', 'TEST USER',
                                  'user user', 'Another Staff',
                                  ]
        new_room_name = 'scala'
        self.amity.reallocate_person(person_name, new_room_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('scala is full. Please pick another room',
                      message)

    def test_print_room_living_space(self):
        living_space_name = 'php'
        living_space = self.amity.all_rooms['living_space'][0]
        living_space.occupants.append('TEST USER')
        self.amity.print_room(living_space_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('TEST USER', message)

    def test_print_room_office(self):
        office_name = 'camelot'
        office = self.amity.all_rooms['office'][2]
        office.occupants.append('TEST USER')
        self.amity.print_room(office_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('TEST USER', message)

    def test_print_allocations_on_screen(self):
        filename = None
        office_name = 'camelot'
        office = self.amity.all_rooms['office'][2]
        office.occupants.append('Daisy Wanjiru')

        living_space_name = 'php'
        living_space = self.amity.all_rooms['living_space'][0]
        living_space.occupants.append('TEST USER')

        self.amity.print_allocations(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Daisy Wanjiru', message)

    def test_print_allocations_in_a_txt_file(self):
        filename = 'test_allocation'
        office_name = 'camelot'
        office = self.amity.all_rooms['office'][2]
        office.occupants.append('Daisy Wanjiru')

        living_space_name = 'php'
        living_space = self.amity.all_rooms['living_space'][0]
        living_space.occupants.append('TEST USER')

        self.amity.print_allocations(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Done', message)

    def test_print_unallocated_on_screen(self):
        filename = None
        self.amity.print_unallocated(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Lavender Ayodi', message)

    def test_print_unallocated_in_a_txt_file(self):
        filename = 'test_unallocated'
        self.amity.print_unallocated(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Done', message)

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
        message = sys.stdout.getvalue().strip()
        self.assertIn('Done', message)

    def test_print_all_rooms_on_screen(self):
        filename = None
        self.amity.print_all_rooms(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('hogwarts', message)

    def test_print_all_rooms_into_a_txt_file(self):
        filename = 'test_all_rooms'
        self.amity.print_all_rooms(filename)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Done', message)

if __name__ == "__main__":
    unittest.main()
