# Alexis Dionne
# Compiler - Driver
# 2/6/19

import sys

from Lexer import Lexer

print(str(sys.argv[-1]))
lexObj = Lexer(str(sys.argv[-1]))
lexObj.getFile()
lexObj.verifyLex()