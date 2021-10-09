from .callable import Callable


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

    def __str__(self):
        return f"{self.class_.name} instance"
