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
    node = Node(name)
    if self.root is None and not self.root:
      # we are the root node rn
      self.root = node
      print("rooted")
    else:
      # we a kid
      self.current.children.append(node)
      node.parent = self.current
      print("CURRENT:",self.current.name)
      print("PARENT of NODE:",node.parent.name)
      print("NODE:",node.name)
      print("Kids of ",self.current.name,"++++++++")
      for z in self.current.children:
        print("<",z.name,">")
    
    # if we are an interior node
    if kind is "branch":
      # update the current node pointer to ourselves
      self.current = node
      if self.current.name:
        print("BRanch to ",self.current.name)
    
    
      
  def returnToParent(self):
    # move up to the parent node when we're done with this branch
    if self.current.parent is not None:
      #print("returnToParent: from",self.current.name," to",self.current.parent.name)
      self.current = self.current.parent
    else:
      # error logging
      print("Unable to return to parent node of", self.current.name)
      
  # method to print the tree
  def toString(self):
    # initial call to expand
    self.expand(self.root, 0)
    return self.result
    
  # recursive function to handle the expansion of the nodes
  def expand(self, node, depth):
    # add depth
    for x in range(depth):
      self.result += "-"
    print("DEPTH: ",depth)
    print("  RESULT: "+self.result)
    for a in node.children: 
      print(a.name)
    # no children/leaf nodes
    if len(node.children) is 0: #not node.children or 
      self.result += "["+node.name+"]"
      self.result += "\n"
    # there are children so note these interior nodes and expand them
    else:
      self.result += "<"+node.name+">"
      for i in range(len(node.children)):
        self.expand(node.children[i], depth + 1)
    
    
class Node():
  # Node class holds information about the token to 
  # be used in the construction of a CST
  def __init__(n, name="", children=[], parent=None):
    n.name = name
    n.children = children
    n.parent = parent

