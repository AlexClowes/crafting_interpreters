from abc import ABC, abstractmethod
import time

from .environment import Environment


class Callable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass


class Function(Callable):
    def __init__(self, declaration):
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)
        interpreter.execute_block(self.declaration.body, environment)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"


class Clock(Callable):
    @staticmethod
    def arity():
        return 0

    @staticmethod
    def call(interpreter, arguments):
        return time.time()

    @staticmethod
    def __str__():
        return "<native fn>"
