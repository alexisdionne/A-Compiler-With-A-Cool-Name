# Alexis Dionne
# Compiler Project 1 - Lex
# 2/6/19
import re
from Token import Token
from Parser import Parser

class Lexer:
  # Lexer contains all methods and 
  # attributes for the lexer of the compiler
  
  def __init__(self, fileName=""):
    # Each lexer has a line and character position
    self.lineNum = 1    # keeps track of what line in the file we're on
    self.currentPos = 0 # keeps track of place in string of input
    self.linePos = 0    # keeps track of location in regards to the program structure
    self.contents = ""
    self.totalPrograms = 1
    
    self.tokens = []
    
    # accepting states available to identify tokens
    self.accepting = {
      1 : ["INTOP",  '+'],      # +
      4 : ["L_BRACE",'{'],      # {
      5 : ["R_BRACE",'}'],      # }
      6 : ["EOP",    '$'],      # $
      11: ["P_STMT", 'print'],  # print
      12: ["L_PAREN",'('],      # (
      13: ["R_PAREN",')'],      # )
      14: ["DIGIT",  '0'],      # 0-9 
      15: ["QUOTE",  '"'],      # "
      20: ["W_STMT", 'while'],  # while
      23: ["TYPE",   'int'],    # int
      24: ["A_STMT", '='],      # =
      26: ["BOOLOP", '!='],     # != | ==
      27: ["TYPE",   'string'], # string
      28: ["I_STMT", 'if'],     # if
      29: ["TYPE",   'boolean'],# boolean
      30: ["B_VAL",  'false'],  # false
      31: ["CHAR",   'a'],      # a-z 
      32: ["B_VAL",  'true'],   # true
      33: ["BOOLOP", '=='],     # ==
      35: ["ID",     'a'],      # single char id
      36: ["SPACE",  ' ']       # a space character
    }
    # a list of the keywords available in the grammar
    self.keywords = [11,20,23,27,28,29,30,32]
    # a list of available symbols to stop at when lexing
    self.symbols = [1,4,5,6,12,13,15,24,26,33]
    
    # 0 indicates an error state
    # go to state 2 if a / is found to check for * in any other state as comments may appear anywhere
    # all characters have the same accepting state, and need to be checked for a follow up char
    self.DFATable = [
    # [ a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, {, }, (, ), /, *, =, !, +, $,  ,\n, ",''],
      [ 0, 2, 0, 0, 0, 2, 0, 0,21, 0, 0, 0, 0, 0, 0, 7, 0, 0, 2, 2, 0, 0,16, 0, 0, 0,14,14,14,14,14,14,14,14,14,14, 4, 5,12,13, 0, 0,24,25, 1, 6, 0, 0,15, 0],  #0
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #1  - + accepting state
      [16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],  #2  - going into comment - s -> t
      [ 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3],  #3  - comment found
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #4  - { accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #5  - } accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #6  - $ accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 8, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #7  - p
      [ 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #8  - r
      [ 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #9  - i
      [16, 0, 0, 0,32, 0,27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #10 - n
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #11 - t - print accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #12 - ( accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #13 - ) accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #14 - digit accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #15 - " accepting state
      [ 0, 0, 0, 0, 0, 0, 0,17, 0, 0, 0,17, 0,29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #16 - w
      [ 0, 0, 0, 0, 0, 0, 0, 0,18, 0, 0, 0, 0, 0, 0, 0, 0, 0,18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #17 - h
      [ 0, 0, 0, 0,30, 0, 0, 0, 0, 0, 0,19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #18 - i
      [ 0, 0, 0, 0,20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #19 - l
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #20 - e - while accepting state
      [ 0, 0, 0, 0, 0,28, 0, 0, 0, 0, 0, 0, 0,22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #21 - i
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #22 - n 
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #23 - t - int accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,33, 0, 0, 0, 0, 0, 0, 0],  #24 - =
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,26, 0, 0, 0, 0, 0, 0, 0],  #25 - !
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #26 - != accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #27 - string accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #28 - if accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #29 - boolean accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #30 - false accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #31 - char accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #32 - true accepting state 
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #33 - == accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #34 - = (assignment) accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #35 - ID accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #36 - space accepting state
      [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   #37 - ERROR state
      ]
    
    self.fileName = fileName
      
  def getFile(self):
    # method for processing the test data file
    # reads file contents into a string
    file = open(self.fileName, "r")
    self.contents = file.read()
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
      '"' : 48,
      '' : 49
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
    
    
    # check for an empty string
    if len(self.contents) is not 0:
      currentChar = self.contents[0]
      print("INFO Lexer - Lexing program ",programCount,"...")
      
      while(self.currentPos < len(self.contents)):
      # loop while the program has not reached the end of the file string
      
        # update the current character and its position
        currentChar = self.contents[self.currentPos]
        index = self.getIndexFromChar(currentChar)
        
        
        #print("Current Char: ",currentChar," lastPosition: ",lastPosition," CurrentPos: ", self.currentPos)
        # when there is an unrecognized token, we gotta just move right past it, but with a report of course
        if index is None and not inComment:
          #if lastPosition == self.currentPos:
          print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
          errorCount += 1
          # watch out for an error right at the end!
          if self.currentPos is len(self.contents):
            print("last in the file?")
            lastPosition += 1
            self.currentPos += 1
            self.linePos += 1
            currentChar = self.contents[self.currentPos]
            index = self.getIndexFromChar(currentChar)
          # otherwise just ignore
          else:
            index = 49
        elif index is 43 and self.contents[self.currentPos+1] is not "=":
          print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
          errorCount += 1
        elif index is 41 and self.contents[self.currentPos+1] is not "/" and self.contents[self.currentPos-1] is not "/":
          print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Token: "+currentChar)
          errorCount += 1
        elif inComment and index is None:
          index = 49
          
        
        # increase the current string pointers
        self.currentPos += 1
        self.linePos += 1
        
        # update the states
        state = self.DFATable[state][index]
        if self.currentPos < len(self.contents) and self.getIndexFromChar(self.contents[self.currentPos]) is not None:
          nextState = self.DFATable[state][self.getIndexFromChar(self.contents[self.currentPos])]
        
        # determine if we are entering or in a comment and change state accordingly
        if self.currentPos < len(self.contents) and currentChar is "/" and self.contents[self.currentPos] is "*":
          if lastAcceptingState not in self.accepting:
            inComment = True
            state = 3
        elif inComment:
          state = 3
          
        # if quotes are active, everything is a char or space until the next quote unless not in the language
        if inQuotes and not inComment:
          if currentChar == '"':
            state = 15
          elif currentChar is "/" and self.contents[self.currentPos - 2] is "*":
            # just left a comment and now we gotta skip the /
            state = 3
          elif index > 25 and index != 49 and index != 46:
            print("ERROR Lexer - Error:",self.lineNum,":",self.linePos," Unrecognized Character: ",currentChar)
            errorCount += 1
            state = 37
          elif index is 49:
            state = 37
          elif index is 46:
            state = 36
          else:  
            state = 31
          
        # end of a comment
        if inComment and currentChar is "*" and self.contents[self.currentPos] is "/":
          inComment = False
          state = 0
        
        # assume the first character we see is an id until proven otherwise
        if(index < 26 and lastAcceptingState is 0 and inQuotes is False and inComment is False):
          lastAcceptingState = 35
          lastPosition = self.currentPos
          
        if nextState is 33:
          # look for a second = in the next place before moving on
          # to catch the == operator
          continue
          
        
        # determine if the lastAcceptingState we have is the best one
        if(state in self.accepting or lastAcceptingState is 35):
          
          # a keyword is preferable, so if it already happened, we don't need a new one
          if(not lastAcceptingState in self.keywords):
            # found a keyword that matched the first char of the current grouping
            if(state in self.keywords and self.accepting[state][1][0] == self.contents[lastPosition-1]):
              lastAcceptingState = state
              lastPosition = self.currentPos
              state = 0
            else:
              # found an id
              if(index < 26 and inQuotes == False): 
                lastAcceptingState = 35
                # we want to go to 0 in case this ID is also the begining of a keyword
                # this accomplishes less useless processing until reaching a symbol
                if self.currentPos < len(self.contents) and self.DFATable[state][self.getIndexFromChar(self.contents[self.currentPos])] is 0:
                  state = 0
              else:
                # found a symbol
                if(state in self.symbols and lastAcceptingState != 35):
                  lastAcceptingState = state
                  lastPosition = self.currentPos
                else:
                  # found a digit
                  if(state == 14):
                    lastAcceptingState = state
                    lastPosition = self.currentPos
                  # found a char or space
                  elif state is 31 or state is 36:
                    lastAcceptingState = state
                    lastPosition = self.currentPos
                    
        # this is within accepting states because it might effect a string if it came before
        if(inQuotes == False and lastAcceptingState is 15):
          inQuotes = True
        elif(inQuotes == True and lastAcceptingState is 15):
          inQuotes = False 
          state = 15
          
        # regex to get position in string more reliably
        if self.lineNum is not self.contents[0:lastPosition].count('\n') + 1:
          # we update lineNum and reset linePos because a new \n was found
          self.lineNum = self.contents[0:lastPosition].count('\n') + 1
          self.linePos = 1
          
          
        if(state in self.symbols or lastAcceptingState in [14,31,36] or lastAcceptingState in self.accepting and index is 40):
          # consume + emit found token
          # call parse if we found a valid $
          
          # CHAR, DIGIT, and ID get special printing since they are ranges
          if(lastAcceptingState in [14,31,35,36]):
            print("Lexer  DEBUG - "+self.accepting[lastAcceptingState][0]+" [ "+self.contents[lastPosition-1]+" ] found at (",self.lineNum,":",self.linePos,")")
            self.tokens.append(Token(self.lineNum, self.contents[lastPosition-1], self.accepting[lastAcceptingState][0]))
          # EoP symbol found
          elif(lastAcceptingState == 6): 
            print("Lexer  DEBUG - "+self.accepting[lastAcceptingState][0]+" [ "+currentChar+" ] found at (",self.lineNum,":",self.linePos,")")
            self.tokens.append(Token(self.lineNum, self.contents[lastPosition-1], self.accepting[lastAcceptingState][0]))
            if(errorCount == 0):
              print("Lexer  INFO - Lex completed with 0 errors\n")
              print("Parser INFO - Parsing program ",programCount,"...")
              # parse gets called here since Lex passed
              parseObj = Parser(self.tokens,programCount)
              parseObj.parseProgram()
              # clear the list of tokens for the next program
              self.tokens.clear()
              print("\n\n")
            else:
              print("Lexer  ERROR - Lex failed with ",errorCount," error(s)\n")
              # can't call parse because Lex is a failure
              print("Skipping Parse...\n\n")
            errorCount = 0
            programCount += 1
            # watch out for no more programs or a lack of an EoP at the end
            if programCount <= self.totalPrograms or lastPosition is not len(self.contents): 
              print("Lexer  INFO - Lexing program ",programCount,"...")
          else:
            print("Lexer  DEBUG - "+self.accepting[lastAcceptingState][0]+" [ "+self.accepting[lastAcceptingState][1]+" ] found at (",self.lineNum,":",self.linePos,")")
            self.tokens.append(Token(self.lineNum, self.accepting[lastAcceptingState][1], self.accepting[lastAcceptingState][0]))
          # reset the pointers
          self.currentPos = lastPosition
          state = 0
          lastAcceptingState = 0
        
        
      printOnceMore = False # will print one last info string if any of these fail
      # if we end while still in quotes - BIG ERROR
      if inQuotes:
        print("Lexer  ERROR - Error: Unterminated String")
        errorCount += 1
        printOnceMore = False
      # same bad stuff in a comment at the End of File
      elif inComment:
        print("Lexer  ERROR - Error: Unterminated Comment")
        errorCount += 1
        printOnceMore = False
      # End of File - if a program is missing the EoP token, the lexer knows
      elif(self.contents[lastPosition-1] != '$'):
        print("Lexer  WARNING - Warning:",self.lineNum,":",self.linePos," End of Program symbol missing: $")
        printOnceMore = True
        # since its just a warning, we add the EoP token so that the rest passes
        self.tokens.append(Token(self.lineNum, "$", "EoP"))
        
      # it was just the warning, so theres one more to parse
      if printOnceMore and errorCount is 0:
          print("Lexer  INFO - Lex completed with 0 errors\n")
          print("Parser INFO - Parsing program ",programCount,"...")
          
          parseObj = Parser(self.tokens,programCount)
          parseObj.parseProgram()
            
          self.tokens.clear()
          print("End of Parse")
      # the programmer didn't end something, so we tell them they failed
      elif printOnceMore and errorCount is not 0:
        print("Lexer  ERROR - Lex failed with ",errorCount," error(s)\n")
        print("Skipping Parse...\n")
      # reached the end of the file
      print("\nEoF")
    # self explanitory
    else:
      print("No programs exist")