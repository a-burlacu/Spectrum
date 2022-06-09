from parent import Parent

class Child(Parent):
    def __init__(self, name: str, var1: int):
        super().__init__(name, var1)

