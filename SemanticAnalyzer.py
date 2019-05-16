# Alexis Dionne
# Compiler Project 3 - Semanic Analysis
# 4/4/19

from Tree import Tree
from Tree import HashNode
from Token import Token
from CodeGen import CodeGen
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
    # drives the semantic analysis forward
    
    # convert CST to AST
    s.expand(s.cst.root, 0)
    
    print("AST of Program",s.programNumber,"...")
    # print the AST
    print(s.ast.toString())
    
    # analyze the program for type and scope
    s.analyze(s.ast.root)
    
    # output results of analysis
    if s.errors == 0:
      s.issueWarnings(s.scopeTree.root)
      print("\n",s.scopeTree.hashToString(),sep='')
      print("Code Gen INFO - Generating code...")
      gen = CodeGen(s.ast, s.scopeTree)
      gen.main()
    else:
      print("\nSymbol table not produced due to error(s).\nError Count: ",s.errors)
      
    s.astString = ''
    
  # recursive function to craft the AST from the CST
  def expand(s, node, depth):
    # depth's purpose was for crafting an AST string separately to compare to actual
    # no children/leaf nodes also ignore things like parentheses now (they suck anyway)
    if len(node.children) is 0 and node.name not in s.leafsIDontCareAbout: 
      s.ast.addNode(node.name, node.lineNumber, "child")
    # there are children so depending on if its good stuff, expand
    # otherwise, just keep digging
    else:
      if node.name is 'Print':
        # grab the Expr node and expand it
        s.ast.addNode("Print", node.lineNumber, "branch")
        s.expand(node.children[2], depth + 1)
        s.ast.returnToParent()
      elif node.name is 'VarDecl':
        # both nodes matter to varDecl equally
        s.ast.addNode("VarDecl", node.lineNumber, "branch")
        for i in range(len(node.children)):
          s.expand(node.children[i], depth + 1)
        s.ast.returnToParent()
      elif node.name is 'Assignment':
        # assignment cares about all of it's kids too
        s.ast.addNode("Assignment", node.lineNumber, "branch")
        for i in range(len(node.children)):
          s.expand(node.children[i], depth + 1)
        s.ast.returnToParent()
      elif node.name is 'IntExpr':
        # screw the '+', we only want variables
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
          if node.children[2].name == '==':
            s.ast.addNode("isEq", node.lineNumber, "branch")
          elif node.children[2].name == '!=':
            s.ast.addNode("notEq", node.lineNumber, "branch")
          s.expand(node.children[1], depth + 1)
          s.expand(node.children[3], depth + 1)
          s.ast.returnToParent()
        else:
          # it wanted to be smol instead and is just a boolVal
          s.expand(node.children[0], depth + 1)
      elif node.name is 'String':
        # string is so great it got it's own recursive function to squish 
        # down into a single string instead of a bunch of characters
        s.squishString(s.str, node)
        s.ast.addNode(s.str, node.lineNumber, "leaf")
        s.str = ""
      elif node.name is 'Block':
        # straight up has a favorite child, what a bad parent
        s.ast.addNode("Block", node.lineNumber, "branch")
        s.expand(node.children[1], depth + 1)
        if s.ast.root is not None:
          s.ast.returnToParent()
      elif node.name is 'While':
        # while has 2 kids to care for since they both grow up into bigger
        # and better things
        s.ast.addNode("While", node.lineNumber, "branch")
        s.expand(node.children[1], depth + 1) # grows up to be a booleanExpr
        s.expand(node.children[2], depth + 1) # grows up to be a whole Block!
        s.ast.returnToParent()
      elif node.name is 'If':
        # pretty much the same as while (copycat)
        s.ast.addNode("If", node.lineNumber, "branch")
        s.expand(node.children[1], depth + 1)
        s.expand(node.children[2], depth + 1)
        s.ast.returnToParent()
      else:
        # otherwise the compiler doesn't give a hoot about this node, and 
        # it moves on in search of a cooler child
        for i in range(len(node.children)):
          s.expand(node.children[i], depth)
        
  def analyze(s, node):
    # traverse AST depth-first, in-order
    
    #reset the result of the type test
    s.typeMatch = False
    
    # call the proper method for each node that comes up
    if node.name is 'Block':
      s.blockAnalysis(node)
      #print(s.scopeTree.current.name)
    elif node.name is 'VarDecl':
      s.varDeclAnalysis(node)
    elif node.name is 'Assignment':
      s.assignmentAnalysis(node)
    elif node.name is 'If' or node.name is 'While':
      s.booleanAnalysis(node.children[0])
      s.blockAnalysis(node.children[1])
    elif node.name is 'Print':
      s.printAnalysis(node.children[0])
    # else
      # nothing happens here because any other nodes dont need special care
      
    # dig deeper if there are more kiddos
    if len(node.children) is not 0:
      for i in range(len(node.children)):
        s.analyze(node.children[i])
      if 'Block' in node.name:
        # return to the parent of this scope
        #print('currentScope:',s.scopeTree.current.name)
        s.scopeTree.returnToParent()
        #print('currentScope:',s.scopeTree.current.name)
  
  def blockAnalysis(s, node):
    # adds a new empty hashNode
    if s.scopeTree.root is not None:
      # the root is always 0
      s.scopeCount += 1
      #print('node parent =',node.parent.name)
    node.name = "Block "+str(s.scopeCount)
    s.scopeTree.addHashNode(s.scopeCount, 'branch')
    s.scope = s.scopeTree.current
  
  def varDeclAnalysis(s, node):
    # add the variable declared to the current scope
    if s.scopeTree.current.addEntry(node.children[1].name, [node.children[0].name, node.children[0].lineNumber, False, False]) is 'Fail':
      print('SEMANTICS ERROR - SCOPE: ',node.children[1].name,' has already been declared in this scope (line ',node.children[1].lineNumber,')',sep='')
      s.errors += 1
    else:
      print('node parent =',node.parent.name)
      print(s.scopeTree.current.hashTable)
  
  def assignmentAnalysis(s, node):
    # check to see if the variable was declared and initialize it if type checks out
    s.checkScope(node.children[0].name, s.scopeTree.current)
    if node.children[1].name == 'BoolOp':
      s.booleanAnalysis(node)
      s.checkScope(node.children[0].name, s.scopeTree.current)
      s.evalExpr(node.children[1], s.scope.hashTable[node.children[0].name][0])
    elif s.scope.name != "-1":
      s.evalExpr(node.children[1], s.scope.hashTable[node.children[0].name][0])
    else:
      print('SEMANTICS ERROR - SCOPE: ',node.children[0].name,' does not exist in this scope (line ',node.children[0].lineNumber,')',sep='')
      s.errors += 1
    
    # return to original scope
    s.checkScope(node.children[0].name, s.scopeTree.current)
    if s.typeMatch is True:
      s.scope.hashTable[node.children[0].name][2] = True # isInit
    elif s.typeMatch is False and s.scope.name != '-1':
      # the rest of this print out occurs in evalExpr to get a better message
      print('SEMANTICS ERROR - SCOPE: ',node.children[0].name,' could not be assigned to ',node.children[1].name,' (line ',node.children[0].lineNumber,')',sep='')
      s.errors += 1
  
  def booleanAnalysis(s, node):
    s.checkScope(node.name, s.scopeTree.current)
    if len(node.children) is 0:
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
        print('SEMANTICS ERROR - SCOPE: ',node.name,' does not exist in this scope (line ',node.lineNumber,')',sep='')
        s.errors += 1
    else:
      # boolean analysis can keep unraveling into more exprs
      for i in range(len(node.children)):
        s.booleanAnalysis(node.children[i])
  
  def printAnalysis(s, node):
    # check the scope of the node to be printed and determine how to check it
    s.checkScope(node.name, s.scopeTree.current)
    #print("node:",node.name,'currentscope:',s.scopeTree.current.name,"scope:",s.scope.name)
    if node.name in s.scope.hashTable:
      s.evalExpr(node, s.scope.hashTable[node.name][0])
    elif node.name is 'true' or node.name is 'false' or node.name is 'BoolOp':
      s.evalExpr(node, 'boolean')
    elif node.name in s.intList or node.name == 'Add':
      s.evalExpr(node, 'int')
    elif s.scope.name == '-1':
      print('SEMANTICS ERROR - SCOPE: ',node.name,' does not exist in this scope (line ',node.lineNumber,')',sep='')
      s.errors += 1
    else:
      s.evalExpr(node, 'string')
      
    s.checkScope(node.name, s.scopeTree.current)
    if s.typeMatch is True and node.name in s.id:
      # print succeeded and the id should be updated as used
      s.scope.hashTable[node.name][3] = True # isUsed
    elif s.typeMatch is False and node.name in s.id:
      if s.scope.name == '-1':
        print('SEMANTICS ERROR - SCOPE: ',node.name,' has not been declared (line ',node.lineNumber,')',sep='')
        s.errors += 1
    else:
      if s.typeMatch is False:
        print('SEMANTICS ERROR - TYPE: ',node.name,' could not be printed (line ',node.lineNumber,')',sep='')
        s.errors += 1
    
