"""
LOGGING:
A way to track events that happen when a program is run.
logging.debug()()() is the most basic method of doing this by adding it at key points of code and seeing what the output is

"logging" is a built-in module we have to import

LOGGING LEVELS:
DEBUG: Detailed info, typically of interest only when diagnosing problems
INFO: Confirmation that things are working as expected
WARNING: Indicates something unexpected happened, or indicates some problem will occur in near future (i.e. Disk Space Low) The software is still
         working as expected. Program automatically starts logging/printing at this level and above in urgency
ERROR: Due to a more serious problem, the software has not been able to perform some function
CRITICAL: A serious error, indicating that the program itself may be unable to continue running

"""
import logging

# Set the log to output to a file named "test", it will keep a record of all occurrences of logging level
# Changing the level of logging to DEBUG instead of default value:WARNING
# Adding format will change the way the logs are displayed in file
logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def add (x, y):
    #Add function
    return x + y

def subtract(x, y):
    # Subtract function
    return x - y

def multiply(x, y):
    # Multiply function
    return x * y

def divide(x, y):
    # Divide function
    return x / y

num_1 = 20
num_2 = 10

add_result = add(num_1, num_2)
logging.debug(f"Add: {num_1} + {num_2} = {add_result}")

sub_result = subtract(num_1, num_2)
logging.debug(f"Add: {num_1} - {num_2} = {sub_result}")

mul_result = multiply(num_1, num_2)
logging.debug(f"Add: {num_1} * {num_2} = {mul_result}")

div_result = divide(num_1, num_2)
logging.debug(f"Add: {num_1} / {num_2} = {div_result}")

