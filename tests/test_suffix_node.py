import pytest
from src.semantic_suffix_tree.suffix_node import SuffixNode

def test_return_node():
  node = SuffixNode("root", 0)
  expected_result = { "name": "root", "index": 0, "parent": None }
  assert node.print_node() == expected_result, "Should return node properties"