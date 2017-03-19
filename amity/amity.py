import sqlite3
# from database import *
from tabulate import tabulate
from termcolor import cprint, colored
import random


class Amity(object):
    all_persons = {
        'staffs': ['Daisy Wanjiru'],
        'fellows': ['Maureen Wangui', 'New person']
        }
    all_allocations = {
        'office': {
            'camelot': ['Daisy Wanjiru']
            },
        'living_space': {

        }
        }
    all_unallocated = []
    all_rooms = {
        'living_space': ['php'],
        'office': ['hogwarts', 'camelot', 'scala']
        }
    # db = Create_Database()
    # cursor = Cursor()
    # commit = Commit()
    # create_table = Create_table()
    # close_db = Close_db()

    def __init__(self):
        self.list_length = 0
        self.person_identifier = []
        self.new_room_name = ''
        self.room_type = ''
        self.room_names = []

    def create_room(self, room_type, room_name):
        """

        Create a list of rooms depending on the user's input

        """
        if room_type == 'O':
            if room_name in self.all_rooms['office'] or room_name in self.all_rooms['living_space']:
                cprint("%s room already exists..." % room_name, 'white')
            else:
                self.all_rooms['office'].append(room_name)
                cprint("<<...An Office: %s has been created...>>"
                       % room_name, 'cyan')

        elif room_type == 'L':
            if room_name in self.all_rooms['living_space'] or room_name in self.all_rooms['office']:
                cprint("%s room already exists..." % room_name, 'white')
            else:
                self.all_rooms['living_space'].append(room_name)
                cprint("<<...An Office: %s has been created...>>"
                       % room_name, 'cyan')
        else:
            cprint("invalid input. Type should be 'o' for office(s) or 'l' for living_space(s)", 'red')

    def add_person(self, position, person_name, want_accomodation=None):
        """

        Add a person/employee and allocate them a room and/or living space 
        depending on their position or preference(fellows)

        """
        # Check if staff exists
        if person_name in self.all_persons['staffs'] + self.all_persons['fellows']:
            print("...Employee: %s already exists..." % person_name)
        else:
            # Adding a staff and allocating them an office space
            if position == 'S' and want_accomodation == 'N':
                self.all_persons['staffs'].append(person_name)
                print("<<...Staff: %s has been added...>>" % person_name)
                # Allocating fellow an office
                self.random_office_space(person_name)
                print("...Allocated an Office Space...")

            # Adding a fellow and allocating an office space but deny them a living space
            elif position == 'S' and want_accomodation == 'Y':
                self.all_persons['staffs'].append(person_name)
                cprint("<<...Staff: %s has been added ...>>" % person_name, 'cyan')
                # Allocating fellow an office
                self.random_office_space(person_name)
                cprint("...Allocated an Office Space...", 'white')
                # Reject request for accomodation
                cprint("...Staff can not be allocated a Living Space...", 'white')
            # Adding a fellow and allocating them a living space and an office space
            elif position == 'F' and want_accomodation == 'Y':
                self.all_persons['fellows'].append(person_name)
                cprint("<<...Fellow: %s has been added...>>" % person_name, 'cyan')
                # Allocating fellow an office
                self.random_office_space(person_name)
                print("...Allocated an Office Space...")
                # Allocating fellow a living space
                self.random_living_space_space(person_name)
            # Adding a fellow and allocating them an office space only
            elif position == 'F' and want_accomodation == 'N':
                self.all_persons['fellows'].append(person_name)
                cprint("<<...Fellow: %s has been added ...>>" % person_name, 'cyan')
                # Allocating fellow an office
                self.random_office_space(person_name)
                cprint("...Allocated an Office Space...", 'white')
                # No accomodation
                self.all_unallocated.append(person_name)

    def random_office_space(self, person_name):
        available_room = []
        for room_name in self.all_allocations['office'].keys():
            if len(self.all_allocations['office'][room_name]) < 6:
                available_room.append(room_name)
            else:
                continue
        # set_allocations_office = set(self.all_allocations['office'])
        room_name = [room_name for room_name in self.all_rooms['office'] if
                     room_name not in self.all_allocations['office'].keys()]
        available_room.extend(room_name)
        allocated_office_name = random.choice(available_room)
        if allocated_office_name in self.all_allocations['office'].keys():
            self.all_allocations['office'][allocated_office_name].append(person_name)
        else:
            self.all_allocations['office'][allocated_office_name] = []
            self.all_allocations['office'][allocated_office_name].append(person_name)

    def random_living_space_space(self, person_name):
        available_room = []
        for room_name in self.all_allocations['living_space'].keys():
            if len(self.all_allocations['living_space'][room_name]) < 6:
                available_room.append(room_name)
            else:
                continue
        room_name = [room_name for room_name in self.all_rooms['living_space'] if
                     room_name not in self.all_allocations['living_space'].keys()]
        available_room.extend(room_name)
        allocated_living_space_name = random.choice(available_room)
        if allocated_living_space_name in self.all_allocations['living_space'].keys():
            self.all_allocations['living_space'][allocated_living_space_name].append(person_name)
        else:
            self.all_allocations['living_space'][allocated_living_space_name] = []
            self.all_allocations['living_space'][allocated_living_space_name].append(person_name)

    def reallocate_staff(self, person_name, new_room_name):
        """
        Reallocates a fellow to a new office or new living space
        """
        # Reallocate a staff to a new room
        if new_room_name in self.all_allocations['office'].keys() and len(
                self.all_allocations['office'][new_room_name]) < 6:
            # Delete previous allocation
            self.remove_person_from_previous_allocation_office(person_name)
            # Reallocate to the new room
            self.all_allocations['office'][new_room_name].append(person_name)
            cprint('%s has been reallocated successfully...', 'white')
        elif new_room_name in self.all_allocations['office'].keys() and len(
                self.all_allocations['office'][new_room_name]) > 6:
            cprint('This room is already full. Please choose another room.', 
                   'red')
        elif new_room_name not in self.all_allocations['office'].keys():
            # Delete previous allocation
            self.remove_person_from_previous_allocation_office(person_name)
            # Reallocate to the new room
            self.all_allocations['office'][new_room_name] = []
            self.all_allocations['office'][new_room_name].append(person_name)
            cprint('%s has been reallocated successfully...', 'white')
        else:
            print("An error occured...")

    def reallocate_fellow(self, person_name, new_room_name):
        """
        Reallocates a fellow to a new office or new living space
        """
        # Reallocate a fellow to a new office
        if new_room_name in self.all_rooms['office']:
            if new_room_name in self.all_allocations['office'].keys() and len(
                    self.all_allocations['office'][new_room_name]) < 6:
                # Delete previous allocation
                self.remove_person_from_previous_allocation_office(person_name)
                # Reallocate to the new room
                self.all_allocations['office'][new_room_name].append(person_name)
                cprint('%s has been reallocated successfully...', 'white')
            elif new_room_name in self.all_allocations['office'].keys() and len(
                    self.all_allocations['office'][new_room_name]) > 6:
                print('This room is already full. Please choose another room.')
            elif new_room_name not in self.all_allocations['office'].keys():
                # Delete previous allocation
                self.remove_person_from_previous_allocation_office(person_name)
                # Reallocate to the new room
                self.all_allocations['office'][new_room_name] = []
                self.all_allocations['office'][new_room_name].append(person_name)
                cprint('%s has been reallocated successfully...', 'white')
        # Reallocate a fellow to a new Living_space
        elif new_room_name in self.all_rooms['living_space']:
            if new_room_name in self.all_allocations['living_space'].keys() and len(
                    self.all_allocations['living_space'][new_room_name]) < 6:
                # Reallocate to the new room
                self.remove_person_from_previous_allocation_living_space(person_name)
                # Delete previous allocation
                self.all_allocations['living_space'][new_room_name].append(person_name)
                cprint('%s has been reallocated successfully...', 'white')
            elif new_room_name in self.all_allocations['living_space'].keys() and len(
                    self.all_allocations['living_space'][new_room_name]) > 6:
                print('This room is already full. Please choose another room.')
            elif new_room_name not in self.all_allocations['living_space'].keys():
                # Delete previous allocation
                self.remove_person_from_previous_allocation_living_space(person_name)
                # Reallocate to the new room
                self.all_allocations['living_space'][new_room_name] = []
                self.all_allocations['living_space'][new_room_name].append(person_name)
                cprint('%s has been reallocated successfully...', 'white')
        else:
            print('An error occurred...')

    def reallocate_person(self, person_name, new_room_name):
        """
        Checks if the person is a felloe or staff.
        Also cheks if the room_name provided is a living space
        or an office and reallocates accordingly
        """
        if person_name in self.all_persons['staffs'] and new_room_name in self.all_rooms['office']:
            return self.reallocate_staff(person_name, new_room_name)
        # Checks if the person is a fellow
        elif person_name in self.all_persons['fellows']:
            return self.reallocate_fellow(person_name, new_room_name)
        # Checks if the person is a staff and if the room is a living space
        elif person_name in self.all_persons['staffs'] and new_room_name in self.all_rooms['living_space']:
            cprint('Staff can not be reallocated to a living space', 'red')
        # Checks if person is in the system
        elif person_name not in self.all_persons['staffs'] and person_name not in self.all_persons['fellows']:
            cprint('%s is not an employee...' % person_name, 'red')
        else:
            cprint('There is no room %s' % new_room_name, 'red')

    def remove_person_from_previous_allocation_office(self, person_name):
        """
        Delete the previous record of office allocations if any
        """
        for room, persons in self.all_allocations['office'].items():
            if person_name in persons:
                self.all_allocations['office'][room].remove(person_name)
            else:
                continue

    def remove_person_from_previous_allocation_living_space(self, person_name):
        """
        Delete the previous record of living_space allocations if any
        """
        for room, persons in self.all_allocations['living_space'].items():
            if person_name in persons:
                self.all_allocations['living_space'][room].remove(person_name)
            else:
                continue

    def print_room(self, room_name):
        """

        Prints all the allocated people in the specified room_name
        if any.

        """
        if room_name in self.all_rooms['office']:
            if room_name in self.all_allocations['office']:
                cprint('OFFICE NAME: %s' % room_name, 'blue')
                cprint('*'*60, 'cyan')
                cprint('\n '.join(self.all_allocations['office'][room_name]),
                       'blue')
            else:
                cprint("Room %s has no allocations" % room_name, 'white')

        elif room_name in self.all_rooms['living_space']:
            if room_name in self.all_allocations['living_space']:
                cprint('LIVING SPACE NAME: %s' % room_name, 'blue')
                cprint('*'*60, 'cyan')
                cprint('\n '.join(self.all_allocations['living_space']
                                  [room_name]), 'blue')
            else:
                cprint("Room %s has no allocations" % room_name, 'white')
        else:
            cprint("Room %s does not exist" % room_name, 'white')

    def print_allocations(self, filename=None):
        """

        Prints all the rooms and the people assigned to them.
        It can display this in a text file ore the screen.

        """
        # Printing into a txt file
        if filename is not None:
            filepath = 'files/' + filename + '.txt'
            allocations_file = open(filepath, "w")
            print("Printing to %s..." % filename)
            allocations_file.write('\t\t...OFFICE...\n')
            for key, items in self.all_allocations['office'].items():
                item = ', '.join(items)
                allocations_file.write('\t' + key + '\n---------------------\n' + item + '\n\n')
            allocations_file.write('\t\t...LIVING SPACE...\n')
            for key, items in self.all_allocations['living_space'].items():
                item = ', '.join(items)
                allocations_file.write('\t' + key + '\n---------------------\n' + item + '\n\n')
            allocations_file.close()
            print('Done.')
        elif filename is None:
            if len(self.all_allocations) > 0:
                print('...OFFICE...')
                # Print all offices and the person names assigned to that room
                for key, value in self.all_allocations['office'].items():
                    print(key, '\n', ',\t'.join(map(str, value)))
                print('\n')
                print('%'*60)
                print('...LIVING SPACE...')
                # Print all living spaces and the person names assigned to that room
                for key, value in self.all_allocations['living_space'].items():
                    print(key, '\n', ',\t'.join(map(str, value)))
            else:
                cprint("There are no allocations at the moment...", 'white')
        else:
            print('...Invalid Command...Please try again...')

    def print_unallocated(self, filename=None):
        """
        Displays all the unallocated people
        """
        # Print on screen
        if filename is not None:
            filepath = 'files/' + filename + '.txt'
            unallocated_file = open(filepath, 'w')
            cprint("Printing to file %s..." % filename , 'white')
            unallocated_file.write('\t \t \t...UNALLOCATED PEOPLE...\n')
            for name in self.all_unallocated:
                unallocated_file.write(name + ',\t')
            unallocated_file.close()
            cprint('Done.')
        # Print in a txt file
        elif filename is None:
            if len(self.all_unallocated) > 0:
                cprint(',\t'.join(map(str, self.all_unallocated)), 'cyan')
            else:
                cprint("There are no unallocated people at the moment...", 'white')
        else:
            cprint('invalid', 'red')

    def load_people(self):
        """
        Collects details about employees and adds them to the system
        """
        load_people_file = open('files/load_People.txt')
        for line in load_people_file.read().splitlines():
            if len(line) == 0:
                continue
            list_words = line.split(' ')
            person_name = ' '.join(list_words[:2])
            position = ''.join(list_words[2][0])
            try:
                want_accomodation = ''.join(list_words[3])
            except IndexError:
                want_accomodation = 'N'
            # print(position)
            self.add_person(position, want_accomodation, person_name)
            print('%s has been added' % person_name)

    def save_state(self, db_name=None): # TODO
        if db_name is not None:
            db = db_name + '.db'
        else:
            db = 'mity.db'

        try:
            # Save all employees
            for position, names in self.all_persons.items():
                for name in names:
                    try:
                        self.cursor.execute("INSERT INTO employee VALUES (null,?,?);",
                                            (name, position))
                    except sqlite3.IntegrityError:
                        continue
            # Save all all_rooms
            for room_type, room_names in self.all_rooms.items():
                for name in room_names:
                    try:
                        self.conn.execute("INSERT INTO room VALUES (null,?,?);",
                                          (name, room_type))
                    except sqlite3.IntegrityError:
                        continue
            self.db_conn.commit()

            # Save allocations
            for room_name, person_names in self.all_allocations['office'].items():
                for person_name in person_names:
                    employee_id = self.conn.execute("SELECT employee_id FROM employee WHERE name=?",
                                                    (person_name,))
                    for e_id in employee_id:
                        employee_id = e_id[0]
                    room_id = self.conn.execute("SELECT room_id FROM room WHERE name=?",
                                                (room_name,))
                    for r_id in room_id:
                        room_id = r_id[0]
                    try:
                        self.conn.execute("INSERT INTO allocation VALUES (null,?,?);",
                                          (employee_id, room_id))
                    except sqlite3.IntegrityError:
                        continue
            self.db_conn.commit()

            # Save Unallocated people
            for person_name in self.all_unallocated:
                employee_id = self.conn.execute("SELECT employee_id FROM employee WHERE name=?",
                                                (person_name,))
                for e_id in employee_id:
                    employee_id = e_id[0]
                try:
                    self.conn.execute("INSERT INTO unallocated VALUES (null,?);",
                                      (employee_id,))
                except sqlite3.IntegrityError:
                    continue
            self.db_conn.commit()
        except:
            print('An error occured')
        self.db_conn.close()

    def load_state(self):
        """

        Collects all the stored information and loads it into the application
        This data persists for as long as the application is running after 
        running this function

        """
        try:
            # Load all employees from the Database
            cprint('Loading Employees...\n', 'white')
            data = self.conn.execute("SELECT name, position FROM employee")
            try:
                for row in data:
                    person_name = row[0]
                    position = row[1]
                    if position is 'staff':
                        self.all_persons['staff'].append(person_name)
                    else:
                        self.all_persons['fellow'].append(person_name)
                cprint('*'*40)
                cprint('\nLoaded successfully...\n', 'white')
            except:
                cprint("Able to load data. An error occurred.", 'red')
            try:
                # Load all rooms from the Database
                cprint('Loading rooms...\n', 'white')
                data = self.conn.execute("SELECT name, room_type FROM room")
                for row in data:
                    name = row[0]
                    room_type = row[1]
                    if room_type is 'office':
                        self.all_rooms['office'].append(name)
                    else:
                        self.all_rooms['living_space'].append(name)
                cprint('*'*40)
                cprint('\nLoaded successfully...\n', 'white')
            except:
                cprint("Able to load data. An error occurred.", 'red')
            try:
                # Load all allocate people from the Database
                cprint('Loading allocations...\n', 'white')
                data = self.conn.execute("SELECT employee_id, room_id FROM allocation")
                for row in data:
                    employee_id = row[0]
                    room_id = row[1]
                    emp_data = self.conn.execute("SELECT employee_name FROM employee WHERE employee_id=?",
                                                 (employee_id))
                    room_data = self.conn.execute("SELECT room_name, room_type FROM employee WHERE room_id=?",
                                                  (rooms_id))
                    employee_name = [row[0] for row in emp_data]
                    room_name = [row[0] for row in room_data]
                    room_type = [row[1] for row in room_data]
                    if room_type == 'office':
                        self.all_allocations['office'][room_name].append[employee_name]
                    else:
                        self.all_allocations['living_space'][room_name].append[employee_name]
                    print(self.all_allocations['living_space'][room_name])
                cprint('*'*40)
                cprint('\nLoaded successfully...\n', 'white')
                # load unallocated
                cprint('Loading unallocated...', 'white')
                data = self.conn.execute("SELECT employee_id FROM unallocated")
                for row in data:
                    employee_id = row[0]
                    emp_data = self.conn.execute("SELECT name FROM employee WHERE employee_id=?", (employee_id))
                    for data in emp_data:
                        employee_name = row[0]
                    print(employee_name)
                    print(self.all_unallocated.append(employee_name))
                cprint('*'*40)
                cprint('\nLoaded successfully...\n', 'white')
            except:
                cprint("Able to load data. An error occurred.", 'red')
        except:
            cprint("Able to load data. An error occurred.", 'red')
