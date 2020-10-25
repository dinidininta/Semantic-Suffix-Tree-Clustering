class Node:
  def __init__(self, name, index, parent = None):
    self.name = name
    self.index = index
    self.parent = parent
    self.children = []

  def print_node(self):
    printed_children = []
    if(len(self.children) > 0):
      for child in self.children:
        printed_child = child.print_node()
        printed_children.append(printed_child)
    return dict(name = self.name, children = printed_children)

  def add_children(self, child):
    self.children.append(child)
  
  def has_children(self):
    return len(self.children) > 0
  
  def has_parent(self):
    return self.parent is not None