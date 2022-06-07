import logging

# Create new logger ::: This will REPLACE the logging.basicConfig() setup :::
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('employee.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# We can comment out the default logger config since we won't be using it anymore
#logging.basicConfig(filename='employee.log', level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

class Employee:
    # A sample Employee class

    def __init__(self, first, last):
        self.first = first
        self.last = last

        logger.info(f'Created Employee: {self.fullname} - {self.email}')
        # Make sure to change 'logging' to 'logger' since we are using a new logger to run INFO method

    @property
    def email(self):
        return f'{self.first}.{self.last}'

    @property
    def fullname(self):
        return f'{self.first} {self.last}'


emp1 = Employee('John', 'Smith')
emp2 = Employee('Alina', 'Burlacu')
emp3 = Employee('Jane', 'Doe')

