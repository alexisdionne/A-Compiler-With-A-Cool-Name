# Alexis Dionne
# Compiler Project 4 - Code Generation
# 5/7/19

from Tree import Tree
from Token import Token

class CodeGen:
  # generate runnable code for an OS to interpret using 6502a machine code
  
  ast = Tree()
  scopeTree = Tree()
  code = []
  arrPos = 0
  jump = {}
  staticVar = {}
  staticCount = 0
  
  id = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
  intList={'0','1','2','3','4','5','6','7','8','9'}
  
  def __init__(s, ast, scope):
    c.ast = ast
    c.scopeTree = scope
    
  def main(s):
    print("main")
    analyze(s.ast.root)
    backpatch()
    
  def analyze(s, node):
    # move through AST and scope tree to generate code
    # call the proper method for each node that comes up
    if node.name is 'Block':
      s.blockGen(node)
    elif node.name is 'VarDecl':
      s.varDeclGen(node)
    elif node.name is 'Assignment':
      s.assignmentGen(node)
    # elif node.name is 'If' or node.name is 'While':
      # s.booleanGen(node.children[0])
      # s.blockGen(node.children[1])
    elif node.name is 'Print':
      s.printGen(node.children[0])
    # else
      # nothing happens here because any other nodes dont need special care
      
    # dig deeper if there are more kiddos
    if len(node.children) is not 0:
      for i in range(len(node.children)):
        s.analyze(node.children[i])
      if node.name == 'Block':
        # return to the parent of this scope
        s.scopeTree.returnToParent()
        
  def blockGen(s, node):
    # move up a scope level to grab correct data location
    print("not sure what to do with this yet")
    
  def varDeclGen(s, node):
    # load the accumulator wih 0 and save a space in memory for the id
    s.code[s.arrPos++] = 'A9'
    s.code[s.arrPos++] = '00'
    s.code[s.arrPos++] = '8D'
    s.code[s.arrPos++] = newStatic(node.children[1])
    s.code[s.arrPos++] = 'XX'
    
  def assignmentGen(s, node):
    # load the accumulator with the number to assign and 
    # store that in the id's memory location
    s.code[s.arrPos++] = 'A9'
    s.code[s.arrPos++] = '0'+node.children[1].name
    s.code[s.arrPos++] = '8D'
    s.code[s.arrPos++] = findStatic(node.children[0])
    s.code[s.arrPos++] = 'XX' 
    
  def printGen(s, node): 
    # load the value into the Y register and
    # print the value
    
    # ADD FUNCITONALIY FOR PRINTING BOOLEXPRS
    if node.children[0].name in id:
      s.code[s.arrPos++] = 'AC'
      s.code[s.arrPos++] = findStatic(node.children[0])
      s.code[s.arrPos++] = 'XX'
      s.code[s.arrPos++] = 'FF'
      if typeStatic(node.children[0]) is 'string':
        s.code[s.arrPos++] = '02'
      else:
        s.code[s.arrPos++] = '01'
    
  def backpatch(s):
    # go back through the code generated and replace any static variables
    for i in staticVar:
      address = hex(staticVar[i] + s.arrPos])
      print('address of ',i,': ',address)
      s.staticVar[i][1] = address
    for x in range(len(s.code)):
      if 'T' in s.code[x]:
        # there is a T which identifies a variable
        # the second letter in the string identifies the unique key
        s.code[x] = s.staticVar[s.code[x][1]][1]
        s.code[x+1] = '00'
  
  # Helper methods
  
  def newStatic(s, node):
    # create a new variable entry in the static table
    s.staticVar[s.staticCount] = [node.name, 'XX', s.scopeTree.current[node.name][1]]
    temp = "T"+str(s.staticCount)
    s.staticCount++
    return temp
    
  def findStatic(s, node):
    # check for the id in the static variables table and return temp number
    temp = s.staticVar.key(node.name)
    temp = "T" + temp
    return temp
    
  def typeStatic(s, node)
    # return the type of the node
    type = s.staticVar.key(node.name)[1]
    return type