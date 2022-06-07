"""
LOGGING:
A way to track events that happen when a program is run.
logging.debug()()()() is the most basic method of doing this by adding it at key points of code and seeing what the output is

"logging" is a built-in module we have to import

LOGGING LEVELS:
DEBUG: Detailed debug, typically of interest only when diagnosing problems
INFO: Confirmation that things are working as expected
WARNING: Indicates something unexpected happened, or indicates some problem will occur in near future (i.e. Disk Space Low) The software is still
         working as expected. Program automatically starts logging/printing at this level and above in urgency
ERROR: Due to a more serious problem, the software has not been able to perform some function
CRITICAL: A serious error, indicating that the program itself may be unable to continue running

"""
import logging
import employee

# Create new logger ::: This will REPLACE the logging.basicConfig() setup :::

logger = logging.getLogger(__name__)
# __name__ changes based on where program is run from, if we run this file itself, __name__ will be equivalent
# to __main__ , if we run this file through an import __name__ will be equivalent to __modulename__

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('test.log')
file_handler.setLevel(logging.ERROR) # Can change level for file only, so it will only print things to file if ERROR, logger still logs DEBUG though
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler() # Displays the logged error in console as well as printing it to file
stream_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# We can comment out the default logger config since we won't be using it anymore
# Set the log to output to a file named "test", it will keep a record of all occurrences of logging level
#logging.basicConfig(filename='test.log',
#                    level=logging.DEBUG, # Changing the level of logging to DEBUG instead of default value:WARNING
#                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s') # Adding format will change the way the logs are displayed in file


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
    try:
        result = x / y
    except ZeroDivisionError:
        #logger.error('Tried to divide by zero')  only logs the Error msg
        logger.exception('Tried to divide by zero') # logs the Traceback of Error
    else:
        return result


num_1 = 20
num_2 = 0

add_result = add(num_1, num_2)
logger.debug(f"Add: {num_1} + {num_2} = {add_result}")

sub_result = subtract(num_1, num_2)
logger.debug(f"Add: {num_1} - {num_2} = {sub_result}")

mul_result = multiply(num_1, num_2)
logger.debug(f"Add: {num_1} * {num_2} = {mul_result}")

div_result = divide(num_1, num_2)
logger.debug(f"Add: {num_1} / {num_2} = {div_result}")

