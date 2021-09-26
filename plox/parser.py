from . import expr
from . import lox
from .tokens import TokenType


class ParseError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return

    def expression(self):
        return self.equality()

    def equality(self):
        return self.left_associative_binary_series(
            self.comparison, (TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)
        )

    def comparison(self):
        return self.left_associative_binary_series(
            self.term,
            (
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ),
        )

    def term(self):
        return self.left_associative_binary_series(
            self.factor, (TokenType.MINUS, TokenType.PLUS)
        )

    def factor(self):
        return self.left_associative_binary_series(
            self.unary, (TokenType.SLASH, TokenType.STAR)
        )

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return expr.Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return expr.Literal(False)
        if self.match(TokenType.TRUE):
            return expr.Literal(True)
        if self.match(TokenType.NIL):
            return expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return expr.Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr.Grouping(expression)
        raise self.error(self.peek(), "Expect expression.")

    def left_associative_binary_series(self, unit, operator_types):
        expression = unit()
        while self.match(*operator_types):
            operator = self.previous()
            right = unit()
            expression = expr.Binary(expression, operator, right)
        return expression

    def match(self, *types):
        if any(map(self.check, types)):
            self.advance()
            return True
        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, type):
        return not self.is_at_end() and self.peek().type is type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type is TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    @staticmethod
    def error(token, message):
        lox.parse_error(token, message)
        return ParseError

    def synchronize(self):
        self.advance()
        while (
            not self.is_at_end()
            and self.previous().type is not TokenType.SEMICOLON
            and self.peek().type not in (
                TokenType.CLASS,
                TokenType.FOR,
                TokenType.FUN,
                TokenType.IF,
                TokenType.PRINT,
                TokenType.RETURN,
                TokenType.VAR,
                TokenType.WHILE,
            )
        ):
            self.advance()
