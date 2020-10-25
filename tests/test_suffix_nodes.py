import pytest
from src.semantic_suffix_tree.node import Node
from src.semantic_suffix_tree.suffix_nodes import SuffixNodes

def test_root_has_children():
  tree = SuffixNodes()
  root = Node('root', 0, None)
  tree.append_node(root)
  child = Node('child', 1, root)
  tree.append_node(child)

  assert root.has_children() == True, "Should return True when root has a child"

def test_child_has_children():
  tree = SuffixNodes()
  root = Node('root', 0, None)
  tree.append_node(root)
  child = Node('child', 1, root)
  tree.append_node(child)
  grand_child = Node('grand_child', 2, child)
  tree.append_node(grand_child)

  assert child.has_children() == True, "Should return True when child has a child"

def test_print_tree():
  root = Node('root', 0, None)
  child = Node('child', 1, root)
  second_child = Node('second_child', 2, root)
  expected_result = { 
    "name": "root",
    "children": [
      { "name": "child", "children": [] },
      { "name": "second_child", "children": [] }
    ]
  }

  tree = SuffixNodes()
  tree.append_node(root)
  tree.append_node(child)
  tree.append_node(second_child)

  assert root.print_node() == expected_result, "Should printed tree"
