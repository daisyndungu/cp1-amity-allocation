class Room:
    def __init__(self, name, room_type, space):
        self.space = space
        self.name = name
        self.room_type = room_type
        self.occupants = []


class Living_Space(Room):
    def __init__(self, room_name):
        super(Room, self).__init__(room_name, 'living_space', space=4)


class Office(Room):
    def __init__(self, room_name):
        super(Room, self).__init__(room_name, 'office', space=6)
