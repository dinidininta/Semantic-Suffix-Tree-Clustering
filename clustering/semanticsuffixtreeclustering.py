import json
import requests
import time
from anytree import PreOrderIter, RenderTree
from clustering.cluster import Cluster
from clustering.suffixnode import SuffixNode
from preprocessing.casefolder import Casefolder
from preprocessing.stopwordremover import StopWordRemover
from preprocessing.postagger.postagger import Postagger


class SemanticSuffixTreeClustering:
    def __init__(self, documents):
        print "building tree...."
        self.root = self.build_tree(documents)
        print "done building tree...."

        print "pruning tree...."
        self.pruned_tree = self.tree_pruning(self.root)
        print "done pruning tree...."

        print "compactifying tree...."
        self.compactified_tree = self.compactify_tree(self.pruned_tree)
        print "done compactifying tree...."

        print "identifying cluster...."
        self.clusters = self.identify_cluster(self.compactified_tree)
        print "done identifying cluster...."

    def get_syn_set(self, word):
        synonym = []

        r = requests.get("http://kateglo.com/api.php?format=json&phrase=" + word)
        r.encoding = 'utf-8'
        try:
            body = json.loads(r.content)
            i = 0
            while i < len(body['kateglo']['relation']['s']):
                try:
                    synonym.append(body['kateglo']['relation']['s']['%s' % str(i)]['related_phrase'])
                    # print body['kateglo']['relation']['s']['%s' % str(i)]['related_phrase']
                    i = i + 1
                except KeyError:
                    break
        except ValueError:
            synonym = []
            # print synonym
            time.sleep(2)

        return synonym

    def count_sem_sim(self, wa, wb):
        # print("Semsim of " + str(wa) + " and " + str(wb))
        # print (getSynSet(wa))
        # print (getSynSet(wb))
        # print wa
        a = self.get_syn_set(wa)
        # print wb
        b = self.get_syn_set(wb)
        count = len(list(set(a) & set(b)))
        # print(count)
        if count >= 1:
            return True
        else:
            return False

    def is_related(self, parent1, parent2):
        relation = []
        for node1 in PreOrderIter(parent1):
            for node2 in PreOrderIter(parent2):
                try:
                    if node1.name == node2.name or self.count_sem_sim(node1.name, node2.name):
                        relation.append(True)
                except requests.ConnectionError:
                    print "trying again.... @is_related"
                    time.sleep(2)
                    continue
                except AttributeError:
                    print node1.name + " is not in database"
                    break

        if len(relation) == len([node1.name for node1 in PreOrderIter(parent1)]) \
                and len(relation) == len([node2.name for node2 in PreOrderIter(parent2)]):
            return True
        else:
            return False

    def build_tree(self, documents):
        print "jumlah dokumen: " + str(len(documents))
        assert len(documents) > 0
        # Buat node root
        root = SuffixNode("root", 0)
        idx = 1
        # doc = 0

        # Konstruksi semantic suffix tree dengan memasukkan dokumen satu per satu
        for id_, document in enumerate(documents):
            title = StopWordRemover().stopwordRemoval(document)
            # print title
            words = Postagger().extract_svo(Casefolder().casefold(title)).split()

            # Kata pertama menjadi child dari root
            current = SuffixNode(words[0], idx, parent=root)
            if len(words) == 1:
                current.insert_doc(id_)
            idx = idx + 1

            pn = [root]
            i = 1

            # Kata kedua dan seterusnya
            while i <= len(words[1:]):
                node = SuffixNode(words[i], idx, parent=current)
                # node.insert_doc(doc)
                idx = idx + 1
                temp = node
                # Kata seterusnya juga dijadikan child dari root
                # List dibalik supaya node per string dibuat secara berurutan seperti anak tangga, agar suffix link juga
                # berurutan
                # List juga difilter supaya node baru tidak ditambah ke node lama yg sudah punya children
                for n in filter(lambda x: x.is_leaf or x == root, pn[::-1]):
                    if words[i] not in n.children:
                        txt = SuffixNode(words[i], idx, parent=n)
                        temp.add_suffix_link(txt)
                        temp = txt
                        # txt.insert_doc(doc)
                        # cek node yg sudah ada kalo misalnya ada nama yang sama, node baru diselipkan sebelumnya
                        # supaya suffix link tidak terbalik
                        pit = [p.name for p in pn]
                        if txt.name in pit:
                            pn.insert(pit.index(txt.name) - 1, txt)
                        else:
                            pn.append(txt)
                        # kalau ini kata yg terakhir baru masukkan dokumen
                        if i == len(words) - 1:
                            txt.insert_doc(id_)
                        idx = idx + 1
                # pn.append(txt)
                current = node
                if i == len(words) - 1:
                    node.insert_doc(id_)
                i = i + 1
            # doc = doc + 1

        # print "\n-----------FIRST TREE------------\n"
        #
        # for pre, fill, node in RenderTree(root):
        #     print("%s%s [%s] suffix = %s, doc = %s" % (pre, node.name, node.index, node.get_index_suffix_link(),
        #                                                node.doc))

        # Proses merge subtree yang parentnya sama secara string dan semantik
        for child in root.children[::-1]:
            # print child.name
            for child2 in root.children:
                if child != child2:
                    try:
                        if child.name == child2.name or self.count_sem_sim(child.name, child2.name):
                            # print("%s pindah ke %s" % (child.name, child2.name))
                            for c in child.children:
                                c.parent = child2
                            for doc in child.doc:
                                child2.insert_doc(doc)
                            child.parent = None
                            break
                    except requests.ConnectionError:
                        print "trying again..... @merge tree"
                        time.sleep(2)
                        continue
                    except AttributeError:
                        print child.name + " is not in database"
                        break

        # Update suffix link
        all_node_index = [simpul.index for simpul in PreOrderIter(root, filter_=lambda n1: n1.name != 'root')]
        for node1 in PreOrderIter(root, filter_=lambda n1: n1.name != 'root'):
            if node1.get_suffix_link() is not None and node1.get_suffix_link().index not in all_node_index:
                for node2 in root.children:
                    if node1 != node2:
                        try:
                            if node1.name == node2.name or self.count_sem_sim(node1.name, node2.name):
                                node1.add_suffix_link(node2)
                        except requests.ConnectionError:
                            print "trying again.... @update suffix link"
                            time.sleep(2)
                            continue
                        except AttributeError:
                            print node1.name + " is not in database"
                            break

        return root

    def tree_pruning(self, tree):
        gn = tree
        # print "\n\nMulai dari " + tree.name
        i = 0

        for pn in PreOrderIter(gn):
            # gn = tree
            if pn.name != "root":
                gn = pn.parent
                # print "gn saat ini " + gn.name + "[" + str(gn.index) + "]"
                # pn = gn.children[i]
                # print "pn saat ini " + pn.name + "[" + str(pn.index) + "]"
                # print "anak gn saat ini: " + str(len(gn.children))
                j = 0
                while j < len(pn.children):
                    cn = pn.children[j]
                    # print "cn saat ini " + cn.name + "[" + str(cn.index) + "]"
                    if cn.has_suffix_link():
                        sn = cn.get_suffix_link()
                        # print "suffix dari " + cn.name + "[" + str(cn.index) + "] adalah " + sn.name + "[" + str(
                        #     sn.index) + "]"
                        if gn != sn:
                            # print "gn != sn "
                            if self.is_related(sn, pn):
                                # print "pn related to sn"
                                cn.parent = None
                                sn.parent = pn
                            else:
                                # print "pn/ccn not related to sn"
                                for doc in sn.doc:
                                    cn.insert_doc(doc)
                                sn.doc = []
                                cn.suffix_link = None
                                for csn in sn.children:
                                    if csn.get_suffix_link() == pn or csn.get_suffix_link() == cn:
                                        csn.parent = cn
                        elif gn == sn:
                            # print "gn == sn"
                            for doc in cn.doc:
                                pn.insert_doc(doc)
                            for ccn in cn.children:
                                for doc2 in ccn.doc:
                                    pn.insert_doc(doc2)
                            cn.parent = None
                    j = j + 1
                #     print "j = " + str(j)
                # for pre, fill, node in RenderTree(tree):
                #     print("%s%s (%s) suffix = %s, doc = %s" % (pre, node.name, node.index, node.get_index_suffix_link(),
                #                                                node.doc))
                # gn = pn
                # tree_pruning(gn)
                i = i + 1
                # print "i = " + str(i)

        # print "\n\n"
        return tree

    def compactify_tree(self, tree):
        gn = tree
        for pn in gn.children:
            names = ""
            docs = []
            # print pn.name
            if len(pn.children) == 1 and pn.get_suffix_link() is None and not pn.doc:
                cn = pn.children[0]
                for ccn in PreOrderIter(cn):
                    names = names + ccn.name + " "
                    if ccn.doc:
                        docs.extend(ccn.doc)
                combined = SuffixNode(pn.name + " " + names, pn.index, parent=tree)
                for doc in docs:
                    combined.insert_doc(doc)
                pn.parent = None
                # elif pn.is_leaf:
                #     pn.parent = None

        # print "sini kali ya"
        # print [node.name for node in PreOrderIter(tree)]
        return tree

    def compute_clus_sim(self, clusters):
        # print "\nperhitungan clussim:"
        # for cluster in clusters:
        #     print("[%s: %s]" % (cluster.label, cluster.documents))
        # print "-----"
        ca = clusters[len(clusters) - 1]
        i = len(clusters) - 2
        while i >= 0:
            try:
                cb = clusters[i]
                # print ca.label + " vs " + cb.label
                if len(list(set(ca.documents) & set(cb.documents))) == len(cb.documents):
                    # print "cb"
                    # print (cb.label + " dihapus")
                    clusters.remove(cb)
                elif len(list(set(ca.documents) & set(cb.documents))) == len(ca.documents):
                    # print "ca"
                    # print (ca.label + " dihapus")
                    clusters.remove(ca)
                    ca = clusters[i]
            except IndexError:
                break
            i = i - 1
        # print "-----"

    def identify_cluster(self, tree):
        gn = tree
        can_cluster = []
        final_cluster = []
        # print [node.name for node in PreOrderIter(gn)]
        for pn in gn.children:
            # print "hehe " + pn.name
            first_cluster = Cluster(pn.name, pn.doc)
            can_cluster.append(first_cluster)
            # print "lol " + pn.name
            for cn in pn.children:
                next_cluster = Cluster(cn.parent.name + " " + cn.name, cn.doc)
                temp = next_cluster
                can_cluster.append(next_cluster)
                for ccn in PreOrderIter(cn, filter_=lambda n: n.name != cn.name):
                    new_cluster = Cluster(next_cluster.label + " " + ccn.name, ccn.doc)
                    can_cluster.append(new_cluster)
                    if ccn.is_leaf:
                        next_cluster = temp
                    else:
                        next_cluster = new_cluster

            # compute clus sim
            self.compute_clus_sim(can_cluster)
            final_cluster += can_cluster
            can_cluster = []

        # filter useless cluster
        for cluster in reversed(final_cluster):
            if not cluster.documents:
                final_cluster.remove(cluster)
            else:
                for cluster2 in filter(lambda x: x != cluster, final_cluster):
                    if len(list(set(cluster.documents) & set(cluster2.documents))) >= 1:
                        if len(cluster.documents) <= len(cluster2.documents):
                            final_cluster.remove(cluster)
                            break

        # for i in range(0, len(final_cluster)):
        #     print("[%s: %s]" % (final_cluster[i].label,  "; ".join([cd.title for cd in final_cluster[i].documents])))

        del can_cluster
        return final_cluster

    def get_clusters(self):
        return self.clusters

    def print_semantic_suffix_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("%s%s [%s] suffix = %s, doc = %s" % (pre, node.name, node.index, node.get_index_suffix_link(),
                                                       node.doc))
