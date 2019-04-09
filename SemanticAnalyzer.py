# Alexis Dionne
# Compiler Project 3 - Semanic Analysis
# 4/4/19

from Tree import Tree
from Token import Token

class Semantics:

  cst = Tree()
  ast = Tree()
  tokenList = []
  errors = 0
  programNumber = 0
  

  def __init__(self, tokenList=[], cst=Tree(), programNumber=0):
    self.tokenList = tokenList
    self.cst = cst
    self.programNumber = programNumber
    
  def main(self):
    print(self.cst.current.name)