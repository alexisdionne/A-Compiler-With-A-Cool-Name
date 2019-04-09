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
  astString = ""
  s = ""
  
  nonTerminals = {'Print', 'VarDecl', 'Assignment', 'IntExpr', 'BooleanExpr', 'String', 'Block', 'While', 'If'}
  leafsIDontCareAbout = {'Statement List', 'CharList', '+', '=', '==', '!=', '$'}

  def __init__(self, tokenList=[], cst=Tree(), programNumber=0):
    self.tokenList = tokenList
    self.cst = cst
    self.programNumber = programNumber
    
  def main(self):
    # 1. make the AST
    # 2. check scope and type (depth first in order recursively)
      # a. search currentScope hash table for id + check if scope is good
      # b. search to check type
        # inheritance -> parents
        # synthesize -> children
        # intrinzic attributes -> type bc math said so
        # identifier class -> type, isInit, isUsed(for print and bool&int exprs)
        
    self.expand(self.cst.root, 0)
    print("printing ast:")
    print(self.astString)
    
    
  '''def makeAST(self, node, depth):
     # add depth
    for x in range(depth):
      self.result += "-"
      self.astString += '-'
    # no children/leaf nodes
    if len(node.children) is 0: #not node.children or 
      self.result += "["+node.name+"]"
      self.result += "\n"
      self.astString += "["+node.name+"]"
      self.astString += "\n"
    # there are children so note these interior nodes and expand them
    else:
      if node.name in self.nonTerminals:
        if node.name is 'Print':
          # child 2 is the Expr that could be anything
          self.astString += "<"+node.name+">\n"
          self.astPrint(node.children[2])
        elif node.name is 'VarDecl':
          self.astVarDecl(node)
        elif node.name is 'Assignment':
          self.astAssign(node)
        elif node.name is 'IntExpr':
          self.astInt(node)
        elif node.name is 'BooleanExpr':
          self.astBool(node)
        elif node.name is 'String':
          self.astString(node)
        elif node.name is 'Block':
          self.astBlock(node)
        elif node.name is 'While':
          self.astWhile(node)
        elif node.name is 'If':
          self.astIf(node)
          
      self.result += "<"+node.name+">\n"
      
      for i in range(len(node.children)):
        self.makeAST(node.children[i], depth + 1)
  
  # traverse the pieces of a print statement
  def astPrint(self, node):
    self.ast.addNode('Print', 'branch')
    if node.children[0].name is 'IntExpr':
      self.astInt(node.children[0])
    elif node.children[0].name is 'String':
      self.astString(node.children[0])
    elif node.children[0].name is 'BooleanExpr':
      self.astBool(node.children[0])
    elif node.children[0].name is 'Id':
      self.ast.addNode(node.children[0].name, 'leaf')
      '''
      
  # recursive function to craft the AST from the CST
  def expand(self, node, depth):
    
    # no children/leaf nodes also ignore things like parentheses now (they suck anyway)
    if len(node.children) is 0 and node.name not in self.leafsIDontCareAbout: 
      self.addDepth(depth)
      self.astString += "["+node.name+"]"
      self.astString += "\n"
    # there are children so depending on if its good stuff, expand
    # otherwise, just keep diggin
    else:
      if node.name is 'Print':
        # grab the Expr node and expand it
        self.addDepth(depth)
        self.astString += "<Print>\n"
        self.ast.addNode("Print", "branch")
        self.expand(node.children[2], depth + 1)
      elif node.name is 'VarDecl':
        # both nodes matter to varDecl equally
        self.addDepth(depth)
        self.astString += "<VarDecl>\n"
        self.ast.addNode("VarDecl", "branch")
        for i in range(len(node.children)):
          self.expand(node.children[i], depth + 1)
      elif node.name is 'Assignment':
        # assignment cares about all of it's kids too
        self.addDepth(depth)
        self.astString += "<Assignment>\n"
        self.ast.addNode("Assignment", "branch")
        for i in range(len(node.children)):
          self.expand(node.children[i], depth + 1)
      elif node.name is 'IntExpr':
        # screw the '+', we only want variables
        self.addDepth(depth)
        self.astString += "<Add>\n"
        self.ast.addNode("Add", "branch")
        self.expand(node.children[0], depth + 1)
        self.expand(node.children[2], depth + 1)
      elif node.name is 'BooleanExpr':
        # booleanExpr is confused about who to care about, it needs help
        if len(node.children) > 1:
          # it decided to be big and have multiple Expr
          self.addDepth(depth)
          self.astString += "<BoolOp>\n"
          self.ast.addNode("BoolOp", "branch")
          self.expand(node.children[1], depth + 1)
          self.expand(node.children[3], depth + 1)
        else:
          # it wanted to be smol instead and is just a boolVal
          self.expand(node.children[0], depth + 1)
      elif node.name is 'String':
        # string is so great it got it's own recursive function to squish 
        # down into a single string instead of a bunch of characters
        self.addDepth(depth)
        self.squishString(self.s, node)
        self.astString += "[" + self.s + "]\n"
        self.ast.addNode(self.s, "leaf")
        self.s = ""
      elif node.name is 'Block':
        self.addDepth(depth)
        self.astString += "<Block>\n"
        self.ast.addNode("Block", "branch")
        self.expand(node.children[1], depth + 1)
      elif node.name is 'While':
        self.addDepth(depth)
        self.astString += "<While>\n"
        self.ast.addNode("While", "branch")
        self.expand(node.children[1], depth + 1)
        self.expand(node.children[2], depth + 1)
      elif node.name is 'If':
        self.addDepth(depth)
        self.astString += "<If>\n"
        self.ast.addNode("If", "branch")
        self.expand(node.children[1], depth + 1)
        self.expand(node.children[2], depth + 1)
      else:
        for i in range(len(node.children)):
          self.expand(node.children[i], depth)
          
  def addDepth(self, depth):
    # add depth to str
    for x in range(depth):
      self.astString += "-"
  
  def squishString(self, s, node):
    if len(node.children) is 0 and node.name not in self.leafsIDontCareAbout: 
      # prepend the next char
      self.s = s + str(node.name)
    else:
      # there are more characters
      for i in range(len(node.children)):
        self.squishString(self.s, node.children[i])