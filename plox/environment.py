from . import interpreter


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        try:
            return self.values[name.lexeme]
        except KeyError:
            raise interpreter.RuntimeException(name, f"Undefined variable {name.lexeme}.")
