import logging


logging.basicConfig(filename='employee.log', level=logging.INFO, format='%(levelname)s:%(message)s')

class Employee:
    # A sample Employee class

    def __init__(self, first, last):
        self.first = first
        self.last = last

        logging.info(f'Created Employee: {self.fullname} - {self.email}')


    @property
    def email(self):
        return f'{self.first}.{self.last}'

    @property
    def fullname(self):
        return f'{self.first} {self.last}'


emp1 = Employee('John', 'Smith')
emp2 = Employee('Alina', 'Burlacu')
emp3 = Employee('Jane', 'Doe')

