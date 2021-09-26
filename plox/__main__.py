import sys

from . import lox


def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(args) == 1:
        lox.run_file(args[0])
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
