class Node:
  def __init__(self, name, index, parent = None):
    self.name = name
    self.index = index
    self.parent = parent
    self.children = []

  def print_node(self):
    return dict(name = self.name, index = self.index, parent = self.parent, children = self.children)

  def add_children(self, child):
    self.children.append(child)
  
  def has_children(self):
    return len(self.children) > 0