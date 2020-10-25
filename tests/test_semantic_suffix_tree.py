import pytest
from src.semantic_suffix_tree.semantic_suffix_tree import SemanticSuffixTree
from src.semantic_suffix_tree.node import Node

def test_return_root_node():
  expected_result = { "name": "root", "index": 0, "parent": None, "children": [] }
  document = [""]
  documents = [document]
  suffixTree = SemanticSuffixTree(documents)
  assert suffixTree.build_semantic_suffix_tree().print_node() == expected_result, "Should return only root node when there is only empty document"