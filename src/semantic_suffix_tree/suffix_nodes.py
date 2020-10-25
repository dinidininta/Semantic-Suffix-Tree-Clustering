from src.semantic_suffix_tree.node import Node

class SuffixNodes:
  def __init__(self):
    self.nodes = []

  def append_node(self, node):
    self.nodes.append(node)
    if(node.has_parent()):
      parent = node.parent
      parent_id = self.nodes.index(parent)
      self.nodes[parent_id].add_children(node)
