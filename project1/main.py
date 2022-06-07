from item import Item
from phone import Phone
from keyboard import Keyboard

"""
Encapsulation, restricting user inputs so they cannot override variable values
"""
# item1 = Item("MyItem", 750)
# item1.apply_increment(0.2)
# # Modified price attribute using method apply_increment
# print(item1.price)


# item1.__name = "OtherItem"  # Does not execute, using __ in front of var name is like using "private": read-only
# print(item1.name)  # Prints "MyItem" not "OtherItem"

# After using setter decorator, we can change the name again, even if it's read-only
# item1.name = "OtherItem"
# print(item1.name)


"""
Abstraction, removing unnecessary information, making process simpler, doing things "behind the scenes"
"""
# item1 = Item("MyItem", 750, 6)
# item1.send_email()
#
# item1.connect() # User cannot access private methods

"""
Inheritance, mechanism that allows us to reuse code across multiple classes
"""
# using class methods and attributes of one class to create an instance of a subclass
# methods of Item class can be applied to instance of Phone child class

# item1 = Phone("jscPhone", 1000, 3)
# item1.apply_increment(0.2)
# print(item1.price)



"""
Polymorphism, the ability to have different outcomes when invoking the same function/method
ex:
    name = "Jim" #str
    print(len(name))
    some_list = ["some", "name"] #list
    print(len(some_list))

# A single function (len) handles different types of variables differently, in strings it counts number of characters
# in lists, it counts number of items the list contains
"""

item1 = Phone("jscPhone", 1000, 3)
item1.apply_discount()
print(item1.price)

# same function has different outcome for phone and keyboard objects

item2 = Keyboard("jscKeyboard", 1000, 3)
item2.apply_discount()
print(item2.price)