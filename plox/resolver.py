from enum import Enum

from . import lox


FunctionType = Enum("FunctionType", ["NONE", "FUNCTION", "INITIALIZER", "METHOD"])


ClassType = Enum("ClassType", ["NONE", "CLASS", "SUBCLASS"])


class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve(self, *args):
        for arg in args:
            arg.accept(self)

    def resolve_function(self, function, type):
        enclosing_function = self.current_function
        self.current_function = type

        self.begin_scope()
        for param in function.params:
            self.define(param)
        self.resolve(*function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if self.scopes:
            scope = self.scopes[-1]
            if name.lexeme in scope:
                lox.parse_error(
                    name, "Already a variable with this name in this scope."
                )
            scope[name.lexeme] = False

    def define(self, name):
        if self.scopes:
            self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes)):
            if name.lexeme in self.scopes[len(self.scopes) - 1 - i]:
                self.interpreter.resolve(expr, i)
                return

    def visit_block(self, stmt):
        self.begin_scope()
        self.resolve(*stmt.statements)
        self.end_scope()

    def visit_class(self, stmt):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)
        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                lox.parse_error(
                    stmt.superclass.name, "A class can't inherit from itself"
                )
            self.current_class = ClassType.SUBCLASS
            self.resolve(stmt.superclass)

        if stmt.superclass is not None:
            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            else:
                declaration = FunctionType.METHOD
            self.resolve_function(method, declaration)

        self.end_scope()

        if stmt.superclass is not None:
            self.end_scope()

        self.current_class = enclosing_class

    def visit_expression(self, stmt):
        self.resolve(stmt.expression)

    def visit_function(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if(self, stmt):
        self.resolve(stmt.condition, stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print(self, stmt):
        self.resolve(stmt.expression)

    def visit_return(self, stmt):
        if self.current_function is FunctionType.NONE:
            lox.parse_error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self.current_function is FunctionType.INITIALIZER:
                lox.parse_error(
                    stmt.keyword, "Can't return a value from an initializer."
                )
            self.resolve(stmt.value)

    def visit_var(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visit_while(self, stmt):
        self.resolve(stmt.condition, stmt.body)

    def visit_assign(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary(self, expr):
        self.resolve(expr.left, expr.right)

    def visit_call(self, expr):
        self.resolve(expr.callee, *expr.arguments)

    def visit_get(self, expr):
        self.resolve(expr.object)

    def visit_grouping(self, expr):
        self.resolve(expr.expression)

    def visit_literal(self, expr):
        pass

    def visit_logical(self, expr):
        self.resolve(expr.left, expr.right)

    def visit_set(self, expr):
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visit_super(self, expr):
        if self.current_class is ClassType.NONE:
            lox.parse_error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.current_class is not ClassType.SUBCLASS:
            lox.parse_error(
                expr.keyword, "Can't use 'super' in a class with no superclass."
            )
        self.resolve_local(expr, expr.keyword)

    def visit_this(self, expr):
        if self.current_class is not ClassType.CLASS:
            lox.parse_error(expr.keyword, "Can't use 'this' outside of a class.")
        self.resolve_local(expr, expr.keyword)

    def visit_unary(self, expr):
        self.resolve(expr.right)

    def visit_variable(self, expr):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            lox.parse_error(
                expr.name, "Can't read local variable in its own initializer."
            )
        self.resolve_local(expr, expr.name)