# helper functions
  def checkScope(s, id, scope):
    # check the current scope and its parents for an id's declaration
    if scope.parent is None:
      if id in scope.hashTable:
        s.scope = scope
      else:
        s.scope = HashNode("-1")
    else:
      if id in scope.hashTable:
        s.scope = scope
      else: 
        s.checkScope(id, scope.parent)
  
  def evalExpr(s, node, type):
    # checks if all children of the current non terminal make sense(scope and type)
    s.typeMatch = False
    if node.name in s.id: # only update the scope check if its an id
      s.checkScope(node.name, s.scopeTree.current)
   #else do no scope check bc it def wont be in the map
    
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
          if s.scope.name != '-1' or node.name.find('"') != -1:
            s.typeMatch = type is 'string'
          else:
            s.typeMatch = False
      # if s.typeMatch == False and s.scope.name != '-1':
        # # big fail :(
        # print('SEMANTICS ERROR - TYPE:',node.name,'is not the same type as',end=' ')
      # elif s.typeMatch == False and s.scope.name == '-1':
        # print('SEMANTICS ERROR - SCOPE:',node.name,end=' ')
    elif node.name is 'BoolOp':
      # boolop produces a boolean result, so the type is compared to boolean
      s.typeMatch = type is 'boolean'
    else:
      # things like Add can unravel for a long time, so dig until the end to verify type
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
      