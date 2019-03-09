# Alexis Dionne
# Compiler Project 2 - Treeee
# 3/9/19

def Node():
  def __init__(self, name="", children=[], parent=None):
    self.name = name
    self.children = children
    self.parent = parent

def Tree():

  def __init__(self):
    self.root = None
    self.current = None
    
  def addNode(name, kind):
    node = Node(name)
    if self.root is None or not self.root:
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
      
  def returnToParent():
    # move up to the parent node when we're done with this branch
    if self.current.parent is not None and self.current.parent.name is not None:
      self.current = self.current.parent
    else:
      # error logging
      print("Unable to return to parent node of", self.current.name)
      
  # method to print the tree
  def toString():
    # initialize the result string
    result = ""
    
    # recursive function to handle the expansion of the nodes
    def expand(node, depth):
      # add depth
      for x in range(depth):
        result += "-"
      
      # no children/leaf nodes
      if not node.children or node.children.length is 0
        result += "["+node.name+"]"
        result += "\n"
      # there are children so note these interior nodes and expand them
      else:
        result += "<"+node.name+">"
        for x in range(node.children.length):
          expand(node.children[x], depth + 1)
    
    # initial call to expand
    expand(self.root, 0)
    return result