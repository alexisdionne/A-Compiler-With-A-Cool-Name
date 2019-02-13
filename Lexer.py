# Alexis Dionne
# Compiler Project 1 - Lex
# 2/6/19
import re

class Lexer:
  # Lexer contains all methods and 
  # attributes for the lexer of the compiler
  
  def __init__(self, fileName=""):
    # Each lexer has a line and character position
    self.lineNum = 1
    self.currentPos = 0
    self.linePos = 0
    self.contents = ""
    self.totalPrograms = 1
    
    # accepting states available to identify tokens
    self.accepting = {
      1 : ["INTOP",  '+'],      # +
      4 : ["L_BRACE",'{'],      # {
      5 : ["R_BRACE",'}'],      # }
      6 : ["EOP",    '$'],      # $
      11: ["P_STMT", 'print'],  # print
      12: ["L_PAREN",'('],      # (
      13: ["R_PAREN",')'],      # )
      14: ["DIGIT", '0'],       # 0-9 
      15: ["QUOTE",  '"'],      # "
      20: ["W_STMT", 'while'],  # while
      23: ["I_TYPE", 'int'],    # int
      24: ["A_STMT", '='],      # =
      26: ["BOOLOP",'!='], # != | ==
      27: ["S_TYPE", 'string'], # string
      28: ["I_STMT", 'if'],     # if
      29: ["B_TYPE", 'boolean'],# boolean
      30: ["B_VAL",'false'],    # false
      31: ["CHAR", 'a'],        # a-z 
      32: ["B_VAL",'true'],     # true
      33: ["BOOLOP",'=='],      # ==
      34: ["ID", 'a']           # single char id
    }
    # a list of the keywords available in the grammar
    self.keywords = [11,20,23,27,28,29,30,32]
    # a list of available symbols to stop at when lexing
    self.symbols = ['+','{','}','(',')','==','!=','=','"','$']
    
    # And a dictionary of movements through the DFA
    
    # 0 indicates an error state
    # go to state 2 if a / is found to check for * in any other state as comments may appear anywhere
    # all characters have the same accepting state, and need to be checked for a follow up char
    self.DFATable = [
    # [ a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, {, }, (, ), /, *, =, !, +, $,  ,\n, "],
      [ 0, 2, 0, 0, 0, 2, 0, 0,21, 0, 0, 0, 0, 0, 0, 7, 0, 0, 2, 2, 0, 0,16, 0, 0, 0,14,14,14,14,14,14,14,14,14,14, 4, 5,12,13, 2, 0,24,25, 1, 6, 0, 0,15],  #0
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #1  - + accepting state
      [ 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],  #2  - going into comment - s -> t
      [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],  #3  - comment found
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #4  - { accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #5  - } accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #6  - $ accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #7  - p
      [ 0, 0, 0, 0,30, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #8  - r
      [ 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #9  - i
      [16, 0, 0, 0,32, 0,27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #10 - n
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #11 - t - print accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #12 - ( accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #13 - ) accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #14 - digit accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #15 - " accepting state
      [ 0, 0, 0, 0, 0, 0, 0,17, 0, 0, 0, 0, 0,29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #16 - w
      [ 0, 0, 0, 0, 0, 0, 0, 0,18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #17 - h
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #18 - i
      [ 0, 0, 0, 0,20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #19 - l
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #20 - e - while accepting state
      [ 0, 0, 0, 0, 0,28, 0, 0, 0, 0, 0, 0, 0,22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #21 - i
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #22 - n 
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #23 - t - int accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,33, 0, 0, 0, 0, 0, 0],  #24 - = (assignment) accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,26, 0, 0, 0, 0, 0, 0],  #25 - !
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #26 - != accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #27 - string accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #28 - if accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #29 - boolean accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #30 - false accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #31 - char accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #32 - true accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]   #33 - == accepting state
      ]
    
    self.fileName = fileName
      
  def getFile(self):
  # arbitrary method for seeing the contents of the file before reading output
  # reads file contents into a string
    file = open(self.fileName, "r")
    self.contents = file.read()
    print ("Printing all contents")
    print (self.contents+"\n--------------------------------------------------------------\n")
    #for i,c in enumerate(self.contents):
    #  print (i,c)
    
    # remove comments
    self.contents = re.sub('/\*.*?\*/', '', self.contents, flags= re.S)
    print ("Printing modified contents")
    print (self.contents+"\n--------------------------------------------------------------\n")
    
    self.totalPrograms = self.contents.count('$')
    
  def getIndexFromChar(self, c):
  # returns the index in the DFATable of the character provided
    CharToNum = {
      'a' : 0,
      'b' : 1,
      'c' : 2,
      'd' : 3,
      'e' : 4,
      'f' : 5,
      'g' : 6,
      'h' : 7,
      'i' : 8,
      'j' : 9,
      'k' : 10,
      'l' : 11,
      'm' : 12,
      'n' : 13,
      'o' : 14,
      'p' : 15,
      'q' : 16,
      'r' : 17,
      's' : 18,
      't' : 19,
      'u' : 20,
      'v' : 21,
      'w' : 22,
      'x' : 23,
      'y' : 24,
      'z' : 25,
      '0' : 26,
      '1' : 27,
      '2' : 28,
      '3' : 29,
      '4' : 30,
      '5' : 31,
      '6' : 32,
      '7' : 33,
      '8' : 34,
      '9' : 35,
      '{' : 36,
      '}' : 37,
      '(' : 38,
      ')' : 39,
      '/' : 40,
      '*' : 41,
      '=' : 42,
      '!' : 43,
      '+' : 44,
      '$' : 45,
      ' ' : 46,
      '\n' : 47,
      '"' : 48
    }
    return CharToNum.get(c)
      
  
  def verifyLex(self):
  # search through a file and pick out tokens from the grammar
  # initialize variables
    counter = 0
    errorCount = 0
    programCount = 1
    state = 0
    nextState = 0
    currentChar = ""
    index = 0
    inQuotes = False  # all characters read until the next " are marked as char
    
    
    # variables for greedy algorithm
    lastPosition = 0        # the location of the last character that was recognized as a token
    lastAcceptingState = 0  # the last state, kept for printing
    
    print("INFO Lexer - Lexing program ",programCount,"...")
    #with open(self.fileName) as f:
    currentChar = self.contents[0] # initialize the first character
    #  while True:
    while(self.currentPos < len(self.contents)):
   
      # update the current character and its position
      currentChar = self.contents[self.currentPos]
      index = self.getIndexFromChar(currentChar)
      #print("index:",index)
      # when there is an unrecognized token, we gotta just move right past it, but with a report of course
      if index is None and lastPosition == self.currentPos:
        print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
        errorCount += 1
        # watch out for an error right at the end!
        if(self.currentPos < len(self.contents)-1):
          lastPosition += 1
          self.currentPos += 1
          self.linePos += 1
          currentChar = self.contents[self.currentPos]
          index = self.getIndexFromChar(currentChar)
        else:
          index = 46
        
      if(currentChar == "\n"):
        self.lineNum += 1
        self.linePos = 0
      self.currentPos += 1
      self.linePos += 1
        
      #print("index:",index)
      # update the states
      
        
      nextState = self.DFATable[state][index]
      #print("\nCurrentChar : " ,currentChar ,"\nCurrent state: " ,state,"\nNext State: ",nextState, "\ncurrentPos: ",self.currentPos)
      state = nextState
      
      #print("inQuotes = ",inQuotes)
      
      if(inQuotes):
        state = 31
      
      if(index < 26 and lastAcceptingState == 0 and inQuotes == False):
        lastAcceptingState = 34
        lastPosition = self.currentPos
        #print("lastAccepting: ",lastAcceptingState,"lastPosition:",lastPosition," currentChar: ",self.contents[lastPosition-1])
      #print("lastPos:",lastPosition,"\n")
      
      if(state in self.accepting):
        # store the located state, and keep looking
        #print("ACCEPTABLE: ",state)
        if(inQuotes == False and currentChar == '"'):
          inQuotes = True
          #print("ENTER QUOTES")
        elif(inQuotes == True and currentChar == '"'):
          inQuotes = False
          #print("EXIT QUOTES")
          state = 15
          
        if(not lastAcceptingState in self.keywords):
          #print("looking for the first state")
          #print('last positioin:',lastPosition)
          #print(self.accepting[state][1][0]," == ",self.contents[lastPosition-1])
          # found a keyword
          if(state in self.keywords and self.accepting[state][1][0] == self.contents[lastPosition-1]): 
            #print("---keyword found at ", self.currentPos)
            lastAcceptingState = state
            lastPosition = self.currentPos
          else:
            #print("else1")
            # found an id
            if(index < 26 and inQuotes == False): 
              #print("--found an id at ", lastPosition)
              lastAcceptingState = 34
            else:
              #print('else2')
              # found a symbol
              if(lastAcceptingState != 34):
                #print('else3')
                if(currentChar in self.symbols): 
                  #print("-found a symbol at ", self.currentPos)
                  lastAcceptingState = state
                  lastPosition = self.currentPos
                else:
                  # found a digit
                  if(state == 14): 
                    #print("f0und a d1g1t at ", self.currentPos)
                    lastAcceptingState = state
                    lastPosition = self.currentPos
                  elif(state == 31):
                    #print("found a CHARACTER at", self.currentPos)
                    lastAcceptingState = state
                    lastPosition = self.currentPos
        
        #print("current char: "+currentChar)
        #print("lastPosition: ",lastPosition)
        
      if((currentChar in self.symbols or inQuotes) or state == 14):
        # consume + emit found
        if(lastAcceptingState == 31 or lastAcceptingState == 14 or lastAcceptingState == 34): # char found
          #print("lastPos[]: "+self.contents[lastPosition-1])
          print("DEBUG  Lexer - "+self.accepting[lastAcceptingState][0]+" [ "+self.contents[lastPosition-1]+" ] found at (",self.lineNum,":",self.linePos,")")
        elif(lastAcceptingState == 6): # EoP symbol found
          print("DEBUG  Lexer - "+self.accepting[lastAcceptingState][0]+" [ "+currentChar+" ] found at (",self.lineNum,":",self.linePos,")")
          if(errorCount == 0):
            print("INFO Lexer - Lex completed with 0 errors\n\n")
          else:
            print("ERROR Lexer - Lex failed with ",errorCount," error(s)\n\n")
          programCount += 1
          errorCount = 0
          # ended in a comment
          if(programCount <= self.totalPrograms):
            print("INFO Lexer - Lexing program ",programCount,"...")
        else:
          print("DEBUG  Lexer - "+self.accepting[lastAcceptingState][0]+" [ "+self.accepting[lastAcceptingState][1]+" ] found at (",self.lineNum,":",self.linePos,")")
        #print()
        # reset the pointers
        self.currentPos = lastPosition
        self.linePos = lastPosition
        state = 0
        lastAcceptingState = 0
        
    # End of File - if a program is missing the EoP token, the lexer knows
    #print(programCount)
    #print(self.totalPrograms)
    if(programCount > self.totalPrograms):
      print("WARNING Lexer - (",self.lineNum,":",self.linePos,") End of Program symbol missing")
      print("INFO Lexer - Lex completed with ",errorCount," errors\n\n")
    
    print("\nEoF")
    
    
    
    
        # if(not lastAcceptingState in self.keywords and self.currentPos > lastPosition and lastAcceptingState == 0): # the first keyword has priority
          # print("--first keyword found at ", self.currentPos)
          # lastAcceptingState = state
          # lastPosition = self.currentPos
        # elif(not state in self.symbols and self.getIndexFromChar(currentChar) < 26):   # any other tokens
          # print("-found an id at ", self.currentPos)
          # lastAcceptingState = 34
          # lastPosition = self.currentPos
        # else:
          # print("found something ElSeE at ", self.currentPos)
          # lastAcceptingState = state
          # lastPosition = self.currentPos
    # else:
      # print("DEBUG  Lexer - "+self.accepting[6][0]+" [ "+self.accepting[6][1]+" ] found at (",self.lineNum,":",self.linePos,")")