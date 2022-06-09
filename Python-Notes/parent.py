class Parent:
    result = 0
    def __init__(self, name: str, var1: int):
        self.name = name
        self.var1 = var1

    def doSomething(self, input_value):
        result = self.var1 + input_value
        print(result)
