from src.semantic_suffix_tree.node import Node

class SemanticSuffixTree:
  def __init__(self, documents):
    self.documents = documents

  def build_semantic_suffix_tree(self):
    root = Node("root", 0)
    return root