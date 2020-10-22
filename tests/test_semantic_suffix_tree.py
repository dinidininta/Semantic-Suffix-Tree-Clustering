import pytest
from src.semantic_suffix_tree.semantic_suffix_tree import SemanticSuffixTree

def test_return_root_node():
  root = { "name": "root", "index": 0, "parent": None }
  document1 = [""]
  documents = [document1]
  suffixTree = SemanticSuffixTree(documents)
  assert suffixTree.get_semantic_suffix_tree() == root, "Should return root node if document length is more than 1"