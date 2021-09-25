import expr
from tokens import Token, TokenType


class ASTPrinter:
    def print(self, expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs):
        return "(" + name + " " + " ".join(map(self.print, exprs)) + ")"

    def visit_binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr):
        return str(expr.value) if expr.value is not None else "nil"

    def visit_unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)


def main():
    expression = expr.Binary(
        expr.Unary(Token(TokenType.MINUS, "-", None, 1), expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        expr.Grouping(expr.Literal(45.67)),
    )
    print(ASTPrinter().print(expression))


if __name__ == "__main__":
    main()
