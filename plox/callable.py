from abc import ABC, abstractmethod
import time


class Callable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass


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
