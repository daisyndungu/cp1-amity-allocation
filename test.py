import unittest
import sys
from io import StringIO

from amity.amity import Amity


class Test_Amity(unittest.TestCase):

    all_persons = {
        'staffs': ['Daisy Wanjiru'],
        'fellows': ['Maureen Wangui']
        }
    all_allocations = {
        'office': {
            'camelot': ['Daisy Wanjiru']
            },
        'living_space': {
            'php': []
        }
        }
    all_unallocated = []
    all_rooms = {
        'living_space': ['php'],
        'office': ['hogwarts']
        }

    def setUp(self):
        # Creates an object (amity) that calls class Amity_allocation.
        self.amity = Amity()
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_create_living_space(self):  # pass
        '''
        This tests if the length of the living space list of living space increases after 
        the new rooms have been created

        '''
        # Checks the length of the living space list before adding new rooms
        counter = len(self.amity.all_rooms['living_space'])
        # Create new rooms
        self.amity.create_room('L', ['topaz'])
        # Checks the length of the living space list after adding new rooms and confirms if it is greater than the previous
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
        counter = len(self.amity.all_persons['staffs'])
        # Adding a new person
        self.amity.add_person('S', ['John Doe'], 'N')
        # Checks the length of staff list after adding new rooms and confirms 
        # if it is greater than the previous
        self.assertGreater(len(self.amity.all_persons['staffs']), counter)

    def test_add_person_fellow(self):
        '''
        Tests if fellow list increases after adding a new person
        '''
        # Checks the length of fellows list before adding a new person
        counter = len(self.amity.all_persons['fellows'])
        # Adding a new person
        self.amity.add_person('F', ['Jane Doe'], 'Y')
        # Checks the length of fellow list after adding new rooms and confirms
        # if it is greater than the previous
        self.assertGreater(len(self.amity.all_persons['fellows']), counter)

    def test_add_person_staff_rejects_request_for_accomodation(self):
        '''

        '''
        self.assertEqual(self.amity.add_person('Clare C', 'staff', 'y'), 'You are a staff hence will be allocated an Office but not a Living Space ')

    def test_add_person_fellow_allocates_accomodation(self):

        self.assertEqual(self.amity.add_person('Lee ndungu', 'fellow', 'y'), 'You are a fellow hence will be allocated an office and a Living Space')

    def test_random_allocations_of_offices(self):
        person_name = 'John Doe'
        self.amity.random_living_space_space(person_name)
        message = sys.stdout.getvalue().strip()
        self.assertIn('Allocating a living Space...', message)

    def test_add_person_fellow_no_accomodation(self):
        self.assertEqual(self.amity.add_person('John Doe', 'fellow', 'n'),
                         'You are a fellow hence will be allocated an office but not Living Space')

    def test_add_person_fellow_no_accomodation(self):
        self.assertEqual(self.amity.add_person('Mary mary', 'fellow', ''),
                         'You are a fellow hence will be allocated an office but not Living Space')

    def test_reallocate_person_to_different_living_space_if_fellow(self):
        self.assertEqual(self.amity.reallocate_person('Lee ndungu', 'php'),
                         'Jane Doe has been reallocated to a new living space: php')

    def test_reallocate_person_to_different_office_if_fellow_or_staff(self):
            self.assertEqual(self.amity.reallocate_person('Jane Doe', 'camelot'),
                             'Jane Doe has been reallocated to a new Office space: camelot')

    def test_rejects_reallocate_person_to_different_living_space_if_staff(self):
            self.assertEqual(self.amity.reallocate_person('Jane Doe', 'camelot'),
                             'Jane Doe can not be reallocated to a living space')

    def test_print_allocations_onto_the_screen(self):
        '''
        Test if prints allocations onto the screen (both staff and fellows). 
        It also specifies if they are allocated an office or a living space or both.
        '''
        self.assertEqual(self.amity.print_allocations(), 'These are all the allocations in Amity')

    def test_print_unallocated_onto_the_screen(self):
        '''
        Test if prints unallocated people onto the screen (both staff and fellows)
        '''
        self.assertEqual(self.amity.print_unallocated(), 'These are all the unallocated people in Amity')

    def test_print_office(self):
        '''
        Prints all the people in a room if the room name provided is an Office
        '''
        self.assertIn(self.amity.print_room('narnia'), self.amity.all_allocations['office'].keys())
        self.assertIn(self.amity.print_room('narnia'), 'This are all the allocations in narnia')

    def test_print_living_space(self):
        '''
        Prints all the people in a room if the room name provided is a living space
        '''
        self.assertIn(self.amity.print_room('Scala'), self.amity.all_allocations['living_space'].keys())
        self.assertIn(self.amity.print_room('Scala'), 'This are all the allocations in Scala')

if __name__ == "__main__":
    unittest.main()
