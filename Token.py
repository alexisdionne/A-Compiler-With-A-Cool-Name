# Alexis Dionne
# Compiler Project 1 - Tokens
# 3/6/19

class Token:
  # defines a token object to pass along through the compiler
  
  def __init__(self, lineNumber=0, value="", type=""):
    self.lineNumber = lineNumber
    self.value = value
    self.type = type