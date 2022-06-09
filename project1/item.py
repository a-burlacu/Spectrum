import csv


# Create parent class
class Item:
    pay_rate = 0.8  # The pay rate after 20% discount
    all = []
    result = 0

    def __init__(self, name: str, price: float, quantity=0):  # Default constructor
        # Run validations on received arguments
        assert price >= 0, f"Price {price} is not greater than or equal to zero."
        assert quantity >= 0, f"Quantity {quantity} is not greater than or equal to zero."

        # Assign to self object
        self.__name = name  # use _ in front of name since it is a read-only attribute, using __ makes it private
        self.__price = price
        self.quantity = quantity

        # Actions to execute
        Item.all.append(self)  # Add instance to list every time it creates new instance

    @property  # restrict access to price attribute
    def price(self):
        return self.__price

    def apply_discount(self):
        self.__price = self.__price * self.pay_rate

    def apply_increment(self, increment_value):
        self.__price = self.__price + self.__price * increment_value

    @property
    # Property Decorator = Read-Only Attribute
    def name(self):
        return self.__name

    @name.setter  # Setter allows changing read-only attribute __name
    def name(self, value):
        if len(value) > 10:  # set length limit for instance name
            raise Exception("The name is too long!")
        else:
            self.__name = value

    def calculate_total_price(self):
        return self.__price * self.quantity

    @classmethod  # @Decorator calls the function right before fx definition, used to change type of fx
    def instantiate_from_csv(cls):  # Class object is passed as argument to class method
        with open('items.csv', 'r') as f:  # Open file and read it
            reader = csv.DictReader(f)  # Read file as a dictionary
            items = list(reader)  # Convert dictionary to list

        for item in items:  # for loop to iterate over each item in list
            Item(  # creates new instance of Item class and assigns values to args using .get
                name=item.get('name'),
                price=float(item.get('price')),
                quantity=int(item.get('quantity')),
            )

    # Create a static method that checks if number is an integer or not
    @staticmethod  # Difference between @classmethod and @staticmethod is object is not passed to args in static
    def is_integer(num):  # static method acts like a regular function definition
        # We will not count floats that are point zero (i.e. 5.0, 10.0)
        if isinstance(num, float):
            return num.is_integer()
        elif isinstance(num, int):
            return True
        else:
            return False

    def __repr__(self):  # method that represents each instance in class
        return f"{self.__class__.__name__}('{self.name}', {self.__price}, {self.quantity})"
        # self.__class__.__name__ references the specific class instance name like Phone, etc

    # Principle of Abstraction: send_email  is only method called in main fx, but it uses 3 more methods to execute
    # however, the user does not know/see this process as it is behind the scenes
    # using __ makes methods private, so only class method can access, user cannot
    def __connect(self, smtp_server):
        pass

    def __prepare_body(self):
        return f"""
        Hello Someone.
        We have {self.name} {self.quantity} times.
        Regards.
        """

    def __send(self):
        pass

    def send_email(self):
        self.__connect('')
        self.__prepare_body()
        self.__send()
