from semantic_suffix_tree.synonyms import dictionary

class SemanticSimilarity:
  def __init__(self, wa, wb):
    self.wa = wa
    self.wb = wb

  def get_semantic_similarity(self):
    wa_synonyms = dictionary[self.wa]
    wb_synonyms = dictionary[self.wb]
    synset = wa_synonyms.intersection(wb_synonyms)
    if(len(synset) >= 1):
      return True
    return False