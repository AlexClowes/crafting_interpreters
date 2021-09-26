from numbers import Number

from tokens import TokenType


class Interpreter:
    def evaluate(self, expr):
        return expr.accept(self)

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op_type = expr.operator.type
        if op_type is TokenType.MINUS:
            return float(left) - float(right)
        if op_type is TokenType.PLUS:
            if isinstance(left, Number) and isinstance(right, Number):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        if op_type is TokenType.SLASH:
            return float(left) / float(right)
        if op_type is TokenType.STAR:
            return float(left) * float(right)
        if op_type is TokenType.GREATER:
            return float(left) > float(right)
        if op_type is TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        if op_type is TokenType.LESS:
            return float(left) < float(right)
        if op_type is TokenType.LESS_EQUAL:
            return float(left) <= float(right)
        if op_type is TokenType.EQUAL:
            return left == right
        if op_type is TokenType.BANG_EQUAL:
            return left != right

    def visit_grouping(self, expr):
        return self.evaluate(expr.expression)

    @staticmethod
    def visit_literal(expr):
        return expr.value

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)
        op_type = expr.operator.type
        if op_type is TokenType.MINUS:
            return -float(right)
        if op_type is TokenType.BANG:
            return not self.is_truthy(right)

    @staticmethod
    def is_truthy(obj):
        return obj not in (None, False)
