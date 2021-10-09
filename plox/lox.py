import sys

from .interpreter import Interpreter
from .parser import Parser
from .resolver import Resolver
from .scanner import Scanner
from .tokens import TokenType


HAD_ERROR = False
HAD_RUNTIME_ERROR = False

INTERPRETER = Interpreter()


def error(line, message):
    report(line, "", message)


def parse_error(token, message):
    if token.type is TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)


def runtime_error(exception):
    print(f"{exception}\n[line {exception.token.line}]")
    global HAD_RUNTIME_ERROR
    HAD_RUNTIME_ERROR = True


def report(line, where, message):
    print(f"[line {line}] Error{where}: {message}")
    global HAD_ERROR
    HAD_ERROR = True


def run(source):
    tokens = Scanner(source).scan_tokens()
    statements = Parser(tokens).parse()
    if not HAD_ERROR:
        Resolver(INTERPRETER).resolve(*statements)
        INTERPRETER.interpret(statements)


def run_file(path):
    with open(path) as f:
        run(f.read())
    if HAD_ERROR:
        sys.exit(65)
    if HAD_RUNTIME_ERROR:
        sys.exit(70)


def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)
        global HAD_ERROR
        HAD_ERROR = False
