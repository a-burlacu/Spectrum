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


