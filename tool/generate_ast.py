import os
import sys


TAB = 4 * " "


def define_type(file, base_name, class_name, field_list):
    file.write(f"class {class_name}({base_name}):\n")
    # __init__
    file.write(TAB + f"def __init__(self, {field_list}):\n")
    for field in field_list.split(","):
        name = field.strip()
        file.write(2 * TAB + f"self.{name} = {name}\n")
    file.write("\n")
    # accept
    file.write(TAB + "def accept(self, visitor):\n")
    file.write(2 * TAB + f"return visitor.visit_{class_name.lower()}(self)\n")
    file.write("\n\n")


def define_ast(output_dir, base_name, types):
    path = os.path.join(output_dir, base_name.lower() + ".py")
    with open(path, mode="w") as f:
        f.write(f"class {base_name}:\n")
        f.write(TAB + "pass\n\n\n")

        # The AST classes
        for type in types:
            class_name, field_list = map(lambda s: s.strip(), type.split(":"))
            define_type(f, base_name, class_name, field_list)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: generate_ast <output_directory>")
        sys.exit(64)
    output_dir = args[0]

    define_ast(
        output_dir,
        "Expr",
        [
            "Assign : name, value",
            "Binary : left, operator, right",
            "Call : callee, paren, arguments",
            "Get : object, name",
            "Grouping : expression",
            "Literal : value",
            "Logical : left, operator, right",
            "Set : object, name, value",
            "Super : keyword, method",
            "This : keyword",
            "Unary : operator, right",
            "Variable : name"
        ],
    )

    define_ast(
        output_dir,
        "Stmt",
        [
            "Block : statements",
            "Class : name, superclass, methods",
            "Expression : expression",
            "Function: name, params, body",
            "If : condition, then_branch, else_branch",
            "Print : expression",
            "Return : keyword, value",
            "Var : name, initializer",
            "While : condition, body",
        ],
    )


if __name__ == "__main__":
    main()
