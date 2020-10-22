from src.semantic_suffix_tree.suffix_node import SuffixNode

class SemanticSuffixTree:
  def __init__(self, documents):
    self.documents = documents

  def get_semantic_suffix_tree(self):
    root = SuffixNode("root", 0)
    return { "name": "root", "index": 0, "parent": None }