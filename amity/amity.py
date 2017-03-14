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
