import pytest
from src.semantic_suffix_tree.semantic_similarity import SemanticSimilarity

def test_return_true_when_similar():
  wa = "eat"
  wb = "ate"
  semanticSimilarity = SemanticSimilarity(wa, wb)
  assert semanticSimilarity.get_semantic_similarity() == True, "Should be true when wa is eat and wb is ate"

def test_return_false_when_not_similar():
  wa = "eat"
  wb = "drink"
  semanticSimilarity = SemanticSimilarity(wa, wb)
  assert semanticSimilarity.get_semantic_similarity() == False, "Should be false when wa is eat and wb is drink"