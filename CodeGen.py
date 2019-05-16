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
  
  id = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
  intList={'0','1','2','3','4','5','6','7','8','9'}
  
  def __init__(s, ast, scope):
    s.ast = ast
    s.scopeTree = scope
    
  def main(s):
    for x in range(256):
      s.code.append('00')
    s.analyze(s.ast.root)
    s.append('00')
    s.arrPos += 1
    print("\nSTATIC:\n",s.staticVar,"\nJUMP:\n",s.jump)
    print()
    s.printCode()
    s.backpatch()
    for x in range(s.arrPos-1, 256):
      s.code.append('00')
    print()
    s.printCode()
    
  def analyze(s, node):
    # move through AST and scope tree to generate code
    # call the proper method for each node that comes up
    # print()
    # print("NODE: ",node.name,"pos: ", s.arrPos)
    if 'Block' in node.name:
      s.blockGen(node)
    elif node.name is 'VarDecl':
      s.varDeclGen(node)
    elif node.name is 'Assignment':
      s.assignmentGen(node)
    elif node.name is 'If':
      s.ifGen(node.children[0])
      s.blockGen(node.children[1])
    elif node.name is 'While':
      #s.whileGen(node)
      print("While")
    elif node.name is 'Print':
      s.printGen(node.children[0])
    # else
      # nothing happens here because any other nodes dont need special care
    # s.printCode()
    
    # dig deeper if there are more kiddos
    if len(node.children) is not 0:
      for i in range(len(node.children)):
        s.analyze(node.children[i])
      if 'Block' in node.name:
        # return to the parent of this scope
        s.scopeTree.returnToParent()
      elif node.name == 'If':
        #print('arrpos - jump =',s.arrPos,'-',s.jump[s.jumpCount-1],'=',str(s.arrPos - s.jump[s.jumpCount-1] - 1))
        # will over shoot if the -1 at the end wasnt there
        s.jump[s.jumpCount-1] = str(s.arrPos - s.jump[s.jumpCount-1] - 1)
        
  def blockGen(s, node):
    # move up a scope level to grab correct data location
    print("\n"+node.name)
    s.findScope(node.name[6], s.scopeTree.root)
    
  def varDeclGen(s, node):
    # load the accumulator wih 0 and save a space in memory for the id
    print("\nVARDECL")
    s.append('A9') 
    s.append('00')
    s.append('8D')
    s.append(s.newStatic(node.children[1])) 
    s.append('XX')
    
  def assignmentGen(s, node):
    # load the accumulator with the number to assign and 
    # store that in the id's memory location
    print("\nASSIGNMENT")
    
    if node.children[1].name in s.id:
      # to an id
      s.append('AD')
      s.append('T'+s.findStatic(node.children[1]))
      s.append('XX')
    elif node.children[1].name in s.intList:
      # to an int
      s.append('A9')
      s.append('0'+node.children[1].name)
    elif node.children[1].name == 'Add':
      # id assigned to a series of additions
      addNode = node.children[1]
      if addNode.children[0].name in s.id:
        s.append('AD')
        s.append('T'+s.findStatic(addNode.children[0]))
        s.append('XX')
      elif addNode.children[0].name in s.intList:
        s.append('A9')
        s.append('0'+addNode.children[0].name)
      s.append('8D')
      temp = s.newStatic(addNode.children[0])
      s.append(temp)
      s.append("XX")
      s.addGen(temp, addNode)
    elif value is 'true':
      # to true
      s.code[s.arrPos] = 'A9'
      s.arrPos += 1
      s.code[s.arrPos] = '01'
      s.arrPos += 1
    elif value is 'false':
      # to false
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
    
    s.append('8D')
    s.append("T"+s.findStatic(node.children[0]))
    s.append('XX')
    
  def addGen(s, temp, node):
    # add all the things
    print('Add',node.name)
    if node.name in s.id:
      s.append('AD')
      s.append('T'+s.findStatic(node))
      s.append('XX')
    elif node.name in s.intList:
      s.append('A9')
      s.append('0'+node.name)
    s.append('6D')
    s.append(temp)
    s.append("XX")
    if len(node.children) > 0:
      for x in range(len(node.children)):
        s.addGen(temp, node.children[x])
    
  def printGen(s, node): 
    # load the value into the Y register and
    # print the value
    print("\nPRINT")
    # ADD FUNCITONALIY FOR PRINTING EXPRS
    if node.name in s.id:
      s.append('AC')
      s.append("T"+s.findStatic(node))
      s.append('XX')
      s.append('A2')
      if s.typeStatic(node) is 'string':
        s.append('02')
      else:
        s.append('01')
      s.append('FF')
    elif node.name in s.intList:
      s.append('A0')
      s.append('0'+node.name)
      s.append('A2')
      s.append('01')
      s.append('FF')
    
  def ifGen(s, node):
    # check if the two values are equivelent
    # and branch depending
    print("\nIF")
    if node.children[0].name in s.id:
      s.append('AE')
      s.append('T' + s.findStatic(node.children[0]))
      s.append('XX')
    elif node.children[0].name in s.intList:
      s.append('A2')
      s.append('0'+str(node.children[0].name))
    s.append('EC')
    if node.children[1].name in s.id:
      s.append('AE')
      s.append('T' + s.findStatic(node.children[1]))
      s.append('XX')
    elif node.children[1].name in s.intList:
      s.append('A2')
      s.append('0'+str(node.children[1].name))
    s.append('D0')
    s.append(s.newJump())
 
  def whileGen(s, node):
    # loop code
    boolop = node.children[0]
    child0 = boolop.children[0]
    child1 = boolop.children[1]
    block = node.children[1]
    t1 = ""
    t2 = ""
    jump = s.arrPos
    # get the first value to compare
    if child1 in s.id:
      s.append('AD')
      s.append('T' + s.findStatic(child1))
      s.append('XX')
    elif child1 in s.intList:
      s.append('AD')
      s.append('0' + child1.name)
    s.append('8D')
    s.append(s.newStatic(child1))
    t1 = s.code[s.arrPos-1]
    s.append('XX')
    # second value to compare
    if child0 in s.id:
      s.append('AD')
      s.append('T' + s.findStatic(child0))
      s.append('XX')
    elif child0 in s.intList:
      s.append('AD')
      s.append('0' + child0.name)
    s.append('8D')
    s.append(s.newStatic(child0))
    t2 = s.code[s.arrPos-1]
    s.append('XX')
    # load values in to compare
    s.append('AE')
    s.append(t2)
    s.append('XX')
    s.append('EC')
    s.append(t1)
    s.append('XX')
    s.append('A9')
    s.append('00')
    if boolop.name is 'isEq':
      s.append('D0')
      s.append(s.newJump())
    else:
      s.append('D0')
      s.append('02')
      s.append('A9')
      s.append('01')
      s.append('A2')
      s.append('00')
      s.append('8D')
      s.append(t1)
      s.append('XX')
      s.append('EC')
      s.append(t1)
      s.append('XX')
      s.append('D0')
      s.append(s.newJump())
    s.blockGen(block)
    s.append('A9')
    s.append('00')
    s.append('8D')
    s.append(t1)
    s.append('XX')
    s.append('A2')
    s.append('01')
    s.append('EC')
    s.append(t1)
    s.append('XX')
    s.append('D0')
    
  def backpatch(s):
    # go back through the code generated and replace any static variables
    for i in s.staticVar:
      address = hex(i + s.arrPos)[2:]
      if len(address) < 2:
        address = "0"+address
      #print('address of ',i,': ',address)
      s.staticVar[i][1] = address
    print(s.staticVar,s.jump)
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
        key = int(s.code[x][1])
        print("key", key)
        if s.jump[key] < 10:
          s.code[x] = '0' + s.jump[key]
        else:
          s.code[x] = s.jump[key]
        
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
        
  def append(s, str):
    # append to the end of the array and increment the position
    s.code.append(str)
    s.arrPos += 1
  
  def newStatic(s, node):
    # create a new variable entry in the static table
    
    # attributes = [name, address, scope, type]
    if node.name in s.id:
      s.staticVar[s.staticCount] = [node.name, 'XX', s.scopeTree.current.hashTable[node.name][1]]
    else:
      if node.name in s.intList:
        s.staticVar[s.staticCount] = [node.name, 'XX', 'int']
      elif node.name == 'true' or node.name == 'false':
        s.staticVar[s.staticCount] = [node.name, 'XX', 'boolean']
      else:
        s.staticVar[s.staticCount] = [node.name, 'XX', 'string']
    temp = "T"+str(s.staticCount)
    print(s.staticVar[s.staticCount],"temp:",temp)
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
    print("temp in find =",temp)
    return temp
    
  def typeStatic(s, node):
    # return the type of the node
    if s.findStatic(node) != "":
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
    
  def findScope(s, num, scope):
    # find and move to the correct scope
    print("Scope",scope.name,"  Num =",num)
    
    if int(num) == int(scope.name):
      s.scopeTree.current = scope
      print("found the scope ", scope.hashTable)
    else:
      if len(scope.children) is not 0: 
      # there are children so note these interior nodes and expand them
        for i in range(len(scope.children)):
          s.findScope(num, scope.children[i])