import pytest
from src.semantic_suffix_tree.node import Node

def test_return_node():
  node = Node("root", 0)
  expected_result = { "name": "root", "index": 0, "parent": None, "children": [] }
  assert node.print_node() == expected_result, "Should return node properties"

def test_has_children():
  root = Node("root", 0)
  child = Node("child", 1, root)
  root.add_children(child)
  assert root.has_children() == True, "Should return true when there is children"

def test_has_no_children():
  root = Node("root", 0)
  assert root.has_children() == False, "Should return false when there is no children"

def test_has_parent():
  root = Node("root", 0)
  child = Node("child", 1, root)

  assert child.has_parent() == True, "Should return true when there is parent"
def test_has_no_parent():
  root = Node("root", 0)

  assert root.has_parent() == False, "Should return False when there is no parent"