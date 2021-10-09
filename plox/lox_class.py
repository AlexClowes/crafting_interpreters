from .callable import Callable
from . import interpreter


class LoxClass(Callable):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return Instance(self)


class Instance:
    def __init__(self, class_):
        self.class_ = class_
        self.fields = {}

    def __str__(self):
        return f"{self.class_.name} instance"

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        raise interpreter.RuntimeException(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value
