# **Abstraction**
___
>Removing unnecessary information, making process simpler, doing things "behind the scenes"

EX:
```python
// main.py //
from class_name import ClassName

object1 = ClassName("var1", var2) 
object1.doSomeTask()


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
```python
// main.py //
from class_name import ClassName

object1 = ClassName("name", value)
object1.doSomething(input_value)



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
        print(result)
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
```python
// main.py //
from child import Child     # Notice we only need to import the child file

child1 = Child("name", var1)
child1.doSomething()



// child.py //              # The child file imports the parent file
from parent import Parent

class Child(Parent):
    def __init__(self, name: str, var1: int):
    
        super().__init__(name, var1)      # The super() function allows child class to access all attributes/methods of parent
        *additional attributes/methods     # Child class can still have its own declared attributes



// parent.py //
class Parent:
    result = 0
    def __init__(self, name: str, var1: int):
        self.name = name
        self.var1 = var1

    def doSomething(self, input_value):
        result = self.var1 + input_value
        print(result)
```
Here there is another file containing the `Child` subclass of the `Parent` superclass. 

In the main function, an object of type `Child` is instantiated, however, the class method `doSomething()` is then called on the object, `child1`. 

The subclass, `Child` is able to access all of the `Parent` class' attributes & methods using the `super()` method contained in
the constructor of the `Child` class. 


# **Polymorphism**
___
>The ability to have different outcomes when invoking the same function. This is useful when there are multiple classes with
> methods of the same name, that have different outputs. 
> 
> A built-in example of a polymorphic function is the `len()` function. It handles different data types in different ways. 
>When used on a string, it counts the number of characters. In lists, it counts the number of items contained. 

EX:
```python
// main.py //
from child import Child
from parent import Parent  # We need to include this since we are creating Parent object

child1 = Child("na", 4)
child1.doSomething(2)

parent1 = Parent("la", 4)
parent1.doSomething(2)


// child.py //              
from parent import Parent

class Child(Parent):

    def __init__(self, name: str, var1: int):
        super().__init__(name, var1)

    def doSomething(self, input_value):
        result = self.var1 * input_value      # This method multiplies in the Child class, but adds in the Parent class
        print(result)


// parent.py //
class Parent:
    result = 0
    def __init__(self, name: str, var1: int):
        self.name = name
        self.var1 = var1

    def doSomething(self, input_value):
        result = self.var1 + input_value
        print(result)

```
In the main function, there are 2 objects created: one `Child` object, and one `Parent` object. 
They both have `var1 = 4` and `input_value = 2` however, their outputs will be different. 

The `Child` class contains the same method, `doSomething()` but instead of addition, it's multiplication. 

When printing the results, for the `child1` object, the output should be `8`. The output of the `parent1` object should be `6`.





