from parent import Parent


class Child(Parent):

    def __init__(self, name: str, var1: int):
        super().__init__(name, var1)

    def doSomething(self, input_value):
        result = self.var1 * input_value      # This method multiplies in the Child class, but adds in the Parent class
        print(result)
