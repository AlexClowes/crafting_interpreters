class Expr:
    pass


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign(self)


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)


class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call(self)


class Get(Expr):
    def __init__(self, object, name):
        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical(self)


class Set(Expr):
    def __init__(self, object, name, value):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable(self)


