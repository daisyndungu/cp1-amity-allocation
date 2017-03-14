class Amity(object):
    all_persons = {
        'staffs': ['Daisy Wanjiru'],
        'fellows': ['Maureen Wangui']
        }
    all_allocations = {
        'office': {
            'camelot': []
            },
        'living_space': {
            'php': []
        }
        }
    all_unallocated = []
    all_rooms = {
        'living_space': ['topaz'],
        'office': ['hogwarts', 'camelot']
        }

    def __init__(self):
        self.list_length = 0
        self.person_identifier = []
        self.new_room_name = ''
        self.room_type = ''
        self.room_names = []

    def create_room(room_type, *room_names):
        if room_type == 'o' or room_type == 'O':
            for room_name in room_names:
                if room_name in self.all_rooms['office']:
                    print("!!!!!!........%s room already exists.........!!!!!!" % room_name)
                else:
                    self.all_rooms = self.all_rooms['office'].append(room_name)
                    print("<<........An Office: %s has been created.........>>" % room_name)

        elif room_type == 'l' or room_type == 'l':
            for room_name in room_names:
                if room_name in self.all_rooms['living_space']:
                    print("!!!!!!........%s already exists.........!!!!!!" % room_name)
                else:
                    self.all_rooms['living_space'].append(room_name)
                    print("<<........A Living Space: %s has been created.........>>"% room_name)
            print(self.all_rooms['living_space'])
        else:
            print("invalid input. Type should be 'o' for office(s) or 'l' for living_space(s)")

    def add_person(position, *person_name, **want_accomodation):
            person_name = input("Enter a persons name: ")
            position = input("Enter their position (S/F): ")
            wants_accomodation = input("Want accomodation  (Y/N): ")

            # Adding a staff and allocating them an office space
            if position == 's' or position == 'S' and want_accomodation == 'n':
                if person_name in self.all_persons['staffs']:
                    print("!!!!!!........Staff: %s already exists.........!!!!!!" % person_name)
                else:
                    self.all_persons['staffs'].append(person_name)
                    print("<<........Staff: %s has been added .........>>" % person_name)
                    # Allocating fellow an office
                    allocated_office_name = random.choice(self.all_rooms['office'])
                    if allocated_office_name in self.all_allocations['office'] and len(self.all_allocations['office'][allocated_office_name]) < 6:
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                        print(all_allocations['office'])
                    else:
                        self.all_allocations['office'][allocated_office_name] = []
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                    print("All allocations: Offices: ", self.all_allocations['office'])
                    print("All Staffs: ", self.all_persons['staffs'])

            # Adding a fellow and allocating an office space but deny them a living space
            elif position == 's' or position == 'S' and want_accomodation == 'y':
                if person_name in self.all_persons['staffs']:
                    print("!!!!!!........Staff: %s already exists.........!!!!!!" % person_name)
                else:
                    self.all_persons['staffs'].append(person_name)
                    print("<<........Staff: %s has been added .........>>" % person_name)
                    # Allocating fellow an office
                    allocated_office_name = random.choice(self.all_rooms['office'])
                    if allocated_office_name in self.all_allocations['office'] and len(self.all_allocations['office'][allocated_office_name]) < 6:
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                        print(all_allocations['office'])
                    else:
                        self.all_allocations['office'][allocated_office_name] = []
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                    print("!!!!!!!!............Staff can not be allocated a Living Space...........!!!!!!!!!!!!")
                    print("All allocations: Offices: ", self.all_allocations['office'])
                    print("All Staffs: ", self.all_persons['staffs'])

            # Adding a fellow and allocating them a living space and an office space
            elif position == 'f' or position == 'F' and want_accomodation == 'y':
                if person_name in self.all_persons['fellows']:
                    print("!!!!!!........Fellow: %s already exists.........!!!!!!" % person_name)
                else:
                    self.all_persons['fellows'].append(person_name)
                    print("<<........Fellow: %s has been added .........>>" % person_name)
                    # Allocating fellow an office
                    allocated_office_name = random.choice(self.all_rooms['office'])
                    if allocated_office_name in self.all_allocations['office'] and len(self.all_allocations['office'][allocated_office_name]) < 6:
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                        print(all_allocations['office'])
                    else:
                        self.all_allocations['office'][allocated_office_name] = []
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                    # Allocating fellow a living space
                    allocated_living_space_name = random.choice(self.all_rooms['living_space'])
                    if allocated_living_space_name in self.all_allocations['living_space'] and len(self.all_allocations['living_space'][allocated_living_space_name]) < 4:
                        self.all_allocations['living_space'][allocated_living_space_name].append(person_name)
                        print(all_allocations['living_space'])
                    else:
                        self.all_allocations['living_space'][allocated_living_space_name] = []
                        self.all_allocations['living_space'][allocated_living_space_name].append(person_name)
                    print("All allocations: Living_space: ", self.all_allocations['living_space'])
                    print(self.all_persons['fellows'])

            # Adding a fellow and allocating them an office space only
            elif position == 'f' or position == 'F' and want_accomodation == 'n':
                if person_name in self.all_persons['fellows']:
                    print("!!!!!!........Fellow: %s already exists.........!!!!!!" % person_name)
                else:
                    self.all_persons['fellows'].append(person_name)
                    print("<<........Fellow: %s has been added .........>>" % person_name)
                    # Allocating fellow an office
                    allocated_office_name = random.choice(self.all_rooms['office'])
                    if allocated_office_name in self.all_allocations['office'] and len(self.all_allocations['office'][allocated_office_name]) < 6:
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                        print(all_allocations['office'])
                    else:
                        self.all_allocations['office'][allocated_office_name] = []
                        self.all_allocations['office'][allocated_office_name].append(person_name)
                    print("All allocations: Offices: ", self.all_allocations['office'])
                    print("All Staffs: ", self.all_persons['staffs'])

            else:
                print("Invalid Input")

    def print_room(self):
        room_name = input("Enter room name: ")
        if room_name in self.all_rooms['office']:
            if room_name in self.all_allocations['office']:
                print(self.all_allocations['office'][room_name])
            else:
                print("Room %s has not allocations" % room_name)

        elif room_name in self.all_rooms['living_space']:
            if room_name in self.all_allocations['living_space']:
                print(self.all_allocations['living_space'][room_name])
            else:
                print("Room %s has not allocations" % room_name)
        else:
            print("Room %s does not exist" % room_name)
