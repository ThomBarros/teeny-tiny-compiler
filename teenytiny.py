from lex import Lexer
from parser import Parser
from myast import *
from emit import Emitter, ASTEmitter

with open("example.teeny", "r") as f:
    source = f.read()

lexer = Lexer(source)
parser = Parser(lexer, None)
ast = parser.parseProgram()
emitter = Emitter("out.c")
ast_emitter = ASTEmitter(emitter)
ast_emitter.emitProgram(ast)
emitter.writeFile()


