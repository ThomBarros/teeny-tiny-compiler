class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self):
        self.statements = []

class LetStatement(ASTNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class String(ASTNode):
    def __init__(self, value):
        self.value = value


class IfStatement(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class InputStatement(ASTNode):
    def __init__(self, name):
        self.name = name