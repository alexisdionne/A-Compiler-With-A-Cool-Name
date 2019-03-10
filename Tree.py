# Alexis Dionne
# Compiler Project 2 - Treeee
# 3/9/19


class Tree():
  # Tree to map out CST of a program
  def __init__(self):
    self.root = Node()
    self.current = Node()
    
  def addNode(self, name, kind):
    node = Node(name)
    if self.root.name is "":
      # we are the root node rn
      self.root = node
    else:
      # we a kid
      node.parent = self.current
      self.current.children.append(node)
    
    # if we are an interior node
    if kind is "branch":
      # update the current node pointer to ourselves
      self.current = node
      
  def returnToParent(self):
    # move up to the parent node when we're done with this branch
    if self.current.parent is not None and self.current.parent.name is not None:
      self.current = self.current.parent
    else:
      # error logging
      print("Unable to return to parent node of", self.current.name)
      
  # method to print the tree
  def toString(self):
    # initialize the result string
    result = ""
    
    # recursive function to handle the expansion of the nodes
    def expand(node, depth):
      # add depth
      for x in range(depth):
        result += "-"
      
      # no children/leaf nodes
      if not node.children or len(node.children) is 0:
        result += "["+node.name+"]"
        result += "\n"
      # there are children so note these interior nodes and expand them
      else:
        result += "<"+node.name+">"
        for x in range(len(node.children)):
          expand(node.children[x], depth + 1)
    
    # initial call to expand
    expand(self.root, 0)
    return result
    
    
class Node():
  # Node class holds information about the token to 
  # be used in the construction of a CST
  def __init__(self, name="", children=[], parent=None):
    self.name = name
    self.children = children
    self.parent = parent

