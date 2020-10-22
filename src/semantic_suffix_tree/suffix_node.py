class SuffixNode:
  def __init__(self, name, index, parent = None):
    self.name = name
    self.index = index
    self.parent = parent

  def print_node(self):
    return dict(name = self.name, index = self.index, parent = self.parent)