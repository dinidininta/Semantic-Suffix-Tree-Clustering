from clustering.semanticsuffixtreeclustering import SemanticSuffixTreeClustering

if __name__ == '__main__':
    documents = ["alat pernapasan", "alat peredaran darah", "alat pencernaan"]
    sstc = SemanticSuffixTreeClustering(documents)
    sstc.print_semantic_suffix_tree()
    print "\nCluster:"
    for c in sstc.get_clusters():
        print "%s : %s" % (c.label, "; ".join([str(cd) for cd in c.documents]))
