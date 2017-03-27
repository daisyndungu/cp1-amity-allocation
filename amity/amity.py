import sqlite3
import random
import os

from termcolor import cprint, colored

from amity.database.database_file import Database

from amity.Person import Fellow, Staff
from amity.Room import LivingSpace, Office


class Amity(object):
    all_persons = {
        'staff': [],
        'fellow': []
        }
    all_allocations = {
        'office': {},
        'living_space': {}
        }
    all_unallocated = {
        'office': [],
        'living_space': []
    }
    all_rooms = {
        'living_space': [],
        'office': []
        }

    def create_room(self, room_type, room_name):
        """
        Create a list of rooms depending on the user's input
        """
        # Check if room type give is O for office or
        # L for living space
        if room_type not in ['L', 'O']:
            cprint("invalid input. Type should be 'o' for office(s) or 'l'\
                for living_space(s)", 'red')
            return

        # Check if the room given already exists
        for room in self.all_rooms['office'] + self.all_rooms['living_space']:
            if room.name == room_name:
                cprint("%s room already exists..." % room_name, 'red')
                return
        # Create office space
        if room_type == 'O':
            new_office = Office(room_name)
            self.all_rooms['office'].append(new_office)
            cprint("An Office: %s has been created...>>"
                   % new_office.name, 'cyan')
        # Create living space
        elif room_type == 'L':
            self.all_rooms['living_space'].append(LivingSpace(room_name))
            cprint("An Living Space: %s has been created...>>"
                   % room_name, 'cyan')

    def add_person(self, position, person_name, want_accomodation):
        """
        Add a person/employee and allocate them a room and/or living space
        depending on their position or preference(fellows)
        """
        # Check if person exists
        for person in self.all_persons['staff'] + self.all_persons['fellow']:
            if person.name == person_name:
                cprint("...Employee: %s already exists..."
                       % person_name, 'cyan')
                return

        # Adding a staff and allocating them an office space
        if position == 'S' and want_accomodation == 'N':
            new_person = Staff(person_name)
            self.all_persons['staff'].append(new_person)
            cprint("Staff: %s has been added...>>\n" % new_person.name, 'cyan')
            # Allocating fellow an office
            self.random_office_space(person_name)

        # Adding a fellow and allocating an office space
        # but deny them a living space
        elif position == 'S' and want_accomodation == 'Y':
            new_person = Staff(person_name)
            self.all_persons['staff'].append(new_person)
            cprint("Staff: %s has been added ...>>" % new_person.name, 'cyan')
            # Allocating staff an office
            self.random_office_space(person_name)
            # Reject request for accomodation
            cprint("...Staff can not be allocated a Living Space...\
            ", 'white')

        # Adding a fellow and allocating them a living space
        # and an office space
        elif position == 'F' and want_accomodation == 'Y':
            new_person = Fellow(person_name, want_accomodation)
            self.all_persons['fellow'].append(new_person)
            cprint("Fellow: %s has been added...>>" % new_person.name, 'cyan')
            # Allocating fellow an office
            self.random_office_space(person_name)
            # Allocating fellow a living space
            self.random_living_space(person_name)

        # Adding a fellow and allocating them an office space only
        elif position == 'F' and want_accomodation == 'N':
            new_person = Fellow(person_name)
            self.all_unallocated['living_space'].append(person_name)
            self.all_persons['fellow'].append(new_person)
            cprint("Fellow: %s has been added ...>>" % new_person.name, 'cyan')
            # Allocating fellow an office
            self.random_office_space(person_name)

    def random_office_space(self, person_name):
        """
        Select all offices with allocations less than 6 and
        those that have none at all
        """
        # Check if there are existing offices
        if self.all_rooms['office']:
            cprint('Allocating an Office...\n', 'white')
            available_office = []
            for office in self.all_rooms['office']:
                if len(office.occupants) < office.space:
                    available_office.append(office)
                else:
                    continue
            print()
            if available_office:
                allocated_office_name = random.choice(available_office)
                allocated_office_name.occupants.append(person_name)
                cprint("Successful.\n", 'yellow')
            else:
                cprint('There are no available office at the moment...\n',
                       'red')
                self.all_unallocated['office'].append(person_name)
                cprint('%s has been added to the waiting list...\n'
                       % person_name,
                       'magenta')
        else:
            # No accomodation
            self.all_unallocated['office'].append(person_name)
            cprint('There are no available Offices at the moment...\n',
                   'red')
            cprint('%s has been added to the waiting list...\n'
                   % person_name, 'magenta')

    def random_living_space(self, person_name):
        """
        Select all living space with allocations less than 4 and
        those that have none at all
        """
        # Check if there are existing living space
        if self.all_rooms['living_space']:
            cprint('Allocating a living Space...\n', 'white')
            available_living_space = []
            for living_space in self.all_rooms['living_space']:
                if len(living_space.occupants) < living_space.space:
                    available_living_space.append(living_space)

            if available_living_space:
                allocated_living_space = random.choice(
                    available_living_space)
                allocated_living_space.occupants.append(person_name)
                cprint("Successful.\n", 'yellow')
            else:
                cprint('There are no available living space at the moment...\n\
                       ', 'red')
                self.all_unallocated['living_space'].append(person_name)
                cprint('%s has been added to the waiting list...\n'
                       % person_name,
                       'magenta')
        else:
            # No accomodation
            self.all_unallocated['living_space'].append(person_name)
            cprint('There are no available Living Space at the moment...\n\
            ', 'red')
            cprint('%s has been added to the waiting list...\n'
                   % person_name, 'magenta')

    def remove_person_from_previous_office_allocations(self, person_name):
        """
            Delete the previous record of office allocations if any
        """
        for room in self.all_rooms['office']:
            for name in room.occupants:
                if name == person_name:
                    room.occupants.remove(person_name)
                    return
                else:
                    continue
        if person_name in self.all_unallocated['office']:
            self.all_unallocated['office'].remove(person_name)

    def remove_person_from_previous_LSpace_allocations(self, person_name):
        """
            Delete the previous record of living_space allocations if any
        """
        for room in self.all_rooms['living_space']:
            for name in room.occupants:
                if name == person_name:
                    room.occupants.remove(person_name)
                    return
                else:
                    continue
        if person_name in self.all_unallocated['living_space']:
            self.all_unallocated['living_space'].remove(person_name)

    def reallocate_a_staff(self, person_name, new_room_name):
        """
            Reallocates a fellow to a new office or new living space
        """
        # Reallocate a person to a new office
        try:
            for room in self.all_rooms['office'] + self.all_rooms[
                 'living_space']:
                if room.name == new_room_name and room.room_type == 'office':
                    for person in room.occupants:
                        if person == person_name:
                            cprint("{} is already allocated in {}...".format(
                                room.name, person), 'red')
                            return
                    if len(room.occupants) < 6:
                        self.remove_person_from_previous_office_allocations(
                            person_name)
                        room.occupants.append(person_name)
                        cprint('%s has been reallocated successfully...'
                               % person_name, 'white')
                        return
                    else:
                        cprint('%s is full. Please pick another room'
                               % room.name, 'red')
                        return
                elif (room.name == new_room_name and room.room_type ==
                      'living_space'):
                    cprint('A Staff can not be allocated a living spaces \
                           ', 'red')
                    return
        except:
            cprint('{} is not an office or it does not exist...'.format(
                new_room_name), 'red')

    def reallocate_a_fellow(self, person_name, new_room_name):
        try:
            for room in self.all_rooms['office'] + self.all_rooms[
                 'living_space']:
                if room.name == new_room_name and room.room_type == 'office':
                    for person in room.occupants:
                        if person == person_name:
                            cprint("{} is already allocated in {}...".format(
                                person, room.name), 'red')
                            return
                    if len(room.occupants) < room.space:
                        self.remove_person_from_previous_office_allocations(
                            person_name)
                        room.occupants.append(person_name)
                        cprint('%s has been reallocated successfully...'
                               % person_name, 'white')
                        return
                    else:
                        cprint('%s is full. Please pick another room'
                               % room.name, 'red')
                        return
                elif (room.name == new_room_name and room.room_type ==
                      'living_space'):
                    for person in room.occupants:
                        if person == person_name:
                            cprint("{} is already allocated in {}...".format(
                                person, room.name), 'red')
                            return
                    if len(room.occupants) < room.space:
                        self.remove_person_from_previous_LSpace_allocations(
                            person_name)
                        room.occupants.append(person_name)
                        cprint('%s has been reallocated successfully...'
                               % person_name, 'white')
                        return
                    else:
                        cprint('%s is full. Please pick another room'
                               % room.name, 'red')
                        return
        except:
            cprint('An error occured', 'red')
            cprint('%s does not exist...' % person_name, 'red')

    def reallocate_person(self, person_name, new_room_name):
        try:
            for person in self.all_persons['staff'] + self.all_persons[
                                        'fellow']:
                if person.name == person_name and person.position == 'fellow':
                    self.reallocate_a_fellow(person_name, new_room_name)
                    break
                elif person.name == person_name and person.position == 'staff':
                    self.reallocate_a_staff(person_name, new_room_name)
                    break
        except:
            cprint('%s does not exist...' % person_name, 'red')
            return

    def print_room(self, room_name):
        """
        Prints all the allocated people in the specified room_name
        if any.
        """
        current_room = None
        for room in self.all_rooms['office'] + self.all_rooms['living_space']:
            if room.name == room_name:
                current_room = room
                break

        if not current_room:
            cprint("Room %s does not exist" % room_name, 'white')
            return

        if current_room.occupants:
            cprint('{} NAME: {} \n'.format(current_room.room_type.upper(),
                   current_room.name), 'white')
            cprint('*'*60, 'cyan')
            cprint(',\t'.join(current_room.occupants),
                   'blue')
            print('\n')
        else:
            cprint("Room %s has no allocations" % current_room.name, 'white')

    def print_all_living_space_allocations(self):
        if self.all_rooms['living_space']:
            # Print all offices and the person names
            # assigned to different room
            cprint('\n...LIVING SPACES...\n', 'cyan')
            for room in self.all_rooms['living_space']:
                self.print_room(room.name)
        else:
            cprint("There are no allocations here at the moment...\n\
            ", 'white')

    def print_all_office_allocations(self):
        if self.all_rooms['office']:
            # Print all offices and the person names
            # assigned to that room
            cprint('\n...OFFICES...\n', 'cyan')
            for room in self.all_rooms['office']:
                self.print_room(room.name)
        else:
            cprint("There are no Offices here at the moment...\n\
            ", 'white')

    def print_all_allocations_into_a_txt_file(self, filename):
        try:
            # Printing into a txt file
            filepath = 'amity/files/' + filename + '.txt'
            output_file = open(filepath, "w")
            print("Printing to %s.txt ...\n\n" % filename)
            output_file.write('\t\t...OFFICE...\n')
            for room in self.all_rooms['office']:
                output_file.write('\n\t' + room.name + '\n' + '-'*80 + '\n')
                if room.occupants:
                    for person in room.occupants:
                        output_file.write(person + ',\t')
                output_file.write('\n')
            output_file.write('\n\n\t\t...LIVING SPACE...\n')
            for room in self.all_rooms['living_space']:
                output_file.write('\n\t' + room.name + '\n' + '-'*80 + '\n')
                if room.occupants:
                    for person in room.occupants:
                        output_file.write(person + ',\t')
                output_file.write('\n')
            output_file.close()
            cprint('\t\t ***Done***', 'white')
        except:
            cprint('An error occurred. Please try again', 'red')

    def print_allocations(self, filename=None):
        """
        Prints all the rooms and the people assigned to them.
        It can display this in a text file ore the screen.
        """
        try:
            if filename:
                self.print_all_allocations_into_a_txt_file(filename)
            else:
                self.print_all_living_space_allocations()
                self.print_all_office_allocations()
        except:
            cprint('An error occured')

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
            output_file.write('\t\t\t \n...OFFICE WAITING LIST...\n')
            for person in self.all_unallocated['office']:
                output_file.write('%s,\t' % person)
            output_file.write('\t\t\t \n\n...LIVING SPACE WAITING LIST...\n')
            for person in self.all_unallocated['living_space']:
                output_file.write('%s,\t' % person)
            output_file.close()
            cprint('%'*60)
            cprint('\n\nDone.', 'white')
        # Print on the screen
        else:
            cprint('\t \t \t...OFFICE...\n', 'white')
            if self.all_unallocated['office']:
                for person in self.all_unallocated['office']:
                    cprint('%s,\t' % person, 'cyan')
            else:
                cprint('\nThere are no unallocated persons at the moment...\n',
                       'red')

            cprint('\t \t \t...Living Space...\n', 'white')
            if self.all_unallocated['living_space']:
                for person in self.all_unallocated['living_space']:
                    cprint('%s,\t' % person, 'cyan')
            else:
                cprint('\nThere are no unallocated persons at the moment...\n',
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
                self.add_person(position, person_name, want_accomodation)
        except:
            cprint('That file does not exist... Please try again.', 'white')

    def save_state(self, db_name=None):
        """
        Persists all the data stored in the app to a SQLite database
        """
        db_name = db_name + '.db' if db_name else 'Amity.db'

        try:
            db_path = 'amity/database/' + db_name
            db = Database(db_path)
            db.create_table()
            cursor = db.cursor()

            # Save all Persons
            if self.all_persons['staff'
                                ] + self.all_persons['fellow']:
                cprint('\t \tSaving all Persons to %s...\n' % db_path, 'cyan')
                for person in self.all_persons['staff'] + self.all_persons[
                        'fellow']:
                    try:
                        cursor.execute(
                            "INSERT INTO employee VALUES (null,?,?);",
                            (person.name, person.position))
                    except sqlite3.IntegrityError:
                        continue
                cprint('\t \tSaved...\n', 'white')
                db.commit()
            else:
                cprint('\t\tThere are no staffs in the System at the moment...\
                \n')

            # Save all Rooms
            if self.all_rooms['office'
                              ] + self.all_rooms['living_space']:
                cprint('\t \tSaving all Rooms to %s...\n' % db_path, 'cyan')
                for room in self.all_rooms['office'] + self.all_rooms[
                        'living_space']:
                    try:
                        cursor.execute(
                            "INSERT INTO room VALUES (null,?,?);",
                            (room.name, room.room_type))
                    except sqlite3.IntegrityError:
                        continue
                cprint('\t \tSaved...\n', 'white')
                db.commit()
            else:
                cprint('\t\tThere are no rooms in the System at the moment...\
                \n', 'red')

            # Save allocations
            if self.all_rooms['office'
                              ] + self.all_rooms['living_space']:
                cprint('\t \tSaving all Rooms to %s...\n' % db_path, 'cyan')
                for room in self.all_rooms['office'
                                           ] + self.all_rooms['living_space']:
                    for person_name in room.occupants:
                        employee_id = cursor.execute(
                            """
                            SELECT employee_id FROM employee WHERE name=?""",
                            (person_name,))
                        for e_id in employee_id:
                            employee_id = e_id[0]
                        room_id = cursor.execute(
                            "SELECT room_id FROM room WHERE name=?",
                            (room.name,))
                        for r_id in room_id:
                            room_id = r_id[0]
                        try:
                            cursor.execute(
                                "INSERT INTO allocation VALUES (null,?,?);",
                                (employee_id, room_id))
                        except sqlite3.IntegrityError:
                            continue
                cprint('\t \tSaved...\n', 'white')
                db.commit()
            else:
                cprint('\t\tThere are no allocations in the System at the moment...\
                \n', 'red')

            # Save all people missing offices
            if self.all_unallocated['office']:
                for person_name in self.all_unallocated['office']:
                    room_type = 'office'
                    employee_id = cursor.execute(
                        "SELECT employee_id FROM employee WHERE name=?",
                        (person_name,))
                    for e_id in employee_id:
                        employee_id = e_id[0]
                    try:
                        cursor.execute(
                            "INSERT INTO unallocated VALUES (null,?,?);",
                            (employee_id, room_type,))
                    except sqlite3.IntegrityError:
                        continue
                cprint('\t \t *Saved successfully...', 'white')
                db.commit()
            else:
                cprint('\t\tOffice waiting list is empty at the moment...\
                    \n', 'red')

            # Save all people missing living space
            if self.all_unallocated['living_space']:
                for person_name in self.all_unallocated['living_space']:
                    room_type = 'living_space'
                    employee_id = cursor.execute(
                        "SELECT employee_id FROM employee WHERE name=?",
                        (person_name,))
                    for e_id in employee_id:
                        employee_id = e_id[0]
                    try:
                        cursor.execute(
                            "INSERT INTO unallocated VALUES (null,?,?);",
                            (employee_id, room_type,))
                    except sqlite3.IntegrityError:
                        continue
                cprint('\t \t *Saved successfully...', 'white')
                db.commit()
            else:
                cprint('\t\tLiving Space is empty at the moment...\
                    \n', 'red')
            db.close_db()
        except:
            cprint('An error occured. Please try again...', 'red')

    def load_all_persons_from_db(self, person_data):
        # Load all employees from the Database
        cprint('Loading Employees...\n', 'white')
        try:
            for row in person_data:
                name = row[0]
                position = row[1]
                if position == 'staff':
                    staff = Staff(name)
                    self.all_persons['staff'].append(staff)
                else:
                    fellow = Fellow(name)
                    self.all_persons['fellow'].append(fellow)
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
                    office = Office(name)
                    self.all_rooms['office'].append(office)
                else:
                    living_space = LivingSpace(name)
                    self.all_rooms['living_space'].append(living_space)
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
                    for room in self.all_rooms['office']:
                        if room.name == room_name:
                            room.occupants.append(employee_name)
                elif room_type == 'living_space':
                    for room in self.all_rooms['living_space']:
                        if room.name == room_name:
                            room.occupants.append(employee_name)
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
                room_type = row[1]
                self.all_unallocated[room_type].append(employee_name)
            cprint('*'*40)
            cprint('\nLoaded successfully...\n', 'white')
        except:
            cprint("Unable to load db. An error occurred.", 'red')

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

    def print_all_person_into_txt_file(self, filename):
        try:
            filepath = 'amity/files/' + filename + '.txt'
            output_file = open(filepath, "w")
            cprint("Printing to %s.txt..." % filename, 'white')
            output_file.write('\t\t...STAFFS...\n')
            for staff in self.all_persons['staff']:
                output_file.write('\n\t' + staff.name + '\n')
            output_file.write('\t\t...FELLOWS...\n')
            for fellow in self.all_persons['fellow']:
                output_file.write('\n\t' + fellow.name + '\n')
            output_file.close()
            cprint('\n\n\t***Done***', 'white')
        except:
            cprint('An error occurred.', 'red')

    def print_all_persons(self, filename=None):
        """
        Prints all the staffs and fellows.
        It can display this in a text file or the screen.
        """
        try:
            # Printing into a txt file
            if filename:
                self.print_all_person_into_txt_file(filename)
            else:
                cprint('...staff...', 'cyan')
                if self.all_persons['staff']:
                    # Print all staffs
                    for staff in self.all_persons['staff']:
                        cprint(''.join(map(str, staff.name)), 'cyan')
                else:
                    cprint("There are no staffs at the moment...", 'white')

                cprint('%'*60, 'white')
                cprint('...Fellow...', 'cyan')
                if self.all_persons['fellow']:
                    # Print all fellows
                    for fellow in self.all_persons['fellow']:
                        cprint(''.join(map(str, fellow.name)), 'cyan')
                else:
                    cprint("There are no fellows at the moment...", 'white')
        except:
            cprint('An error occurred.', 'red')

    def print_all_rooms_into_txt_file(self, filename):
        try:
            filepath = 'amity/files/' + filename + '.txt'
            output_file = open(filepath, "w")
            cprint("Printing to %s.txt..." % filename, 'white')
            output_file.write('\t\t...OFFICE...\n')
            for office in self.all_rooms['office']:
                output_file.write('\n\t' + office.name + '\n')
            output_file.write('\t\t...LIVING SPACE...\n')
            for living_space in self.all_rooms['living_space']:
                output_file.write('\n\t' + living_space.name + '\n')
            output_file.close()
            cprint('\n\n\t***Done***', 'white')
        except:
            print('An error occurred.')

    def print_all_rooms(self, filename=None):
        """
        Prints all the offices and living spaces.
        It can display this in a text file or the screen.
        """
        try:
            # Printing into a txt file
            if filename:
                self.print_all_rooms_into_txt_file(filename)
            else:
                cprint('...OFFICES...', 'cyan')
                if self.all_rooms['office']:
                    # Print all staffs
                    for office in self.all_rooms['office']:
                        cprint(''.join(map(str, office.name)), 'cyan')
                else:
                    cprint("There are no offices at the moment...", 'white')

                cprint('%'*60, 'white')
                cprint('...LIVING SPACES...', 'cyan')
                if self.all_rooms['living_space']:
                    # Print all fellows
                    for living_space in self.all_rooms['living_space']:
                        cprint(''.join(map(str, living_space.name)), 'cyan')
                else:
                    cprint("There are no living_spaces at the moment", 'white')
        except:
            cprint('An error occurred.', 'red')
