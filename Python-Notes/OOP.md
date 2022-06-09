# **Abstraction**
___
>Removing unnecessary information, making process simpler, doing things "behind the scenes"

EX:
```
// main.py //
from class_name import ClassName

object = ClassName("var1", var2) 
object.doSomeTask()


// class_name.py//
class ClassName:
    def __init__(self, var1: str, var2: int):  # This is the class constructor
        self.var1 = var1
        self.var2 = var2
        
        
    def firstTask(self):
        * some funciton defitinion*
        return result
    
    def secondTask(self, result):
        * some function definition*
        
    def doSomeTask(self):
        self.firstTask()
        self.secondTask('result')
        return taskdone
```
Here, the class method called in the main function, `doSomeTask()` uses two other methods the user doesn't know about in order to execute itself.

# **Encapsulation**
___
>"Information hiding", or restricting user access to variables or methods by 
> bundling them together into a class or function definition which is inaccessible to the user.

EX: 
```
// main.py //
from class_name import ClassName

object = ClassName("name", value)
object.doSomething(input_value)

print(object.result)


// class_name.py//

class ClassName:
    result = 0              # Initialized variable 
    def __init__(self, name: str, value: int):
        self.name = name
        self.__value = value  # __ indicates a PRIVATE variable

    @property                 # A setter function for the value variable
    def value(self):
      return self.__value

    def doSomething(self, input_value):
        result = self.__value + input_value
        return result
```
Here we have the function `doSomething` called by the user in main. The function accepts some parameter, _input_. 
The user then requests the result value of the instance, _object_, to be displayed. 

Under the `ClassName` definition, we have a **private variable** `self.__value` which the user cannot access again after the value is set. This 
prevents changing values and affecting the overall outcome of the program. 

The `@property` decorator acts as a **"setter"** and calls the function below it: `value(self)` 
to set the value of the private variable `self.__value`.


The function called by the user, `doSomething`, then is able to access the `__value` and perform the function using the user's _input_. 
The function then sets the attribute `self.result` to equal the new value. 

When the user prints the value of `object.result` they are displaying this new value.

# **Inheritance**
___
>Re-using attributes or methods by creating subclasses (or child classes) and _inheriting_ values from the parent class. 
> This cuts down code repetition. 

EX:
```
// main.py //
from child import Child     # Notice we only need to import the child file

object = Child("name", var1, var2)
object.doSomething()

print(object.result)


// child.py //              # The child file imports the parent file
from parent import Parent

class Child(Parent):
    def __init__(self, name: str, var1: int):
    
        super().__init__(name, var1)      # The super() function allows child class to access all attributes/methods of parent
        *additional attributes/method     # Child class can still have its own declared attributes


// parent.py //
class Parent:
    def __init__(self, name: str, var1: int):
        self.name = name
        self.value = value 
       

    def doSomething(self, input_value):
        self.result = self.__value + input_value











