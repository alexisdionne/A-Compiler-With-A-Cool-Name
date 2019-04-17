# Alexis Dionne
# Compiler Project 3 - Semanic Analysis
# 4/4/19

from Tree import Tree
from Tree import HashNode
from Token import Token
#from Token import Variable

class Semantics:

  cst = Tree()
  ast = Tree()
  scopeTree = Tree()
  scopeCount = 0
  scope = None
  tokenList = []
  errors = 0
  programNumber = 0
  astString = ''
  str = ''
  assignmentStr = ''
  typeMatch = True
  
  nonTerminals = {'Print', 'VarDecl', 'Assignment', 'IntExpr', 'BooleanExpr', 'String', 'Block', 'While', 'If'}
  leafsIDontCareAbout = {'Statement List', 'CharList', '+', '=', '==', '!=', '$', '(', ')'}
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
    #print(s.astString)
    s.analyze(s.ast.root)
    if s.errors == 0:
      s.issueWarnings(s.scopeTree.root)
      print("\n",s.scopeTree.hashToString(),sep='')
    else:
      print("\nSymbol table not produced due to error(s).\nError Count: ",s.errors)
    s.astString = ''
    
  # recursive function to craft the AST from the CST
  def expand(s, node, depth):
    # print('node is ',node.name)
    # if s.ast.root is not None:
      # print('current node is',s.ast.current.name)
      # if s.ast.current.parent is not None:
        # print('currents parent is',s.ast.current.parent.name)
    # no children/leaf nodes also ignore things like parentheses now (they suck anyway)
    if len(node.children) is 0 and node.name not in s.leafsIDontCareAbout: 
      s.addDepth(depth)
      s.astString += "["+node.name+"]"
      s.astString += "\n"
      s.ast.addNode(node.name, node.lineNumber, "child")
    # there are children so depending on if its good stuff, expand
    # otherwise, just keep diggin
    else:
      if node.name is 'Print':
        # grab the Expr node and expand it
        s.addDepth(depth)
        s.astString += "<Print>\n"
        s.ast.addNode("Print", node.lineNumber, "branch")
        s.expand(node.children[2], depth + 1)
        s.ast.returnToParent()
      elif node.name is 'VarDecl':
        # both nodes matter to varDecl equally
        s.addDepth(depth)
        s.astString += "<VarDecl>\n"
        s.ast.addNode("VarDecl", node.lineNumber, "branch")
        for i in range(len(node.children)):
          s.expand(node.children[i], depth + 1)
        s.ast.returnToParent()
      elif node.name is 'Assignment':
        # assignment cares about all of it's kids too
        s.addDepth(depth)
        s.astString += "<Assignment>\n"
        s.ast.addNode("Assignment", node.lineNumber, "branch")
        for i in range(len(node.children)):
          s.expand(node.children[i], depth + 1)
        s.ast.returnToParent()
      elif node.name is 'IntExpr':
        # screw the '+', we only want variables
        s.addDepth(depth)
        s.astString += "<Add>\n"
        if len(node.children) > 1:
          s.ast.addNode("Add", node.lineNumber, "branch")
          s.expand(node.children[0], depth + 1)
          s.expand(node.children[2], depth + 1)
          s.ast.returnToParent()
        else:
          s.expand(node.children[0], depth + 1)
      elif node.name is 'BooleanExpr':
        # booleanExpr is confused about who to care about, it needs help
        if len(node.children) > 1:
          # it decided to be big and have multiple Expr
          s.addDepth(depth)
          s.astString += "<BoolOp>\n"
          s.ast.addNode("BoolOp", node.lineNumber, "branch")
          s.expand(node.children[1], depth + 1)
          s.expand(node.children[3], depth + 1)
          s.ast.returnToParent()
        else:
          # it wanted to be smol instead and is just a boolVal
          s.expand(node.children[0], depth + 1)
      elif node.name is 'String':
        # string is so great it got it's own recursive function to squish 
        # down into a single string instead of a bunch of characters
        s.addDepth(depth)
        s.squishString(s.str, node)
        s.astString += "[" + s.str + "]\n"
        s.ast.addNode(s.str, node.lineNumber, "leaf")
        s.str = ""
      elif node.name is 'Block':
        # straight up has a favorite child, what a bad parent
        s.addDepth(depth)
        s.astString += "<Block>\n"
        s.ast.addNode("Block", node.lineNumber, "branch")
        s.expand(node.children[1], depth + 1)
        if s.ast.root is not None:
          s.ast.returnToParent()
      elif node.name is 'While':
        # while has 2 kids to care for since they both grow up into bigger
        # and better things
        s.addDepth(depth)
        s.astString += "<While>\n"
        s.ast.addNode("While", node.lineNumber, "branch")
        s.expand(node.children[1], depth + 1) # grows up to be a booleanExpr
        s.expand(node.children[2], depth + 1) # grows up to be a whole Block!
        s.ast.returnToParent()
      elif node.name is 'If':
        # pretty much the same as while (copycat)
        s.addDepth(depth)
        s.astString += "<If>\n"
        s.ast.addNode("If", node.lineNumber, "branch")
        s.expand(node.children[1], depth + 1)
        s.expand(node.children[2], depth + 1)
        s.ast.returnToParent()
      else:
        # otherwise the compiler doesn't give a hoot about this node, and 
        # it moves on in search of a cooler child
        #print('no hoots given for',node.name)
        for i in range(len(node.children)):
          s.expand(node.children[i], depth)
        
  def analyze(s, node):
    # traverse AST depth-first, in-order
    s.typeMatch = False
    # if s.scopeTree.root is not None:
      # print(s.scopeTree.hashToString())
    if node.name is 'Block':
      s.blockAnalysis(node)
    elif node.name is 'VarDecl':
      s.varDeclAnalysis(node)
    elif node.name is 'Assignment':
      s.assignmentAnalysis(node)
    elif node.name is 'If' or node.name is 'While':
      #print('child 1:',node.children[0].name)
      #print('child 2:',node.children[1].name)
      s.booleanAnalysis(node.children[0])
      s.blockAnalysis(node.children[1])
    elif node.name is 'Print':
      s.printAnalysis(node.children[0])
    if len(node.children) is not 0:
      #print(node.name,"is a parent of",len(node.children),"children")
      for i in range(len(node.children)):
        #print("ANALYZING ",node.children[i].name,'... scope',s.scopeTree.current.name)
        s.analyze(node.children[i])
      if node.name == 'Block':
        #print('Returned from Block',s.scopeTree.current.name)
        s.scopeTree.returnToParent()
  
  def blockAnalysis(s, node):
    #print('--BLOCK--')
    if s.scopeTree.root is not None:
      s.scopeCount += 1
    s.scopeTree.addHashNode(s.scopeCount, 'branch')
    s.scope = s.scopeTree.current
    #print('block',s.scopeTree.current.name)
  
  def varDeclAnalysis(s, node):
    #print('--VARDECL--')
    # add the variable declared to the current scope
    if s.scopeTree.current.addEntry(node.children[1].name, [node.children[0].name, node.children[0].lineNumber, False, False, None]) is 'Fail':
      print('SEMANTICS ERROR - SCOPE:',node.children[1].name,'has already been declared in this scope')
      s.errors += 1
  
  def assignmentAnalysis(s, node):
    #print('--ASSIGNMENT--')
    # check to see if the variable was declared and initialize it if type checks out
    #print('YOOOOOOOOOOOO',node.children[1].name)
    s.checkScope(node.children[0].name, s.scopeTree.current)
    #print(s.scope.hashTable)
    if node.children[1].name == 'BoolOp':
      #print('WENT IN HERE')
      s.booleanAnalysis(node)
      #print('right before eval again')
      s.checkScope(node.children[0].name, s.scopeTree.current)
      s.evalExpr(node.children[1], s.scope.hashTable[node.children[0].name][0])
    elif s.scope.name != "-1":
      #print("checking ",node.children[0].name,"against",node.children[1].name)
      s.evalExpr(node.children[1], s.scope.hashTable[node.children[0].name][0])
    else:
      print('SEMANTICS ERROR - SCOPE:',node.children[0].name,'does not exist in this scope')
      s.errors += 1
    
    # return to original scope
    s.checkScope(node.children[0].name, s.scopeTree.current)
    if s.typeMatch is True:
      s.scope.hashTable[node.children[0].name][2] = True # isInit
      #print("updated hash of",node.children[0].name,":",s.scope.hashTable[node.children[0].name])
    elif s.typeMatch is False and s.scope.name != '-1':
      print(node.children[0].name)
      s.errors += 1
  
  def booleanAnalysis(s, node):
    #print('--BOOLEAN--')
    s.checkScope(node.name, s.scopeTree.current)
    #print(node.name)
    if len(node.children) is 0:
      #s.evalExpr(node, s.scopeTree.current.hashTable[node.children[0].name][0])
      if node.name in s.scope.hashTable:
        s.evalExpr(node, s.scope.hashTable[node.name][0])
      elif node.name is 'true' or node.name is 'false':
        s.evalExpr(node, 'boolean')
      elif node.name in s.intList:
        s.evalExpr(node, 'int')
      else:
        s.evalExpr(node, 'string')
        
      if s.typeMatch is True and node.name in s.scope.hashTable:
        if node.parent.children[0].name is not node.name:
          # will only update to used if it is not the one being assigned
          s.scope.hashTable[node.name][3] = True #isUsed
      elif s.typeMatch is not True:
        print('SEMANTICS ERROR - SCOPE:',node.name,'does not exist in this scope')
        s.errors += 1
    else:
      for i in range(len(node.children)):
        s.booleanAnalysis(node.children[i])
  
  def printAnalysis(s, node):
    #print('--PRINT--')
    s.checkScope(node.name, s.scopeTree.current)
    if node.name in s.scope.hashTable:
      s.evalExpr(node, s.scope.hashTable[node.name][0])
    elif node.name is 'true' or node.name is 'false':
      s.evalExpr(node, 'boolean')
    elif node.name in s.intList:
      s.evalExpr(node, 'int')
    elif s.scope is None:
      print('SEMANTICS ERROR - SCOPE:',node.name,'does not exist in this scope')
      s.errors += 1
    else:
      s.evalExpr(node, 'string')
      
    s.checkScope(node.name, s.scopeTree.current)
    if s.typeMatch is True:
      # print succeeded and the id should be updated as used
      s.scope.hashTable[node.name][3] = True # isUsed
    else:
      if s.scope.name == '-1':
        print('SEMANTICS ERROR - SCOPE:',node.name,'has not been declared')
        s.errors += 1
      else:
        print('SEMANTICS ERROR - TYPE:',node.name,'could not be printed')
        s.errors += 1
    #print("updated hash of'",node.name,"':" ,s.scope.hashTable[node.name])
    
