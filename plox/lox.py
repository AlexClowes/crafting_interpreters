import sys


class Lox:
    def __init__(self):
        self.had_error = False

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

    @staticmethod
    def run(source):
        for token in Scanner(source).scan_tokens():
            print(token)

    def run_file(self, path):
        with open(path) as f:
            self.run(f.read())
        if self.had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            self.run(line)
            self.had_error = False

    def main(self):
        args = sys.argv[1:]
        if len(args) > 1:
            print("Usage: plox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.run_file(args[0])
        else:
            self.run_prompt()


if __name__ == "__main__":
    Lox().main()
