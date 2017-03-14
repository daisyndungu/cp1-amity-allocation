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

    