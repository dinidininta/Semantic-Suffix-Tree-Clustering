# Semantic Suffix Tree Clustering
A Python implementation of Semantic Suffix Tree Clustering algorithm, based on the Janruang and Guha's paper "Semantic Suffix Tree Clustering" https://www.cs.ait.ac.th/~guha/papers/semSufTreeClus.pdf

The  distinctive  methodology  of the  Semantic  Suffix  Tree  Clustering  (SSTC)  algorithm  is  that  it  simultaneously  constructs  the semantic  suffix  tree  through  an  on-depth  and  on-breadth  pass by using semantic similarity and string matching. SSTC uses only subject-verb-object classification to generate clusters and readable labels.

SSTC  can  cluster  documents  that  share  a semantic similarity. Specific cluster are returned in a readable form. Additionally, the SSTC can improve the performance of approaches that use the original STC algorithm because it can cluster semantically similar documents, reduce the number of nodes and reach higher precision.

SSTC has 3 main phases:  
1. Preprocessing  and  constructing  semantic  suffixtree
2. Tree pruning, the process to reduce the number of nodes on-depth and  sub-trees  on-breadth  while  still  retaining  the  concept  or meaning of each node and sub-tree.
3. Identifying clusters

This implementation is available to Indonesian language only.

# Prerequisites
Need installation of this library first.
* [anytree](https://github.com/c0fec0de/anytree) - The Python tree data library

# Usage

    from clustering.semanticsuffixtreeclustering import SemanticSuffixTreeClustering
    
    documents = ["alat pernapasan", "alat peredaran darah", "alat pencernaan"]
    sstc = SemanticSuffixTreeClustering(documents)
    
    sstc.print_semantic_suffix_tree()
    
    print "\nCluster:"
    for c in sstc.get_clusters():
        print "%s : %s" % (c.label, "; ".join([str(cd) for cd in c.documents]))
        
# Postagger Modul
The postagger modul used in this project is from
* [pebahasa](https://github.com/pebbie/pebahasa)
