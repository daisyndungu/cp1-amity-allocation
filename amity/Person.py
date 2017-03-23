
class Person(object):
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name, 'staff')


class Fellow(Person):
    def __init__(self, name, want_accomodation='N'):
        super(Fellow, self).__init__(name, 'fellow')
        self.want_accomodation = want_accomodation
