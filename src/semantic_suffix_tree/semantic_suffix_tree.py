from src.semantic_suffix_tree.node import Node
from src.semantic_suffix_tree.suffix_nodes import SuffixNodes

class SemanticSuffixTree:
  def __init__(self, documents):
    self.documents = documents

  def build_semantic_suffix_tree(self):
    root = None
    documents_amount = len(self.documents)
    if(documents_amount > 0):
      root = Node("root", 0)
      tree = SuffixNodes()
      tree.append_node(root)
      
      for id_, document in enumerate(self.documents):
        for word in document:
          node = Node(word, id_, root)
          tree.append_node(node)
    return root