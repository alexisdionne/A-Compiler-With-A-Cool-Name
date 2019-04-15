# Alexis Dionne
# Compiler Project 3 - Semanic Analysis
# 4/4/19

from Tree import Tree
from Token import Token
#from Token import Variable

class Semantics:

  cst = Tree()
  ast = Tree()
  scopeTree = Tree()
  scopeCount = 0
  tokenList = []
  errors = 0
  programNumber = 0
  astString = ''
  str = ''
  assignmentStr = ''
  typeMatch = True
  
  nonTerminals = {'Print', 'VarDecl', 'Assignment', 'IntExpr', 'BooleanExpr', 'String', 'Block', 'While', 'If'}
  leafsIDontCareAbout = {'Statement List', 'CharList', '+', '=', '==', '!=', '$'}
  id = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
  intList={'0','1','2','3','4','5','6','7','8','9'}

  def __init__(s, tokenList=[], cst=Tree(), programNumber=0):
    s.tokenList = tokenList
    s.cst = cst
    s.programNumber = programNumber
    s.ast = Tree()
    s.type = ['int','string','boolean']
    
  def main(s):
    # 1. make the AST (check)
    # 2. check scope and type (depth first in order recursively)
      # a. search currentScope hash table for id + check if scope is good
      # b. search to check type
        # inheritance -> parents
        # synthesize -> children
        # intrinzic attributes -> type bc math said so
        # identifier class -> type, isInit, isUsed(for print and bool&int exprs)
        
    s.expand(s.cst.root, 0)
    print("AST of Program",s.programNumber,"...")
    print(s.ast.toString())
    print()
    s.analyze(s.ast.root)
    
  # recursive function to craft the AST from the CST
  def expand(s, node, depth):
    
    # no children/leaf nodes also ignore things like parentheses now (they suck anyway)
    if len(node.children) is 0 and node.name not in s.leafsIDontCareAbout: 
      #s.addDepth(depth)
      s.astString += "["+node.name+"]"
      #s.astString += "\n"
      s.ast.addNode(node.name, "child")
    # there are children so depending on if its good stuff, expand
    # otherwise, just keep diggin
    else:
      if node.name is 'Print':
        # grab the Expr node and expand it
        #s.addDepth(depth)
        #s.astString += "<Print>\n"
        s.ast.addNode("Print", "branch")
        s.expand(node.children[2], depth + 1)
      elif node.name is 'VarDecl':
        # both nodes matter to varDecl equally
        #s.addDepth(depth)
        #s.astString += "<VarDecl>\n"
        s.ast.addNode("VarDecl", "branch")
        for i in range(len(node.children)):
          s.expand(node.children[i], depth + 1)
      elif node.name is 'Assignment':
        # assignment cares about all of it's kids too
        #s.addDepth(depth)
        #s.astString += "<Assignment>\n"
        s.ast.addNode("Assignment", "branch")
        for i in range(len(node.children)):
          s.expand(node.children[i], depth + 1)
      elif node.name is 'IntExpr':
        # screw the '+', we only want variables
        #s.addDepth(depth)
        #s.astString += "<Add>\n"
        if len(node.children) > 1:
          s.ast.addNode("Add", "branch")
          s.expand(node.children[0], depth + 1)
          s.expand(node.children[2], depth + 1)
        else:
          s.expand(node.children[0], depth + 1)
      elif node.name is 'BooleanExpr':
        # booleanExpr is confused about who to care about, it needs help
        if len(node.children) > 1:
          # it decided to be big and have multiple Expr
          #s.addDepth(depth)
          #s.astString += "<BoolOp>\n"
          s.ast.addNode("BoolOp", "branch")
          s.expand(node.children[1], depth + 1)
          s.expand(node.children[3], depth + 1)
        else:
          # it wanted to be smol instead and is just a boolVal
          s.expand(node.children[0], depth + 1)
      elif node.name is 'String':
        # string is so great it got it's own recursive function to squish 
        # down into a single string instead of a bunch of characters
        #s.addDepth(depth)
        s.squishString(s.str, node)
        #s.astString += "[" + s.s + "]\n"
        s.ast.addNode(s.str, "leaf")
        s.str = ""
      elif node.name is 'Block':
        # straight up has a favorite child, what a bad parent
        #s.addDepth(depth)
        s.astString += "<Block>\n"
        s.ast.addNode("Block", "branch")
        s.expand(node.children[1], depth + 1)
      elif node.name is 'While':
        # while has 2 kids to care for since they both grow up into bigger
        # and better things
        #s.addDepth(depth)
        #s.astString += "<While>\n"
        s.ast.addNode("While", "branch")
        s.expand(node.children[1], depth + 1) # grows up to be a booleanExpr
        s.expand(node.children[2], depth + 1) # grows up to be a whole Block!
      elif node.name is 'If':
        # pretty much the same as while (copycat)
        #s.addDepth(depth)
        #s.astString += "<If>\n"
        s.ast.addNode("If", "branch")
        s.expand(node.children[1], depth + 1)
        s.expand(node.children[2], depth + 1)
      else:
        # otherwise the compiler doesn't give a hoot about this node, and 
        # it moves on in search of a cooler child
        for i in range(len(node.children)):
          s.expand(node.children[i], depth)
        
  def analyze(s, node):
    # traverse AST depth-first, in-order
    
    if node.name is 'Block':
      s.blockAnalysis(node)
    elif node.name is 'VarDecl':
      s.varDeclAnalysis(node)
    elif node.name is 'Assignment':
      s.assignmentAnalysis(node)
    elif node.name is 'If':
      s.booleanAnalysis(node.children[0])
      s.blockAnalysis(node.children[1])
    # check scope
    #checkScope()
    # check type
    #checkType()
    if len(node.children) is 0: # no kids so go up
      # not sure what goes here?
      print(node.name,"is a child")
        
    else:
      print(node.name,"is a parent of",len(node.children),"children")
      for i in range(len(node.children)):
        s.analyze(node.children[i])
  
  def blockAnalysis(s, node):
    if s.scopeTree.root is not None:
      s.scopeCount += 1
    s.scopeTree.addHashNode(s.scopeCount, 'branch', True)
    print('block',s.scopeTree.current.name)
  
  def varDeclAnalysis(s, node):
    # add the variable declared to the current scope
    if s.scopeTree.current.addEntry(node.children[1].name, [node.children[0].name, False, False, None]) is 'Fail':
      print('Failed to add',node.children[1].name,'to scope',scopeCount)
      s.errors += 1
    else:
      print('it added',node.children[1].name)
      s.scopeTree.current.printHashTable()
  
  def assignmentAnalysis(s, node):
    # check to see if the variable was declared and initialize it
    #if s.checkScope(node.children[0].name, s.scopeTree.current) is not None:
      # type = s.scopeTree.current.hashTable[node.children[0].name][0]
      # typeMatch = True
      # for i in range(len(node.children)):
        # if node.children[i].name in id and s.checkScope(node.children[i].name, s.scopeTree.current):
          # s.scopeTree.current.hashTable[node.children[i].name][0]
    s.evalExpr(node, s.scopeTree.current.hashTable[node.children[0].name][0])
    if s.typeMatch is True:
      s.scopeTree.current.hashTable[node.children[0].name][1] = True # isInit
      s.buildAssignmentStr(node.children[1])
      s.scopeTree.current.hashTable[node.children[0].name][3] = s.assignmentStr
      print("Assigned",s.assignmentStr,"to",node.children[0].name)
      s.assignmentStr = ''
    else:
      print("Failed to assign",node.children[1].name,"to",node.children[0].name)
      s.errors += 1
  
  def booleanAnalysis(s, node):
    if len(node.children) is 0:
      if node.name in id and s.checkScope(node.name, s.scopeTree.current) is not None:
        s.scopeTree.current.hashTable[node.name][2] = True #isUsed
        # the node is a variable that needs to be checked for type
        print("this is a type thing, so skippish for now")
      else:
        s.errors += 1
        print(node.name," is not declared anywhere")
    else:
      for i in range(len(node.children)):
        s.booleanAnalysis(node.children[i])
  
  # def printAnalysis(s, node):
    # if
    
