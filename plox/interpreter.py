from numbers import Number

from .callable import Callable, Clock
from .environment import Environment
from . import lox
from .tokens import TokenType


class RuntimeException(RuntimeError):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token


class Interpreter:
    def __init__(self):
        self.environment = self.globals = Environment()
        self.globals.define("clock", Clock())

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeException as exc:
            lox.runtime_error(exc)

    def execute(self, stmt):
        stmt.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression(self, stmt):
        self.evaluate(stmt.expression)

    def visit_if(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_while(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_assign(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op_type = expr.operator.type
        if op_type is TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if op_type is TokenType.PLUS:
            if isinstance(left, Number) and isinstance(right, Number):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeException(
                expr.operator, "Operands must be two numbers or two strings."
            )
        if op_type is TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            if right == 0:
                raise RuntimeException(
                    expr.operator, "Division by zero"
                )
            return float(left) / float(right)
        if op_type is TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        if op_type is TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if op_type is TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if op_type is TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if op_type is TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        if op_type is TokenType.EQUAL:
            return left == right
        if op_type is TokenType.BANG_EQUAL:
            return left != right

    def visit_call(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(argument) for argument in expr.arguments]
        if not isinstance(callee, Callable):
            raise RuntimeException(expr.paren, "Can only call functions and classes.")
        if len(arguments) != callee.arity():
            raise RuntimeException(
                expr.paren,
                f"Expected {callee.arity()} arguments but got {len(arguments)}.",
            )
        return callee.call(self, arguments)

    def visit_grouping(self, expr):
        return self.evaluate(expr.expression)

    @staticmethod
    def visit_literal(expr):
        return expr.value

    def visit_logical(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type is TokenType.OR:
            if self.is_truthy(left):
                return left
        elif not self.is_truthy(left):
            return left
        return self.evaluate(expr.right)

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)
        op_type = expr.operator.type
        if op_type is TokenType.MINUS:
            self.check_number_operands(expr.operator, right)
            return -float(right)
        if op_type is TokenType.BANG:
            return not self.is_truthy(right)

    def visit_variable(self, expr):
        return self.environment.get(expr.name)

    @staticmethod
    def check_number_operands(operator, *operands):
        if any(not isinstance(operand, Number) for operand in operands):
            raise RuntimeException(operator, "Operand must be a number.")

    @staticmethod
    def is_truthy(obj):
        return obj not in (None, False)

    @staticmethod
    def stringify(value):
        if value is None:
            return "nil"
        if isinstance(value, Number):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)
