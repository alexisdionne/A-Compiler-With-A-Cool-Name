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
    self.programCount = 1
    # A most recent full match
    self.lastPosition = 0
    
    # accepting states 
    # if state in accepting
    #self.accepting = [1,4,5,6,11]
    self.accepting = {
      1 : "INTOP",    # +
      4 : "L_BRACE",  # [
      5 : "R_BRACE",  # ]
      6 : "EOP",      # $
      11: "P_STMT",   # print
      12: "L_PAREN",  # (
      13: "R_PAREN",  # )
      14: "DIGIT",    # 0-9
      15: "QUOTE",    # "
      20: "W_STMT",   # while
      23: "I_TYPE",   # int
      27: "S_TYPE",   # string
      28: "I_STMT",   # if
      29: "B_TYPE",   # boolean
      30: "B_VAL"     # false | true
    }
    
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
      [16, 0, 0, 0,30, 0,27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #10 - n
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
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,26, 0, 0, 0, 0, 0, 0],  #24 - = (assignment) accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,26, 0, 0, 0, 0, 0, 0],  #25 - !
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #26 - != & == accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #27 - string accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #28 - if accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #29 - boolean accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #30 - false accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    
    self.fileName = fileName
      
  def getFile(self):
    file = open(self.fileName, "r")
    print ("Printing all contents")
    print (file.read())
    
  def getIndexFromChar(self, c):
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
    state = 0
    nextState = 0
    currentChar = ""
    index = 0
    errorCount = 0
    programCount = 1
    print("INFO Lexer - Lexing program ",programCount,"...")
    with open(self.fileName) as f:
      currentChar = f.read(1) # initialize the first character
      while True:
      
        if(currentChar == "\n"):
          self.lineNum += 1
          self.currentPos = 0
        else:
          self.currentPos += 1
          
        # tell the compiler to not worry at all about the letters it doesn't know
        index = self.getIndexFromChar(currentChar)
        if(state == 3 and index != 41):
          index = 46 # a recognized character ' ' so the compiler doesn't throw an error
          
        #print("index:",index)
        nextState = self.DFATable[state][index]
        #print("CurrentChar : " ,currentChar ,"\nCurrent state: " ,state,"\nNext State: ",nextState, "\n")
        state = nextState
        
        if(state in self.accepting):
          print("DEBUG  Lexer - "+self.accepting.get(state)+" [ "+currentChar+" ] found at (",self.lineNum,":",self.currentPos,")")
          if(state == 6):
            print("INFO Lexer - Lex completed with ",errorCount," errors\n\n")
            programCount += 1
            errorCount = 0
            if f.read(1):
              print("INFO Lexer - Lexing program ",programCount,"...")
          state = 0
          
        if(currentChar != '$' and not f.tell()):
          print("WARNING Lexer - (",self.lineNum,":",self.currentPos,") End of Program symbol missing")
          
        currentChar = f.read(1)
        
        if not currentChar:
          print("EoF")
          break