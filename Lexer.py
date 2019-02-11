# Alexis Dionne
# Compiler Project 1 - Lex
# 2/6/19

class Lexer:
  # Lexer contains all methods and 
  # attributes for the lexer of the compiler
  
  def __init__(self, fileName=""):
    # Each lexer has a line and character position
    self.lineNum = 1
    self.currentPos = 0
    # A most recent full match
    self.lastPosition = 0
    
    # accepting states 
    # if state in accepting
    self.accepting = [1,4,5]
    
    # And a dictionary of movements through the DFA
    
    # 0 indicates an error state
    # go to state 2 if a / is found to check for * in any other state as comments may appear anywhere
    
    self.DFATable = [['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',0,1,2,3,4,5,6,7,8,9,'{','}','(',')','/','*','=','!','+','EoL'],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,0,0,2,0,0,0,1,0],#0
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],#1 - + accepting state
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0],#2 - will return to the start state if the / is found after *
      [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3],#3
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],#4 - accepting state of {
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],#5 - accepting state of }
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0]
      ]
    self.fileName = fileName
      
  def getFile(self):
    file = open(self.fileName, "r")
    print ("Printing all contents")
    print (file.read())
  
  
  def findTokens(self):
    state = 0
    nextState = 0
    currentChar = ""
    with open(self.fileName) as f:
      currentChar = f.read(1) # initialize the first character
      while True:
        nextState = self.DFATable[state][currentChar]
        state = nextState
        currentChar = f.read(1)
        if not currentChar:
          print ("EoF")
          break
        print ("CurrentChar : " + currentChar + "\n Current state: " + state)