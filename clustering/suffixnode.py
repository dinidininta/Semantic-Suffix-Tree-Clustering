from anytree import NodeMixin


class SuffixNode(NodeMixin):
    def __init__(self, name, index, parent=None):
        self.name = name
        self.parent = parent
        self.index = index
        self.suffix_link = None
        self.doc = []

        # if suffix_link is not None:
        #     self.suffix_link = suffix_link
        # else:
        #     self.suffix_link = self

    def add_suffix_link(self, node2):
        self.suffix_link = node2

    def has_suffix_link(self):
        if self.suffix_link is None:
            return False
        else:
            return True

    def get_index_suffix_link(self):
        if self.suffix_link is None:
            return "None"
        else:
            return self.suffix_link.index

    def get_suffix_link(self):
        return self.suffix_link

    def insert_doc(self, doc):
        if doc not in self.doc:
            self.doc.append(doc)
