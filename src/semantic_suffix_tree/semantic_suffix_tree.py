from src.semantic_suffix_tree.suffix_node import SuffixNode

class SemanticSuffixTree:
  def __init__(self, documents):
    self.documents = documents

  def build_semantic_suffix_tree(self):
    root = SuffixNode("root", 0)
    return root