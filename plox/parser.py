from . import expr
from . import lox
from . import stmt
from .tokens import TokenType


class ParseError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = self.expression() if self.match(TokenType.EQUAL) else None
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return stmt.Var(name, initializer)

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def expression_statement(self):
        expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return stmt.Expression(expression)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expression = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expression, expr.Variable):
                name = expression.name
                return expr.Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expression

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
        if self.match(TokenType.IDENTIFIER):
            return expr.Variable(self.previous())
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
