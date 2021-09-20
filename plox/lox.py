import sys

import scanner


HAD_ERROR = False


def error(line, message):
    report(line, "", message)


def report(line, where, message):
    print(f"[line {line}] Error{where}: {message}")
    global HAD_ERROR
    HAD_ERROR = True


def run(source):
    for token in scanner.Scanner(source).scan_tokens():
        print(token)


def run_file(path):
    with open(path) as f:
        run(f.read())
    if HAD_ERROR:
        sys.exit(65)


def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)
        global HAD_ERROR
        HAD_ERROR = False


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
