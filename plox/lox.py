import sys

import lox
from interpreter import Interpreter
import parser
import scanner
from tokens import TokenType


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
    lox.HAD_RUNTIME_ERROR = True


def report(line, where, message):
    print(f"[line {line}] Error{where}: {message}")
    lox.HAD_ERROR = True


def run(source):
    tokens = scanner.Scanner(source).scan_tokens()
    expression = parser.Parser(tokens).parse()
    if not lox.HAD_ERROR:
        INTERPRETER.interpret(expression)


def run_file(path):
    with open(path) as f:
        run(f.read())
    if lox.HAD_ERROR:
        sys.exit(65)
    if lox.HAD_RUNTIME_ERROR:
        sys.exit(70)


def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)
        lox.HAD_ERROR = False


def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()


if __name__ == "__main__":
    main()
