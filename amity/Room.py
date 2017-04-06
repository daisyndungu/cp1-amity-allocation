from abc import ABCMeta


class Room:
    __metaclass__ = ABCMeta

    def __init__(self, name, room_type, space):
        self.space = space
        self.name = name
        self.room_type = room_type
        self.occupants = []

    def __repr__(self):
        return self.name


class LivingSpace(Room):
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name, 'living_space', 4)


class Office(Room):
    def __init__(self, room_name):
        super(Office, self).__init__(room_name, 'office', 6)
