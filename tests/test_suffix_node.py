import pytest
from src.semantic_suffix_tree.suffix_node import SuffixNode

def test_return_node():
  node = SuffixNode("root", 0)
  expected_result = { "name": "root", "index": 0, "parent": None }
  assert node.print_node() == expected_result, "Should return node properties"

def test_has_children():
  root = SuffixNode("root", 0)
  child = SuffixNode("child", 1, root)
  root.add_children(child)
  assert root.has_children() == True, "Should return true when there is children"