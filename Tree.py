# Alexis Dionne
# Compiler Project 2 - Treeee
# 3/9/19

class Tree():
  # Tree to map out CST of a program
  def __init__(self):
    self.root = None
    self.current = None
    self.result = ""
    
  def addNode(self, name, kind):
    node = Node(name, [], None)
    if self.root is None and not self.root:
      # we are the root node rn
      self.root = node
    else:
      # we are a kid and by default a leaf unless branch is specified
      self.current.children.append(node)
      node.parent = self.current
      
    # if we are an interior node
    if kind is "branch":
      # update the current node pointer to ourselves
      self.current = node
      
  # same as addNode, but modified to have hash tables for scope
  def addHashNode(self, name, kind):
    node = HashNode(name, [], None, {})
    if self.root is None and not self.root:
      # we are the root node rn
      self.root = node
    else:
      # we are a kid and by default a leaf unless branch is specified
      self.current.children.append(node)
      node.parent = self.current
      
    # if we are an interior node
    if kind is "branch":
      # update the current node pointer to ourselves
      self.current = node
    
  
  def returnToParent(self):
    # move up to the parent node when we're done with this branch
    if self.current.parent is not None:
      self.current = self.current.parent
    elif self.root is not self.current:
      # error logging
      print("Unable to return to parent node of", self.current.name)
      
  # method to print the tree
  def toString(self):
    # initial call to expand
    self.expand(self.root, 0)
    return self.result
    
  # method to print the tree
  def hashToString(self):
    # initial call to expand
    self.result = "------------------------------------------------\n"+ "Name\tType\t Scope\tLine\tisInit\tisUsed\n" + "------------------------------------------------\n"
    self.hashExpand(self.root)
    return self.result
    
  # recursive function to handle the expansion of the nodes
  def expand(self, node, depth):
    # add depth
    for x in range(depth):
      self.result += "-"
    # no children/leaf nodes
    if len(node.children) is 0: #not node.children or 
      self.result += "["+node.name+"]"
      self.result += "\n"
    # there are children so note these interior nodes and expand them
    else:
      self.result += "<"+node.name+">\n"
      for i in range(len(node.children)):
        self.expand(node.children[i], depth + 1)
    
  # recursive function to print all the hash tables  
  def hashExpand(self, node):
    # no children/leaf nodes
    for i in node.hashTable:
      self.result += str(i) + "\t"
      self.result += str(node.hashTable[i][0]) + "\t "
      self.result += str(node.name) + "\t"
      self.result += "line#" + "\t"
      self.result += str(node.hashTable[i][1]) + "\t"
      self.result += str(node.hashTable[i][2]) + "\n"
    if len(node.children) is not 0: 
    # there are children so note these interior nodes and expand them
      for i in range(len(node.children)):
        self.hashExpand(node.children[i])
  
class Node():
  # Node class holds information about the token to 
  # be used in the construction of a CST
  def __init__(n, name="", children=[], parent=None):
    n.name = name
    n.children = children
    n.parent = parent

class HashNode():
  def __init__(h, name="", children=[], parent=None, hashTable={}):
    h.name = name
    h.children = children
    h.parent = parent
    h.hashTable = hashTable
    
  def addEntry(h, name, attributes):
    # add a hash table entry
    # attributes = [type, isInit, isUsed, value]
    if name not in h.hashTable:
      h.hashTable[name] = attributes
      return 'Success'
    else:
      return 'Fail'