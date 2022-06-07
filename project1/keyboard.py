from item import Item

# Create child class
class Keyboard(Item):
    pay_rate = 0.7
    def __init__(self, name: str, price: float, quantity=0):  # Default constructor
        # Call to super function to have access to all attributes/methods
        super().__init__(
            name, price, quantity
        )
