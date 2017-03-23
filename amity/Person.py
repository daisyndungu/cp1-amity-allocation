
class Person(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Staff(Person):
    def __init__(self, person_name):
        super(Staff, self).__init__(person_name, 'staff')


class Fellow(Person):
    def __init__(self, person_name):
        super(Staff, self).__init__(person_name, 'fellow')
