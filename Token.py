# Alexis Dionne
# Compiler Project 2 - Tokens
# 3/6/19

class Token:
  # defines a token object to pass along through the compiler
  
  def __init__(self, lineNumber=0, value="", type=""):
    self.lineNumber = lineNumber
    self.value = value
    self.type = type
    
class Variable:
  type = ""
  isInit = False
  isUsed = False
  value = ""
  
  def __init__(v, type, isInit, isUsed, value):
    v.type = type
    v.isInit = isInit
    v.isUsed = isUsed
    v.value = value
    
  def getType(v):
    return v.type