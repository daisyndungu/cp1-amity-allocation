import sqlite3
import random
import os

from termcolor import cprint, colored

from amity.database.database_file import Database


class Amity(object):
    all_persons = {
        'staff': [],
        'fellow': []
        }
    all_allocations = {
        'office': {},
        'living_space': {}
        }
    all_unallocated = []
    all_rooms = {
        'living_space': [],
        'office': []
        }

    def create_room(self, room_type, room_name):
        """

        Create a list of rooms depending on the user's input

        """
        if room_type == 'O':
            if room_name in self.all_rooms['office'] or room_name in \
                    self.all_rooms['living_space']:
                cprint("%s room already exists..." % room_name, 'red')
            else:
                self.all_rooms['office'].append(room_name)
                cprint("An Office: %s has been created...>>"
                       % room_name, 'cyan')

        elif room_type == 'L':
            if room_name in self.all_rooms['living_space'] or room_name in \
                 self.all_rooms['office']:
                cprint("%s room already exists..." % room_name, 'red')
            else:
                self.all_rooms['living_space'].append(room_name)
                cprint("An Living Space: %s has been created...>>"
                       % room_name, 'cyan')
        else:
            cprint("invalid input. Type should be 'o' for office(s) or 'l'\
                 for living_space(s)", 'red')

    def add_person(self, position, person_name, want_accomodation=None):
        """

        Add a person/employee and allocate them a room and/or living space
        depending on their position or preference(fellows)

        """
        # Check if staff exists
        if (person_name in self.all_persons['staff'] +
           self.all_persons['fellow']):
            cprint("...Employee: %s already exists..." % person_name, 'cyan')
        else:
            # Adding a staff and allocating them an office space
            if position == 'S' and want_accomodation == 'N':
                self.all_persons['staff'].append(person_name)
                cprint("Staff: %s has been added...>>\n" % person_name, 'cyan')
                # Allocating fellow an office
                self.random_office_space(person_name)

            # Adding a fellow and allocating an office space
            # but deny them a living space
            elif position == 'S' and want_accomodation == 'Y':
                self.all_persons['staff'].append(person_name)
                cprint("Staff: %s has been added ...>>" % person_name, 'cyan')
                # Allocating staff an office
                self.random_office_space(person_name)
                # Reject request for accomodation
                cprint("...Staff can not be allocated a Living Space...\
                ", 'white')

            # Adding a fellow and allocating them a living space
            # and an office space
            elif position == 'F' and want_accomodation == 'Y':
                self.all_persons['fellow'].append(person_name)
                cprint("Fellow: %s has been added...>>" % person_name, 'cyan')
                # Allocating fellow an office
                self.random_office_space(person_name)
                # Allocating fellow a living space
                self.random_living_space(person_name)

            # Adding a fellow and allocating them an office space only
            elif position == 'F' and want_accomodation == 'N':
                self.all_unallocated.append(person_name)
                self.all_persons['fellow'].append(person_name)
                cprint("Fellow: %s has been added ...>>" % person_name, 'cyan')
                # Allocating fellow an office
                self.random_office_space(person_name)

    def random_office_space(self, person_name):
        """
        Select all offices with allocations less than 6 and
        those that have none at all
        """
        if self.all_rooms['office']:
            cprint('Allocating an Office...\n', 'white')
            available_room = []
            for room_name in self.all_allocations['office'].keys():
                if len(self.all_allocations['office'][room_name]) < 6:
                    available_room.append(room_name)
                else:
                    continue
            room_name = [room_name for room_name in self.all_rooms['office'] if
                         room_name not in self.all_allocations['office'].keys()
                         ]
            available_room.extend(room_name)
            if available_room:
                allocated_office_name = random.choice(available_room)
                if allocated_office_name in self.all_allocations[
                                                                'office'
                                                                ].keys():
                    (self.all_allocations['office'][allocated_office_name].
                     append(person_name))
                else:
                    self.all_allocations['office'][allocated_office_name] = []
                    (self.all_allocations['office'][allocated_office_name].
                     append(person_name))
                cprint("Successful.\n", 'yellow')
            else:
                cprint('There are no available office at the moment...\n',
                       'red')
                self.all_unallocated.append(person_name)
                cprint('%s has been added to the waiting list...\n'
                       % person_name,
                       'magenta')
        else:
            # No accomodation
            self.all_unallocated.append(person_name)
            cprint('There are no available Offices at the moment...\n',
                   'red')

    def random_living_space(self, person_name):
        """
        Select all living space with allocations less than 4 and
        those that have none at all
        """
        if self.all_rooms['living_space']:
            cprint('Allocating a living Space...\n', 'white')
            available_room = []
            for room_name in self.all_allocations['living_space'].keys():
                if len(self.all_allocations['living_space'][room_name]) < 4:
                    available_room.append(room_name)
                else:
                    continue
            room_name = [room_name for room_name in
                         self.all_rooms['living_space']
                         if room_name not in
                         self.all_allocations['living_space'].keys()]
            available_room.extend(room_name)
            if available_room:
                allocated_living_space_name = random.choice(available_room)
                if (allocated_living_space_name in
                   self.all_allocations['living_space'].keys()):
                    (self.all_allocations['living_space']
                     [allocated_living_space_name].append(person_name))
                else:
                    self.all_allocations['living_space'
                                         ][allocated_living_space_name] = []
                    self.all_allocations['living_space'
                                         ][allocated_living_space_name].append(
                                            person_name)
                cprint("Successful.\n", 'yellow')
            else:
                cprint('There are no available living space at the moment...\n\
                       ', 'red')
                self.all_unallocated.append(person_name)
                cprint('%s has been added to the waiting list...\n'
                       % person_name,
                       'magenta')
        else:
            # No accomodation
            self.all_unallocated.append(person_name)
            cprint('There are no available Living Space at the moment...\n\
            ', 'red')

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
            cprint('%s has been reallocated successfully...' % person_name,
                   'white')

        elif new_room_name in self.all_allocations['office'].keys() and len(
                self.all_allocations['office'][new_room_name]) >= 6:
            cprint('This room is already full. Please choose another room.\n',
                   'red')

        elif new_room_name not in self.all_allocations['office'].keys():
            # Delete previous allocation
            self.remove_person_from_previous_allocation_office(person_name)
            # Reallocate to the new room
            self.all_allocations['office'][new_room_name] = []
            self.all_allocations['office'][new_room_name].append(person_name)
            cprint('%s has been reallocated successfully...\n', 'white')
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
                (self.all_allocations['office'][new_room_name].
                    append(person_name))
                cprint('%s has been reallocated successfully...'
                       % person_name, 'white')
            elif new_room_name in self.all_allocations['office'].keys() and \
                    len(self.all_allocations['office'][new_room_name]) >= 6:
                cprint('This room is already full. Please choose another room.\
                       \n', 'red')
            elif new_room_name not in self.all_allocations['office'].keys():
                # Delete previous allocation
                self.remove_person_from_previous_allocation_office(person_name)
                # Reallocate to the new room
                self.all_allocations['office'][new_room_name] = []
                (self.all_allocations['office'][new_room_name].
                    append(person_name))
                cprint('%s has been reallocated successfully...\n'
                       % person_name, 'white')

        # Reallocate a fellow to a new Living_space
        elif new_room_name in self.all_rooms['living_space']:
            if new_room_name in self.all_allocations['living_space'].keys() \
              and len(self.all_allocations['living_space'][new_room_name]) < 4:
                # Reallocate to the new room
                (self.remove_person_from_previous_allocation_living_space(
                    person_name))
                # Delete previous allocation
                (self.all_allocations['living_space'][new_room_name].
                    append(person_name))
                cprint('%s has been reallocated successfully...'
                       % person_name, 'white')
            elif (new_room_name in self.all_allocations['living_space'].
                  keys() and len(self.all_allocations['living_space']
                  [new_room_name]) >= 4):
                cprint('This room is already full. Please choose another room.\
                       \n', 'red')
            elif (new_room_name not in self.all_allocations['living_space'].
                  keys()):
                # Delete previous allocation
                (self.remove_person_from_previous_allocation_living_space(
                    person_name))
                # Reallocate to the new room
                self.all_allocations['living_space'][new_room_name] = []
                (self.all_allocations['living_space'][new_room_name].append(
                    person_name))
                cprint('%s has been reallocated successfully...\n'
                       % person_name, 'white')
        else:
            print('An error occurred...')

    def remove_person_from_previous_allocation_office(self, person_name):
        """
        Delete the previous record of office allocations if any
        """
        for room, persons in self.all_allocations['office'].items():
            if person_name in persons:
                self.all_allocations['office'][room].remove(person_name)
            else:
                continue
        if person_name in self.all_unallocated:
            self.all_unallocated.remove(person_name)

    def remove_person_from_previous_allocation_living_space(self, person_name):
        """
        Delete the previous record of living_space allocations if any
        """
        for room, persons in self.all_allocations['living_space'].items():
            if person_name in persons:
                self.all_allocations['living_space'][room].remove(person_name)
            else:
                continue
        if person_name in self.all_unallocated:
            self.all_unallocated.remove(person_name)

    def reallocate_person(self, person_name, new_room_name):
        """
        Checks if the person is a felloe or staff.
        Also cheks if the room_name provided is a living space
        or an office and reallocates accordingly
        """
        if (person_name in self.all_persons['staff'] and new_room_name in
                self.all_rooms['office']):
            return self.reallocate_staff(person_name, new_room_name)
        # Checks if the person is a fellow
        elif person_name in self.all_persons['fellow']:
            return self.reallocate_fellow(person_name, new_room_name)
        # Checks if the person is a staff and if the room is a living space
        elif (person_name in self.all_persons['staff'] and new_room_name in
                self.all_rooms['living_space']):
            cprint('Staff can not be reallocated to a living space', 'red')
        # Checks if person is in the system
        elif (person_name not in self.all_persons['staff'] and person_name not
                in self.all_persons['fellow']):
            cprint('%s is not an employee...' % person_name, 'red')
        else:
            cprint('There is no room %s' % new_room_name, 'red')

    def print_room(self, room_name):
        """

        Prints all the allocated people in the specified room_name
        if any.

        """
        if room_name in self.all_rooms['office']:
            if room_name in self.all_allocations['office']:
                cprint('OFFICE NAME: %s' % room_name, 'blue')
                cprint('*'*60, 'cyan')
                cprint(',\t'.join(self.all_allocations['office'][room_name]),
                       'blue')
            else:
                cprint("Room %s has no allocations" % room_name, 'white')

        elif room_name in self.all_rooms['living_space']:
            if room_name in self.all_allocations['living_space']:
                cprint('LIVING SPACE NAME: %s' % room_name, 'blue')
                cprint('*'*60, 'cyan')
                cprint(',\t'.join(self.all_allocations['living_space']
                                  [room_name]), 'blue')
            else:
                cprint("Room %s has no allocations" % room_name, 'white')
        else:
            cprint("Room %s does not exist" % room_name, 'white')

    def check_empty_offices(self, key):
        """
        Check if Office has no allocations
        """
        if len(self.all_allocations['office'][key]) == 0:
            cprint('%s has no allocations at the moment...\n', 'white')
        else:
            pass

    def check_empty_living_space(self, key):
        """
        Check if living space has no allocations
        """
        if len(self.all_allocations['living_space'][key]) == 0:
            print('%s has no allocations at the moment...\n' % key)
        else:
            pass

    def print_allocations(self, filename=None):
        """

        Prints all the rooms and the people assigned to them.
        It can display this in a text file ore the screen.

        """
        try:
            # Printing into a txt file
            if filename:
                filepath = 'amity/files/' + filename + '.txt'
                output_file = open(filepath, "w")
                print("Printing to %s.txt ...\n\n" % filename)
                output_file.write('\t\t...OFFICE...\n')
                for key, items in self.all_allocations['office'].items():
                    self.check_empty_offices(key)
                    item = ', '.join(items)
                    output_file.write('\t' + key + '\n-----------------\
                    ----\n' + item + '\n\n')
                output_file.write('\t\t...LIVING SPACE...\n')
                for key, items in self.all_allocations['living_space'].items():
                    self.check_empty_living_space(key)
                    item = ', '.join(items)
                    output_file.write('\t' + key + '\n-------------\
                    --------\n' + item + '\n\n')
                output_file.close()
                cprint('\t\t ***Done***', 'white')
            else:
                cprint('...OFFICE...', 'cyan')
                if self.all_allocations['office']:
                    # Print all offices and the person names
                    # assigned to that room
                    for key, value in self.all_allocations['office'].items():
                        # Check for a blank office list
                        cprint(key, 'yellow')
                        # Check for empty rooms
                        self.check_empty_offices(key)
                        cprint(',\t'.join(map(str, value)), 'cyan')
                else:
                    cprint("There are no allocations at the moment...\
                    ", 'white')

                cprint('%'*60, 'white')
                cprint('...LIVING SPACE...', 'cyan')
                if self.all_allocations['living_space']:
                    # Print all living spaces and the person names
                    # assigned to that room
                    for key, value in self.all_allocations['living_space'].\
                         items():
                        cprint(key, 'yellow')
                        # Check for empty rooms
                        self.check_empty_living_space(key)
                        cprint(',\t'.join(map(str, value)), 'cyan')
                else:
                    cprint("There are no allocations at the moment...\
                    ", 'white')
        except:
            cprint('An error occurred.', 'red')

    def print_unallocated(self, filename=None):
        """
        Displays all the unallocated people
        """
        # Print in to a file
        if filename:
            filepath = 'amity/files/' + filename + '.txt'
            output_file = open(filepath, 'w')
            cprint("Printing to file %s..." % filename, 'white')
            output_file.write('\t \t \t...UNALLOCATED PEOPLE...\n')
            for name in self.all_unallocated:
                output_file.write(name + ',\t')
            output_file.close()
            cprint('Done', 'white')
        # Print on the screen
        else:
            if self.all_unallocated:
                cprint(',\t'.join(map(str, self.all_unallocated)), 'cyan')
            else:
                cprint('There are no unallocated persons at the moment...',
                       'red')

    def load_people(self, filename):
        """
        Collects details about employees and adds them to the system
        """
        try:
            filepath = 'amity/files/' + filename + '.txt'
            load_people_file = open(filepath)
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
                self.add_person(position, person_name, want_accomodation)
        except Exception as e:
            print('That file does not exist... Please try again.')
            print(str(e))

    def save_state(self, db_name=None):
        """
        Persists all the data stored in the app to a SQLite database
        """
        if db_name:
            db_name = db_name + '.db'
        else:
            db_name = 'Amity.db'

        try:
            db_path = 'amity/database/' + db_name
            db = Database(db_path)
            db.create_table()
            cursor = db.cursor()

            # Save all employees
            cprint('\t \tSaving to %s...' % db_path, 'white')
            for position, names in self.all_persons.items():
                for name in names:
                    try:
                        cursor.execute(
                            "INSERT INTO employee VALUES (null,?,?);",
                            (name, position))
                    except sqlite3.IntegrityError:
                        continue
            db.commit()

            # Save all all_rooms
            for room_type, room_names in self.all_rooms.items():
                for name in room_names:
                    try:
                        cursor.execute("INSERT INTO room VALUES (null,?,?);",
                                       (name, room_type))
                    except sqlite3.IntegrityError:
                        continue
            db.commit()

            # Save allocations
            for room_name, person_names in self.all_allocations['office'
                                                                ].items():
                for person_name in person_names:
                    employee_id = cursor.execute(
                        """
                        SELECT employee_id FROM employee WHERE name=?""",
                        (person_name,))
                    for e_id in employee_id:
                        employee_id = e_id[0]
                    room_id = cursor.execute(
                        "SELECT room_id FROM room WHERE name=?",
                        (room_name,))
                    for r_id in room_id:
                        room_id = r_id[0]
                    try:
                        cursor.execute(
                            "INSERT INTO allocation VALUES (null,?,?);",
                            (employee_id, room_id))
                    except sqlite3.IntegrityError:
                        continue
            for room_name, person_names in self.all_allocations['living_space'
                                                                ].items():
                for person_name in person_names:
                    employee_id = cursor.execute(
                        "SELECT employee_id FROM employee WHERE name=?",
                        (person_name,))
                    for e_id in employee_id:
                        employee_id = e_id[0]
                    room_id = cursor.execute(
                        "SELECT room_id FROM room WHERE name=?", (room_name,))
                    for r_id in room_id:
                        room_id = r_id[0]
                    try:
                        cursor.execute(
                            "INSERT INTO allocation VALUES (null,?,?);",
                            (employee_id, room_id))
                    except sqlite3.IntegrityError:
                        continue
            db.commit()

            # Save Unallocated people
            for person_name in self.all_unallocated:
                employee_id = cursor.execute(
                    "SELECT employee_id FROM employee WHERE name=?",
                    (person_name,))
                for e_id in employee_id:
                    employee_id = e_id[0]
                try:
                    cursor.execute("INSERT INTO unallocated VALUES (null,?);",
                                   (employee_id,))
                except sqlite3.IntegrityError:
                    continue
            db.commit()
            cprint('\t \t *Saved successfully...', 'white')
            db.close_db()
        except Exception as e:
            print('An error occured')
            print(str(e))

    def load_all_persons_from_db(self, person_data):
        # Load all employees from the Database
        cprint('Loading Employees...\n', 'white')
        try:
            for row in person_data:
                person_name = row[0]
                position = row[1]
                if position == 'staff':
                    self.all_persons['staff'].append(person_name)
                else:
                    self.all_persons['fellow'].append(person_name)
            cprint('*'*40)
            cprint('\nLoaded successfully...\n', 'white')
        except:
            cprint('There are no Staff/Fellows in the Database', 'white')

    def load_all_rooms_from_db(self, room_data):
        try:
            # Load all rooms from the Database
            cprint('Loading rooms...\n', 'white')
            for row in room_data:
                name = row[0]
                room_type = row[1]
                if room_type == 'office':
                    self.all_rooms['office'].append(name)
                else:
                    self.all_rooms['living_space'].append(name)
            cprint('*'*40)
            cprint('\nLoaded successfully...\n', 'white')
        except:
            cprint('There are no rooms in the Database', 'white')

    def load_all_allocations_from_db(self, allocation_data):
        try:
            # Load all allocate people from the Database
            cprint('Loading allocations...\n', 'white')
            for row in allocation_data:
                employee_name = row[0]
                position = row[1]
                room_name = row[2]
                room_type = row[3]
                if room_type == 'office':
                    if room_name not in self.all_allocations['office']:
                        self.all_allocations['office'][room_name] = []
                    (self.all_allocations['office'][room_name].
                        append(employee_name))
                elif room_type == 'living_space':
                    if room_name not in self.all_allocations['living_space']:
                        self.all_allocations['living_space'][room_name] = []
                    (self.all_allocations['living_space'][room_name].
                        append(employee_name))
                else:
                    cprint('An Error Occurred...', 'red')
            cprint('*'*40)
            cprint('\nLoaded successfully...\n', 'white')
        except:
            cprint('There are no allocations in the Database', 'white')

    def load_unallocated_people_data_from_db(self, unallocate_data):
        try:
            # load unallocated people data from db
            cprint('Loading unallocated...', 'white')
            for row in unallocate_data:
                employee_name = row[0]
                self.all_unallocated.append(employee_name)
            cprint('*'*40)
            cprint('\nLoaded successfully...\n', 'white')
        except Exception as e:
            cprint("Unable to load db. An error occurred.", 'red')
            print(str(e))

    def load_state(self, db_name=None):
        """
        Loads data from a database into the application.
        """
        if db_name:
            db_name = db_name + '.db'
        else:
            db_name = 'Amity.db'

        try:
            db_path = 'amity/database/' + db_name
            db = Database(db_path)
            cursor = db.cursor()
            # get all people's data from db
            person_data = db.load_all_persons_from_db()
            self.load_all_persons_from_db(person_data)
            # get all allocated data from db
            room_data = db.load_all_rooms_from_db()
            self.load_all_rooms_from_db(room_data)
            # get all allocated data from db
            allocation_data = db.query_allocation_records()
            self.load_all_allocations_from_db(allocation_data)
            # get all allocated data from db
            unallocate_data = db.query_unallocated_records()
            self.load_unallocated_people_data_from_db(unallocate_data)
        except:
            cprint('An error occured when loading data...', 'red')

    def print_all_persons(self, filename=None):
        """

        Prints all the staffs and fellows.
        It can display this in a text file or the screen.

        """
        try:
            # Printing into a txt file
            if filename:
                filepath = 'amity/files/' + filename + '.txt'
                output_file = open(filepath, "w")
                print("Printing to %s...\n" % filename)
                output_file.write('\t\t...STAFF...\n')
                for items in self.all_persons['staff']:
                    item = ''.join(items)
                    output_file.write('\n------------------\n' + item + '\n\n')
                output_file.write('\t\t...FELLOW...\n')
                for items in self.all_persons['fellow']:
                    item = ''.join(items)
                    output_file.write('\n------------------\n' + item + '\n\n')
                output_file.close()
                cprint('***Done***', 'white')
            else:
                cprint('...staff...', 'cyan')
                if self.all_persons['staff']:
                    # Print all staffs
                    for value in self.all_persons['staff']:
                        cprint(''.join(map(str, value)), 'cyan')
                else:
                    cprint("There are no staffs at the moment...", 'white')

                cprint('%'*60, 'white')
                cprint('...Fellow...', 'cyan')
                if self.all_persons['fellow']:
                    # Print all fellows
                    for value in self.all_persons['fellow']:
                        cprint(''.join(map(str, value)), 'cyan')
                else:
                    cprint("There are no fellows at the moment...", 'white')
        except:
            cprint('An error occurred.', 'red')

    def print_all_rooms(self, filename=None):
        """

        Prints all the offices and living spaces.
        It can display this in a text file or the screen.

        """
        try:
            # Printing into a txt file
            if filename:
                filepath = 'amity/files/' + filename + '.txt'
                output_file = open(filepath, "w")
                print("Printing to %s..." % filename)
                output_file.write('\t\t...OFFICE...\n')
                for items in self.all_rooms['office']:
                    item = ''.join(items)
                    output_file.write('\n------------------\n' + item + '\n\n')
                output_file.write('\t\t...LIVING SPACE...\n')
                for items in self.all_rooms['living_space']:
                    item = ''.join(items)
                    output_file.write('\n------------------\n' + item + '\n\n')
                output_file.close()
                cprint('***Done***', 'white')
            else:
                cprint('...OFFICES...', 'cyan')
                if self.all_rooms['office']:
                    # Print all staffs
                    for value in self.all_rooms['office']:
                        cprint(''.join(map(str, value)), 'cyan')
                else:
                    cprint("There are no offices at the moment...", 'white')

                cprint('%'*60, 'white')
                cprint('...LIVING SPACES...', 'cyan')
                if self.all_rooms['living_space']:
                    # Print all fellows
                    for value in self.all_rooms['living_space']:
                        cprint(''.join(map(str, value)), 'cyan')
                else:
                    cprint("There are no living_spaces at the moment", 'white')
        except:
            cprint('An error occurred.', 'red')
