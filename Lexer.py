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
      34: ["A_STMT", '='],      # =
      26: ["BOOLOP",'!='], # != | ==
      27: ["S_TYPE", 'string'], # string
      28: ["I_STMT", 'if'],     # if
      29: ["B_TYPE", 'boolean'],# boolean
      30: ["B_VAL",'false'],    # false
      31: ["CHAR", 'a'],        # a-z 
      32: ["B_VAL",'true'],     # true
      33: ["BOOLOP",'=='],      # ==
      35: ["ID", 'a']           # single char id
    }
    # a list of the keywords available in the grammar
    self.keywords = [11,20,23,27,28,29,30,32]
    # a list of available symbols to stop at when lexing
    self.symbols = [1,4,5,6,12,13,15,26,33,34]
    
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
      [ 0, 0, 0, 0,32, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #8  - r
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
      [34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34, 2,34,33,34,34,34,34,34,34],  #24 - =
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,26, 0, 0, 0, 0, 0, 0],  #25 - !
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #26 - != accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #27 - string accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #28 - if accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #29 - boolean accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #30 - false accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #31 - char accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #32 - true accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #33 - == accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #34 - = (assignment) accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  #35 - ID accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   #36 - ERROR STATE
      ]
    
    self.fileName = fileName
      
  def getFile(self):
    # method for processing the test data file
    # reads file contents into a string
    file = open(self.fileName, "r")
    self.contents = file.read()
    
    # remove comments - nvm
    # self.contents = re.sub('/\*.*?\*/', '', self.contents, flags= re.S)
    print(self.contents+"\n---------------------------------------------------------------------------\n")
    
    # used for keeping track of when to stop printing INFO statements
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
  # search through a file and pick out and print tokens from the grammar
  # initialize variables
    errorCount = 0    # counter for errors
    programCount = 1  # counter for INFO statements
    state = 0         # the current state occupied in the DFA table
    nextState = 0     # used to view the next state as well as move there
    currentChar = ""  # the character currently being examined
    index = 0         # the location in the DFA Table of the current character (if it has one)
    inQuotes = False  # all characters read until the next " are marked as char
    nextJump = 0      # used to determine if we should keep going or just accept the ID as an ID
    inComment = False
    
    # variables for greedy algorithm
    lastPosition = 0        # the location of the last character that was recognized as a token
    lastAcceptingState = 0  # the last state, kept for printing
    
    print("INFO Lexer - Lexing program ",programCount,"...")
    currentChar = self.contents[0]
    
    while(self.currentPos < len(self.contents)):
    # loop while the program has not reached the end of the file string
    
      # update the current character and its position
      currentChar = self.contents[self.currentPos]
      index = self.getIndexFromChar(currentChar)
      #print("index: ",index)
      
      #print("Current Char: ",currentChar," lastPosition: ",lastPosition," CurrentPos: ", self.currentPos)
      # when there is an unrecognized token, we gotta just move right past it, but with a report of course
      if index is None:
        #if lastPosition == self.currentPos:
        print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
        errorCount += 1
        # watch out for an error right at the end!
        if(self.currentPos == len(self.contents)-1):
          #print("last in the file?")
          lastPosition += 1
          self.currentPos += 1
          self.linePos += 1
          currentChar = self.contents[self.currentPos]
          index = self.getIndexFromChar(currentChar)
        # otherwise just ignore
        else:
          index = 46
      elif index is 43 and self.contents[self.currentPos+1] is not "=":
        print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
        errorCount += 1
      elif index is 41 and self.contents[self.currentPos+1] is not "/" and self.contents[self.currentPos-1] is not "/":
        print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
        errorCount += 1
        
      
      # increase the current line position for printing
      if(currentChar == "\n"):
        #print("New Line!")
        self.lineNum += 1
        self.linePos = 0
      self.currentPos += 1
      self.linePos += 1
      
      #print("State before update: ",state)
      # update the states
      state = self.DFATable[state][index]
      #print("State: ",state)
      # we need the nextJump to determine later on if its worth continuing greedy grabs
      if self.currentPos < len(self.contents):
        nextJump = self.DFATable[state][self.getIndexFromChar(self.contents[self.currentPos])]
      
      # if quotes are active, everything is a char until the next quote unless not in the language
      if inQuotes:
        if currentChar == '"':
          state = 15
        elif index > 25 and index != 46:
          print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Character: ",currentChar)
          errorCount += 1
          state = 36
        elif index is 40 and self.getIndexFromChar(self.contents[self.currentPos + 1]) is 41:
          inComment = True
        else:  
          state = 31
        
      if inComment:
        state = 3
        #print("STILL in comment")
      # issa comment boiii
      #if state is 2 and nextJump is 3:
      if index is 40 and self.getIndexFromChar(self.contents[self.currentPos + 1]) is 41:
        inComment = True
        state = 3
        #print("COMMMMMMENT")
      # no more comment sonn
      #elif inComment and state is 3 and nextJump is 2:
      elif inComment and index is 41 and self.getIndexFromChar(self.contents[self.currentPos + 1]) is 40:
        inComment = False
        state = 0
       # print("END COMMENT")
      
      # assume the first character we see is an id until proven otherwise
      if(index < 26 and lastAcceptingState is 0 and inQuotes is False and inComment is False):
        lastAcceptingState = 35
        lastPosition = self.currentPos
      
      
      # determine if the lastAcceptingState we have is the best one
      if(state in self.accepting or lastAcceptingState == 35):
      
        # this is within accepting states because it might effect a string if it came before
        if(inQuotes == False and currentChar == '"'):
          inQuotes = True
          #print("entered QUOTES")
        elif(inQuotes == True and currentChar == '"'):
          inQuotes = False 
          state = 15
          #print("exit QUOTES")
          
        # a keyword is preferable, so if it already happened, we don't need a new one
        if(not lastAcceptingState in self.keywords):
          # found a keyword that matched the first char of the current grouping
          if(state in self.keywords and self.accepting[state][1][0] == self.contents[lastPosition-1]):
            lastAcceptingState = state
            lastPosition = self.currentPos
            #print("LastPos:",lastPosition)
            #print("Accepted Keyword")
            state = 0
          else:
            # found an id
            if(index < 26 and inQuotes == False): 
              #print("--found an id at ", lastPosition)
              lastAcceptingState = 35
              # we want to go to 0 in case this ID is also the begining of a keyword
              # this accomplishes less useless processing until reaching a symbol
              if nextJump is 0:
                state = 0
              #print("Accepted ID")
            else:
              # found a symbol
              if(state in self.symbols and lastAcceptingState != 35):
                lastAcceptingState = state
                lastPosition = self.currentPos
                #print("Accepted Symbol")
              else:
                # found a digit
                if(state == 14):
                  lastAcceptingState = state
                  lastPosition = self.currentPos
                  #print("Accepted Digit")
                # found a char
                elif(state == 31):
                  lastAcceptingState = state
                  lastPosition = self.currentPos
                  #print("Accepted Char")
        
        
      if(state in self.symbols or state == 31 or state == 14):
        # consume + emit found
        #print("symbol found, processing token")
        # CHAR, DIGIT, and ID get special printing since they are ranges
        if(lastAcceptingState == 31 or lastAcceptingState == 14 or lastAcceptingState == 35):
          print("DEBUG  Lexer - "+self.accepting[lastAcceptingState][0]+" [ "+self.contents[lastPosition-1]+" ] found at (",self.lineNum,":",self.linePos,")")
        # EoP symbol found
        elif(lastAcceptingState == 6): 
          print("DEBUG  Lexer - "+self.accepting[lastAcceptingState][0]+" [ "+currentChar+" ] found at (",self.lineNum,":",self.linePos,")")
          if(errorCount == 0):
            print("INFO Lexer - Lex completed with 0 errors\n\n")
          else:
            print("ERROR Lexer - Lex failed with ",errorCount," error(s)\n\n")
          errorCount = 0
          programCount += 1
          # watch out for no more programs
          if(programCount >= self.totalPrograms and self.contents[len(self.contents)-1] != '$'):
            print("INFO Lexer - Lexing program ",programCount,"...")
        else:
          print("DEBUG  Lexer - "+self.accepting[lastAcceptingState][0]+" [ "+self.accepting[lastAcceptingState][1]+" ] found at (",self.lineNum,":",self.linePos,")")
          
        # reset the pointers
        self.currentPos = lastPosition
        state = 0
        lastAcceptingState = 0
        
      #print()
        
    # End of File - if a program is missing the EoP token, the lexer knows
    if(self.contents[len(self.contents)-1] != '$'):
      print("WARNING Lexer - Warning:",self.lineNum,":",self.linePos," End of Program symbol missing: $")
      print("INFO Lexer - Lex completed with ",errorCount," errors\n\n")
    elif inQuotes:
      print("ERROR Lexer - Error: End Quote Missing")
      errorCount += 1
      print("INFO Lexer - Lex completed with ",errorCount," errors\n\n")
    
    print("\nEoF")