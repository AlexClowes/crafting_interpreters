from .callable import Callable
from . import interpreter


class LoxClass(Callable):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __str__(self):
        return self.name

    def arity(self):
        if initializer := self.find_method("init"):
            return initializer.arity()
        return 0

    def call(self, interpreter, arguments):
        instance = Instance(self)
        if initializer := self.find_method("init"):
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def find_method(self, name):
        return self.methods.get(name)


class Instance:
    def __init__(self, class_):
        self.class_ = class_
        self.fields = {}

    def __str__(self):
        return f"{self.class_.name} instance"

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        if method := self.class_.find_method(name.lexeme):
            return method.bind(self)
        raise interpreter.RuntimeException(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value