# helper functions         
  def addDepth(s, depth):
    # add depth to str
    for x in range(depth):
      s.astString += "-"
  
  def squishString(s, string, node):
    if len(node.children) is 0 and node.name not in s.leafsIDontCareAbout: 
      # prepend the next char
      s.str = string + str(node.name)
    else:
      # there are more characters
      for i in range(len(node.children)):
        s.squishString(s.str, node.children[i])
  
  def buildAssignmentStr(s, node):
    # build the string to be assigned to the id
    if node.name is 'Add':
      s.buildAssignmentStr(node.children[0])
      s.assignmentStr += " + "
      s.buildAssignmentStr(node.children[1])
    elif len(node.children) is 0:
      s.assignmentStr += node.name
    else:
      for i in range(len(node.children)):
        s.buildAssignmentStr(node.children[i])
      
  def checkScope(s, id, scope):
    # check the current scope and its parents for an id's declaration
    print(scope.hashTable)
    print(id)
    if scope.parent is None:
      if id in scope.hashTable:
        print("returning scope")
        return scope
      else:
        print("does not exist in scope")
        return None
    else:
      if id in scope.hashTable:
        print("returning scope")
        return scope
      else: 
        checkScope(id, scope.parent)
  
  def evalExpr(s, node, type):
    # checks if all children of the current non terminal make sense(scope and type)
    if(len(node.children)) is 0:
      print(node.name,"nodename")
      if node.name in s.id and s.checkScope(node.name, s.scopeTree.current) is not None:
        scope = s.checkScope(node.name, s.scopeTree.current)
        #scope.hashTable[node.name][2] = True # isUsed
        s.typeMatch = scope.hashTable[node.name][0] is type
      else:
        if node.name is 'false' or node.name is 'true':
          s.typeMatch = type is 'boolean'
        elif node.name in s.intList:
          s.typeMatch = type is 'int'
        else:
          s.typeMatch = type is 'string'
    else:
      for i in range(len(node.children)):
        s.evalExpr(node.children[i], type)