# When to use class methods and when to use static methods?

class Item:
    @staticmethod
    def is_integer(num):
        """
        A "general" method that doesn't involve class objects.
        This should do something that has a relationship with the class,
        but not something that must be unique per instance!
        """

    @classmethod
    def instantiate_from_something(cls): # cls is a mandatory parameter of instance type
        """
        A "specific" method for objects of class, usually used from a data file.
        This should also do something that has a relationship with the class,
        but usually, those are used to manipulate different structures of data
        to instantiate objects, like we have done with CSV
        """