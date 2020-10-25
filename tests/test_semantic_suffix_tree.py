import pytest
from src.semantic_suffix_tree.semantic_suffix_tree import SemanticSuffixTree
from src.semantic_suffix_tree.node import Node

def test_return_none():
  documents = []
  suffixTree = SemanticSuffixTree(documents)
  assert suffixTree.build_semantic_suffix_tree() == None, "Should return none when there is no document"

def test_return_first_tree():
  expected_result = { 
    "name": "root", 
    "children": [
      { "name": "cat", "children": [] }
    ]
  }
  document = ["cat"]
  documents = [document]
  suffixTree = SemanticSuffixTree(documents)

  assert suffixTree.build_semantic_suffix_tree().print_node() == expected_result, "Should return first tree branch when there is one document with one word"
