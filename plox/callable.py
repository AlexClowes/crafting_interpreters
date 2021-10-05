from abc import ABC, abstractmethod
import time

from .environment import Environment


class Return(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Callable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass


class Function(Callable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for param, arg in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, arg)
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as ret:
            return ret.value

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
