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
  jumpCount = 0
  staticVar = {}
  staticCount = 0
  
  id = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
  intList={'0','1','2','3','4','5','6','7','8','9'}
  
  def __init__(s, ast, scope):
    s.ast = ast
    s.scopeTree = scope
    
  def main(s):
    print("main")
    s.analyze(s.ast.root)
    s.code.append('00')
    s.arrPos += 1
    s.backpatch()
    for x in range(s.arrPos, 256):
      s.code.append('00')
    print()
    s.printCode()
    
  def analyze(s, node):
    # move through AST and scope tree to generate code
    # call the proper method for each node that comes up
    # print()
    # print("NODE: ",node.name,"pos: ", s.arrPos)
    if node.name is 'Block':
      s.blockGen(node)
    elif node.name is 'VarDecl':
      s.varDeclGen(node)
    elif node.name is 'Assignment':
      s.assignmentGen(node)
    elif node.name is 'If':
      s.ifGen(node.children[0])
      s.blockGen(node.children[1])
    # elif node.name is 'While':
      
    elif node.name is 'Print':
      s.printGen(node.children[0])
    # else
      # nothing happens here because any other nodes dont need special care
    # s.printCode()
    
    # dig deeper if there are more kiddos
    if len(node.children) is not 0:
      for i in range(len(node.children)):
        s.analyze(node.children[i])
      if node.name == 'Block':
        # return to the parent of this scope
        s.scopeTree.returnToParent()
      elif node.name == 'If':
        s.jump[s.jumpCount-1] = str(s.arrPos - s.jump[s.jumpCount-1])
        
  def blockGen(s, node):
    # move up a scope level to grab correct data location
    print("BLOCK not sure what to do with this yet")
    
  def varDeclGen(s, node):
    # load the accumulator wih 0 and save a space in memory for the id
    s.code.append('A9') 
    s.arrPos += 1
    s.code.append('00')
    s.arrPos += 1
    s.code.append('8D')
    s.arrPos += 1
    s.code.append(s.newStatic(node.children[1])) 
    s.arrPos += 1
    s.code.append('XX')
    s.arrPos += 1
    
  def assignmentGen(s, node):
    # load the accumulator with the number to assign and 
    # store that in the id's memory location
    if node.children[1].name in s.id:
      s.code.append('AD')
      s.arrPos += 1
      s.code.append('T'+s.findStatic(node.children[1]))
      s.arrPos += 1
      s.code.append('XX')
      s.arrPos += 1
    elif node.children[1].name in s.intList:
      s.code.append('A9')
      s.arrPos += 1
      s.code.append('0'+node.children[1].name)
      s.arrPos += 1
    s.code.append('8D')
    s.arrPos += 1
    s.code.append("T"+s.findStatic(node.children[0]))
    s.arrPos += 1
    s.code.append('XX')
    s.arrPos += 1
    
  def printGen(s, node): 
    # load the value into the Y register and
    # print the value
    
    # ADD FUNCITONALIY FOR PRINTING BOOLEXPRS
    if node.name in s.id:
      s.code.append('AC')
      s.arrPos += 1
      s.code.append("T"+s.findStatic(node))
      s.arrPos += 1
      s.code.append('XX')
      s.arrPos += 1
      s.code.append('A2')
      s.arrPos += 1
      if s.typeStatic(node) is 'string':
        s.code.append('02')
        s.arrPos += 1
      else:
        s.code.append('01')
        s.arrPos += 1
      s.code.append('FF')
      s.arrPos += 1
    elif node.name in s.intList:
      s.code.append('A0')
      s.arrPos += 1
      s.code.append('0'+node.name)
      s.arrPos += 1
      s.code.append('A2')
      s.arrPos += 1
      s.code.append('01')
      s.arrPos += 1
      s.code.append('FF')
      s.arrPos += 1
    
  def ifGen(s, node):
    # check if the two values are equivelent
    # and branch depending
    
    s.code.append('AE')
    s.arrPos += 1
    s.code.append('T' + s.findStatic(node.children[0]))
    s.arrPos += 1
    s.code.append('XX')
    s.arrPos += 1
    s.code.append('EC')
    s.arrPos += 1
    s.code.append('T' + s.findStatic(node.children[1]))
    s.arrPos += 1
    s.code.append('XX')
    s.arrPos += 1
    s.code.append('D0')
    s.arrPos += 1
    s.code.append(s.newJump())
    s.arrPos += 1
  
  def backpatch(s):
    # go back through the code generated and replace any static variables
    for i in s.staticVar:
      address = hex(i + s.arrPos)[2:]
      if len(address) < 2:
        address = "0"+address
      #print('address of ',i,': ',address)
      s.staticVar[i][1] = address
    for x in range(len(s.code)):
      if 'T' in s.code[x]:
        # there is a T which identifies a variable
        # the second letter in the string identifies the unique key
        key = s.code[x][1]
        #print("replacing T",key," with ",s.staticVar[int(key)][1])
        s.code[x] = s.staticVar[int(key)][1]
        s.code[x+1] = '00'
      elif 'J' in s.code[x]:
        key = s.code[x][1]
        if len(s.jump[int(key)][0]) < 2:
          s.code[x] = '0' + s.jump[int(key)][0]
        else:
          s.code[x] = s.jump[int(key)][0]
        
  
  # Helper methods
  
  def printCode(s):   
    # print code in easy to copy and paste format
    count = 0
    for x in range(len(s.code)):
      print(s.code[x], end=' ')
      if count % 7 == 0 and count != 0:
        # new line every 8 hex numbers
        print()
        count = 0
      else:
        count += 1
  
  def newStatic(s, node):
    # create a new variable entry in the static table
    s.staticVar[s.staticCount] = [node.name, 'XX', s.scopeTree.current.hashTable[node.name][1]]
    temp = "T"+str(s.staticCount)
    s.staticCount = s.staticCount + 1
    return temp
    
  def findStatic(s, node):
    # check for the id in the static variables table and return temp number
    temp = "ERROR"
    for x in s.staticVar:
      #print('x is',s.staticVar[x])
      if s.staticVar[x][0] == node.name:
        #print("found ",node.name)
        temp = str(x)
    return temp
    
  def typeStatic(s, node):
    # return the type of the node
    key = s.findStatic(node)
    print(key)
    if key in s.staticVar:
      type = s.staticVar[key]
    else:
      type = "ERROR"
    return type
    
  def newJump(s):
    # create a new jump distance in jump table
    s.jump[s.jumpCount] = s.arrPos
    temp = "J" + str(s.jumpCount)
    s.jumpCount += 1
    return temp