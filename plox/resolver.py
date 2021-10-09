from enum import Enum

from . import lox


FunctionType = Enum("FunctionType", ["NONE", "FUNCTION"])


class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

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
                lox.error(name, "Already a variable with this name in this scope.")
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

    def visit_expression(self, stmt):
        self.resolve(stmt.expression)

    def visit_function(self, stmt):
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
            lox.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
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

    def visit_grouping(self, expr):
        self.resolve(expr.expression)

    def visit_literal(self, expr):
        pass

    def visit_logical(self, expr):
        self.resolve(expr.left, expr.right)

    def visit_unary(self, expr):
        self.resolve(expr.right)

    def visit_variable(self, expr):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            lox.error("Can't read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
