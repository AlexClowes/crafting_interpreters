import lox
from tokens import Token, TokenType


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            # We are at the beginning of the next lexeme
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            token = TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            self.add_token(token)
        elif c == "=":
            token = TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            self.add_token(token)
        elif c == "<":
            token = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            self.add_token(token)
        elif c == ">":
            token = TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            self.add_token(token)
        else:
            lox.error(self.line, "Unexpected character")

    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        ret = self.source[self.current]
        self.current += 1
        return ret

    def add_token(self, type, literal=None):
        self.tokens.append(
            Token(type, self.source[self.start : self.current], literal, self.line)
        )