# helper functions
  def checkScope(s, id, scope):
    # check the current scope and its parents for an id's declaration
    #print(id,'in',scope.hashTable)
    if scope.parent is None:
      if id in scope.hashTable:
        #print("returning scope",scope.hashTable)
        s.scope = scope
      else:
        #print("does not exist in scope")
        s.scope = HashNode("-1")
    else:
      if id in scope.hashTable:
        #print("returning scope",scope.name)
        s.scope = scope
      else: 
        s.checkScope(id, scope.parent)
  
  def evalExpr(s, node, type):
    # checks if all children of the current non terminal make sense(scope and type)
    #print("--EVAL--\nnodename:",node.name," type checking:",type)
    s.typeMatch = False
    if node.name in s.id: # only update the scope check if its an id
      s.checkScope(node.name, s.scopeTree.current)
    # else do no scope check bc it def wont be in the map
    
    #print("node",node.name," #kids:",len(node.children))
    #print(s.scope.name," :",s.scope.hashTable)
    if(len(node.children)) == 0:
      if node.name in s.id and s.scope.name != "-1":
        s.scope.hashTable[node.name][3] = True # isUsed
        s.typeMatch = s.scope.hashTable[node.name][0] is type
      else:
        if node.name is 'false' or node.name is 'true':
          s.typeMatch = type is 'boolean'
        elif node.name in s.intList:
          s.typeMatch = type is 'int'
        else:
          if s.scope.name != '-1':
            s.typeMatch = type is 'string'
          else:
            s.typeMatch = False
      if s.typeMatch == False and s.scope.name != '-1':
        print('SEMANTICS ERROR - TYPE:',node.name,'is not the same type as',end=' ')
    elif node.name is 'BoolOp':
      #print('compared boolop(boolean) to ',type)
      # boolop produces a boolean result, so the type is compared to boolean
      s.typeMatch = type is 'boolean'
    else:
      for i in range(len(node.children)):
        s.evalExpr(node.children[i], type)
        
  def issueWarnings(s, node):
    # goes through and determines warnings for
    # 1) declared but not used
    # 2) uninitialized but used
    # 3) initialized but not used
    hash = node.hashTable
    for i in node.hashTable:
      if hash[i][2] == False: # not initialized
        if hash[i][3] == True: # used
          print('SEMANTICS WARNING - ',i,'is used and not initialized.')
        else: # unused
          print('SEMANTICS WARNING - ',i,'is never used or initialized.')
      else: # initialized
        if hash[i][3] == False: # unused
          print('SEMANTICS WARNING - ',i,'is initialized but unused.')
          
    if len(node.children) is not 0: 
    # there are children so note these interior nodes and expand them
      for i in range(len(node.children)):
        s.issueWarnings(node.children[i])
             
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
      