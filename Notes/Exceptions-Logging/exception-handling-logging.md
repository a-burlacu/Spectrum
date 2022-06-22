# **Errors/Exceptions**
___
> Errors and exceptions are nearly synonymous. 
> 
> An **Error** can be identified & corrected during compile time. There are **syntax errors** or **exceptions**.
> 
> An **Exception** can only be identified during runtime and can be handled with `try` and `except` statements.
> This allows for exceptions to be thrown without crashing the program. 

## - Built-in Exceptions
Python already contains a lot of built-in exception types, for common issues like dividing by zero `ZeroDivisionError`,
entering the wrong data type `TypeError`, or trying to import a missing file `FileNotFoundError`.

Other common built-in exceptions:

 `ValueError` `AssertionError` `KeyboardInterrupt` `OverflowError` `RuntimeError` `OverflowError`

A full list of built-in exceptions can be found [HERE](https://docs.python.org/3.9/library/exceptions.html#exception-hierarchy).

## - User-defined Exceptions
It can be useful to create custom exception types, such as for a game or other user-interactive program. 

To create a user-defined exception:
- Create a new class derived from the built-in `Exception` class
  - Then you can create subclasses for other errors derived from your own error

EX:
```python
// exception.py //

class MyError(Exception):
    * custom base class for other errors *
    pass

class MySubError(MyError):
    * custom derived error class *
    pass


# using a try-except block for exception handling
while True:
    try:
        function()
        raise MySubError ("Exception occured")
        
    except MyError as err:
        print("There was an error")
```
Here we created two custom exception classes. 

In the `try-except` block we used the `raise` statement to force the specified exception to occur.
This doesn't mean there was an error necessarily. It could just be a way to clarify incorrect input in a function or similar. 

# **Logging**
___
> Logging is a way to track events that happen when a program runs. 
> A similar way to do this is by using the `print()` statement. 
> However, logs allow us to track multiple runs of a program as well as to save the log in a file.
> 
> This allows us to look at behavior and errors over time to improve debugging methods.

## - Logging Levels

The `logging` module is already built-in to Python, so it is easy to implement in a program by using:
`import logging` at the top of a file.

There are **5 Logging Levels** that correspond to functions of the same name.

| **Level Name** | **Function Syntax** | **Description**                                              |
| -------------- | ------------------- | ------------------------------------------------------------ |
| DEBUG          | logging.debug()     | Detailed info, used when diagnosing issues                   |
| INFO           | logging.info()      | Confirmation that things are operating normally              |
| WARNING        | logging.warning()   | Indicates unexpected occurrence, or developing issue,<br/> program still functions normally |
| ERROR          | logging.error()     | A more serious issue, program has not been able to <br/>perform a function, reports error without raising exception |
| CRITICAL       | logging.critical()  | Serious error, program may be unable to continue running     |

