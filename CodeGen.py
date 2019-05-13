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
  # key : [name, address, scope]
  staticVar = {}
  staticCount = 0
  heapPos = 255
  scopesVisited = []
  
  id = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
  intList={'0','1','2','3','4','5','6','7','8','9'}
  
  def __init__(s, ast, scope):
    s.ast = ast
    s.scopeTree = scope
    
  def main(s):
    for x in range(256):
      s.code.append('00')
    s.analyze(s.ast.root)
    s.arrPos += 1
    print("\nSTATIC:\n",s.staticVar,"\nJUMP:\n",s.jump)
    s.backpatch()
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
        s.scopeCount -= 1
        s.scopeTree.returnToParent()
      elif node.name == 'If':
        #print('arrpos - jump =',s.arrPos,'-',s.jump[s.jumpCount-1],'=',str(s.arrPos - s.jump[s.jumpCount-1] - 1))
        # will over shoot if the -1 at the end wasnt there
        s.jump[s.jumpCount-1] = str(s.arrPos - s.jump[s.jumpCount-1] - 1)
        
  def blockGen(s, node):
    # move up a scope level to grab correct data location
    s.scopesVisited.append(s.scopeTree.current.name)
    print("\nBLOCK",s.scopesVisited)
    
  def varDeclGen(s, node):
    # load the accumulator wih 0 and save a space in memory for the id
    print("\nVARDECL")
    s.code[s.arrPos] = 'A9'
    s.arrPos += 1
    s.code[s.arrPos] = '00'
    s.arrPos += 1
    s.code[s.arrPos] = '8D'
    s.arrPos += 1
    s.code[s.arrPos] = s.newStatic(node.children[1])
    s.arrPos += 1
    s.code[s.arrPos] = 'XX'
    s.arrPos += 1
    
  def assignmentGen(s, node):
    # load the accumulator with the number to assign and 
    # store that in the id's memory location
    print("\nASSIGNMENT")
    value = node.children[1].name
    if value in s.id:
      s.code[s.arrPos] = 'AD'
      s.arrPos += 1
      s.code[s.arrPos] = ('T'+s.findStatic(node.children[1]))
      s.arrPos += 1
      s.code[s.arrPos] = 'XX'
      s.arrPos += 1
    elif value in s.intList:
      s.code[s.arrPos] = 'A9'
      s.arrPos += 1
      s.code[s.arrPos] = ('0'+value)
      s.arrPos += 1
    elif value is 'true':
      s.code[s.arrPos] = 'A9'
      s.arrPos += 1
      s.code[s.arrPos] = '01'
      s.arrPos += 1
    elif value is 'false':
      s.code[s.arrPos] = 'A9'
      s.arrPos += 1
      s.code[s.arrPos] = '00'
      s.arrPos += 1
    else:
      # it must be a string
      # leave a 00 to signal the end of the string
      s.heapPos -= 1
      for x in range(len(value)-2, 0, -1):
        # look at each letter back to front
        #print(x," at ",value[x])
        encoded = str(hex(ord(value[x])))[2:]
        #print("encoded as hex: ",encoded)
        s.code[s.heapPos] = encoded
        s.heapPos -= 1
      s.code[s.arrPos] = 'A9'
      s.arrPos += 1
      # the +1 directs it back to the beginning of string
      s.code[s.arrPos] = str(hex(s.heapPos+1))[2:]
      #print('stored string at heapPos',hex(s.heapPos),'in code[',s.arrPos,']')
      s.arrPos += 1
    s.code[s.arrPos] = '8D'
    s.arrPos += 1
    s.code[s.arrPos] = ('T'+s.findStatic(node.children[0]))
    s.arrPos += 1
    s.code[s.arrPos] = 'XX'
    s.arrPos += 1
    
  def printGen(s, node): 
    # load the value into the Y register and
    # print the value
    print("\nPRINT")
    # ADD FUNCITONALIY FOR PRINTING BOOLEXPRS
    if node.name in s.id:
      s.code[s.arrPos] = 'AC'
      s.arrPos += 1
      s.code[s.arrPos] = ('T'+s.findStatic(node))
      s.arrPos += 1
      s.code[s.arrPos] = 'XX'
      s.arrPos += 1
      s.code[s.arrPos] = 'A2'
      s.arrPos += 1
      if s.typeStatic(node) is 'string':
        #print("its a string")
        s.code[s.arrPos] = '02'
        s.arrPos += 1
      else:
        s.code[s.arrPos] = '01'
        s.arrPos += 1
    elif node.name in s.intList:
      s.code[s.arrPos] = 'A0'
      s.arrPos += 1
      s.code[s.arrPos] = ('0'+node.name)
      s.arrPos += 1
      s.code[s.arrPos] = 'A2'
      s.arrPos += 1
      s.code[s.arrPos] = '01'
      s.arrPos += 1
    s.code[s.arrPos] = 'FF'
    s.arrPos += 1
    
  def ifGen(s, node):
    # check if the two values are equivelent
    # and branch depending
    print("\nIF")
    if node.children[0].name in s.id:
      s.code[s.arrPos] = 'AE'
      s.arrPos += 1
      s.code[s.arrPos] = ('T' + s.findStatic(node.children[0]))
      s.arrPos += 1
      s.code[s.arrPos] = 'XX'
      s.arrPos += 1
    elif node.children[0].name in s.intList:
      s.code[s.arrPos] = 'A2'
      s.arrPos += 1
      s.code[s.arrPos] = ('0'+str(node.children[0].name))
      s.arrPos += 1
    s.code[s.arrPos] = 'EC'
    s.arrPos += 1
    s.code[s.arrPos] = ('T' + s.findStatic(node.children[1]))
    s.arrPos += 1
    s.code[s.arrPos] = 'XX'
    s.arrPos += 1
    s.code[s.arrPos] = 'D0'
    s.arrPos += 1
    s.code[s.arrPos] = s.newJump()
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
        print("backpatch ",s.code[x])
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
    # attributes = [name, address, scope, type]
    s.staticVar[s.staticCount] = [node.name, 'XX', s.scopeTree.current.name, s.scopeTree.current.hashTable[node.name][0]]
    print(s.staticVar[s.staticCount])
    temp = "T"+str(s.staticCount)
    s.staticCount = s.staticCount + 1
    return temp
    
  def findStatic(s, node):
    # check for the id in the static variables table and return temp number
    temp = ""
    for x in s.staticVar:
      #print('x is',s.staticVar[x])
      if s.staticVar[x][0] == node.name and s.staticVar[x][2] == s.scopeTree.current.name:
        print("found ",s.staticVar[x])
        temp = str(x)
    #print("findStatic: ",temp, 'node name: ',node.name)
    return temp
    
  def typeStatic(s, node):
    # return the type of the node
    if s.findStatic(node) != "ERROR":
      key = int(s.findStatic(node))
      type = s.staticVar[key][3]
      #print(key,type)
    else:
      type = "ERROR"
    print("type =",type)
    return type
    
  def newJump(s):
    # create a new jump distance in jump table
    s.jump[s.jumpCount] = s.arrPos
    temp = "J" + str(s.jumpCount)
    s.jumpCount += 1
    print("newJump =",temp)
    return temp