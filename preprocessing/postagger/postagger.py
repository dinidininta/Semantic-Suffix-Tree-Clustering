from hmmtagger import MainTagger
from tokenization import *
import re


class Postagger:
    def __init__(self):
        self.NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
        self.VERBS = ['VB', 'VBG', 'VBN', 'VBP', 'VBT', 'VBI']
        self.PREPS = ['PRP', 'PRP$']

    def postag(self, sentences):
        lines = sentences.split()
        result = []
        try:
            mt = MainTagger('preprocessing/postagger/hmmtagger/resource/Lexicon.trn',
                            'preprocessing/postagger/hmmtagger/resource/Ngram.trn',
                            0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)
            for l in lines:
                # print l
                if len(l) == 0: continue
                result += mt.taggingStr(l)
        except Exception as e:
            print e
            return "Error exception at POS Tagger"
        return result

    def extract_svo(self, sentence):
        snippets = ""
        tagged = self.postag(sentence)
        for word in tagged:
            tag = re.sub('.*/', '', word)
            # print tag
            if tag in self.NOUNS or tag in self.VERBS or tag in self.PREPS:
                word = re.sub('/.*', '', word)
                snippets = snippets + " " + word
        return snippets[1:]


if __name__ == '__main__':
    # tagged = " ".join(Postagger().postag("aku itu adalah sampah"))
    # print Postagger().postag("aku itu adalah sampah")
    print Postagger().extract_svo("kucing itu makan keju")
