from myast import *
from lex import *
from parser import *

class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emitLine(self, code):
        self.code += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'

    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)



class ASTEmitter:
    def __init__(self, emitter):
        self.emitter = emitter
        self.symbols = set()

    def emitProgram(self, node: Program):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        for stmt in node.statements:
            self.emitStatement(stmt)

        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

    def emitStatement(self, stmt):
        if isinstance(stmt, LetStatement):
            if stmt.name not in self.symbols:
                self.symbols.add(stmt.name)
                self.emitter.headerLine(f"float {stmt.name};")
            self.emitter.emit(f"{stmt.name} = ")
            self.emitExpression(stmt.expression)
            self.emitter.emitLine(";")

        elif isinstance(stmt, PrintStatement):
            if isinstance(stmt.expression, String):
                self.emitter.emitLine(f'printf("{stmt.expression.value}\\n");')
            else:
                self.emitter.emit('printf("%.2f\\n", (float)(')
                self.emitExpression(stmt.expression)
                self.emitter.emitLine("));")

        elif isinstance(stmt, IfStatement):
            self.emitter.emit("if(")
            self.emitExpression(stmt.condition)
            self.emitter.emitLine("){")

            for s in stmt.then_body:
                self.emitStatement(s)

            self.emitter.emitLine("}")

            if stmt.else_body is not None:
                self.emitter.emitLine("else{")
                for s in stmt.else_body:
                    self.emitStatement(s)
                self.emitter.emitLine("}")

        elif isinstance(stmt, WhileStatement):
            self.emitter.emit("while(")
            self.emitExpression(stmt.condition)
            self.emitter.emitLine("){")
            for s in stmt.body:
                self.emitStatement(s)
            self.emitter.emitLine("}")

        elif isinstance(stmt, InputStatement):
            if stmt.name not in self.symbols:
                self.symbols.add(stmt.name)
                self.emitter.headerLine(f"float {stmt.name};")
            self.emitter.emitLine(f'if(0 == scanf("%f", &{stmt.name})) {{')
            self.emitter.emitLine(f'{stmt.name} = 0;')
            self.emitter.emitLine('scanf("%*s");')
            self.emitter.emitLine('}')

        elif isinstance(stmt, Identifier):
            self.emitter.emitLine(stmt.name + ";")



    def emitExpression(self, expr):
        if isinstance(expr, Number):
            self.emitter.emit(str(expr.value))
        elif isinstance(expr, String):
            self.emitter.emit(f'"{expr.value}"')
        elif isinstance(expr, Identifier):
            self.emitter.emit(expr.name)
        elif isinstance(expr, BinaryExpression):
            self.emitter.emit("(")
            self.emitExpression(expr.left)
            self.emitter.emit(f" {self.mapOperator(expr.operator)} ")
            self.emitExpression(expr.right)
            self.emitter.emit(")")
        elif isinstance(expr, UnaryExpression):
            self.emitter.emit(self.mapOperator(expr.operator))
            self.emitExpression(expr.operand)

        else:
            raise Exception(f"Unknown expression type: {type(expr)}")


    def mapOperator(self, operator):
        mapping = {
            TokenType.PLUS: '+',
            TokenType.MINUS: '-',
            TokenType.ASTERISK: '*',
            TokenType.SLASH: '/',
            TokenType.GT: '>',
            TokenType.GTEQ: '>=',
            TokenType.LT: '<',
            TokenType.LTEQ: '<=',
            TokenType.EQEQ: '==',
            TokenType.NOTEQ: '!='
        }
        return mapping.get(operator, '?')
