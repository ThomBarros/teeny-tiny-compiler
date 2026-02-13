from myast import *
import sys
from lex import *

class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    def checkToken(self, kind):
        return self.curToken.kind == kind

    def checkPeek(self, kind):
        return self.peekToken.kind == kind

    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected" + kind.name + ", got" + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    def expression(self):
        return self.term()
    
    def term(self):
        node = self.factor()

        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            operator = self.curToken.kind
            self.nextToken()
            right = self.factor()
            node = BinaryExpression(node, operator, right)

        return node

    def factor(self):
        node = self.unary()

        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            operator = self.curToken.kind
            self.nextToken()
            right = self.unary()
            node = BinaryExpression(node, operator, right)

        return node

    def unary(self):
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            operator = self.curToken.kind
            self.nextToken()
            right = self.unary()
            return UnaryExpression(operator, right)

        return self.primary()

    def primary(self):
        if self.checkToken(TokenType.NUMBER):
            value = float(self.curToken.text)
            self.nextToken()
            return Number(value)
        elif self.checkToken(TokenType.STRING):
            value = self.curToken.text
            self.nextToken()
            return String(value)
        elif self.checkToken(TokenType.IDENT):
            name = self.curToken.text
            self.nextToken()
            return Identifier(name)
        else:
            self.abort("Unexpected token at " + self.curToken.text)

    def parseProgram(self):
        program = Program()

        while not self.checkToken(TokenType.EOF):
            stmt = self.statement()
            if stmt is not None:
                program.statements.append(stmt)

        return program


    def comparison(self):
        left = self.expression()

        if not self.isComparisonOperator():
            self.abort("Expected comparison operator at " + self.curToken.text)

        operator = self.curToken.kind
        self.nextToken()
        right = self.expression()

        node = BinaryExpression(left, operator, right)

        while self.isComparisonOperator():
            operator = self.curToken.text
            self.nextToken()
            right = self.expression()
            node = BinaryExpression(node, operator, right)

        return node

    def isComparisonOperator(self):
        return (
            self.checkToken(TokenType.GT) or
            self.checkToken(TokenType.GTEQ) or
            self.checkToken(TokenType.LT) or
            self.checkToken(TokenType.LTEQ) or
            self.checkToken(TokenType.EQEQ) or
            self.checkToken(TokenType.NOTEQ)
        )


    def statement(self):
        if self.checkToken(TokenType.PRINT):
            self.nextToken()
            expr = self.expression()
            return PrintStatement(expr)
        elif self.checkToken(TokenType.LET):
            self.nextToken()

            if not self.checkToken(TokenType.IDENT):
                self.abort("Expected identifier after LET")

            name = self.curToken.text
            self.nextToken()
            self.match(TokenType.EQ)
            expr = self.expression()

            return LetStatement(name, expr)

        elif self.checkToken(TokenType.NEWLINE):
            self.nextToken()
            return None

        elif self.checkToken(TokenType.IF):
            self.nextToken()
            condition = self.comparison()
            self.match(TokenType.THEN)
            self.match(TokenType.NEWLINE)

            then_body = []
            while not self.checkToken(TokenType.ENDIF) and not self.checkToken(TokenType.ELSE):
                stmt = self.statement()
                if stmt is not None:
                    then_body.append(stmt)

            else_body = None
            if self.checkToken(TokenType.ELSE):
                self.nextToken()
                self.match(TokenType.NEWLINE)
                else_body = []

                while not self.checkToken(TokenType.ENDIF):
                    stmt = self.statement()
                    if stmt is not None:
                        else_body.append(stmt)

            self.match(TokenType.ENDIF)
            self.match(TokenType.NEWLINE)

            return IfStatement(condition, then_body, else_body)

        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            condition = self.comparison()
            self.match(TokenType.REPEAT)
            self.match(TokenType.NEWLINE)
            body = []

            while not self.checkToken(TokenType.ENDWHILE):
                stmt = self.statement()
                if stmt is not None:
                    body.append(stmt)
                
            self.match(TokenType.ENDWHILE)
            self.match(TokenType.NEWLINE)

            return WhileStatement(condition, body)

        elif self.checkToken(TokenType.INPUT):
            self.nextToken()
            if not self.checkToken(TokenType.IDENT):
                self.abort("Expected identifier after INPUT")
            name = self.curToken.text
            self.nextToken()
            return InputStatement(name)


        else:
            self.abort("Invalid statement at" + self.curToken.text)