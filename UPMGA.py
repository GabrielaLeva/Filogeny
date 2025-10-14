# UPMGA.py
# Implementation of the UPGMA (Unweighted Pair Group Method with Arithmetic Mean) algorithm for CREATING PHYLOGNETIC TREES
# This code is a simple demonstration and is sunject to optimization, readablility and error handling improvements.
# Might become a method in a future class, idk.

taxa=[[0, 4, 2, 3], [4, 0 ,6, 7], [2,6,0,5], [3,7,5,0]]
taxa_labels=["A", "B", "C", "D"]
def get_distance(tree, dist, label):
    if label not in tree:
        return dist
    else:
        return dist-tree[label]["to_end"]
def UPMGA(taxa,taxa_labels):
    # Tree structure to hold the final tree
    # Might become a proper object in the future
    # {"Cluster": {"A" : distance, "B":distance, "to_end":distance},}
    tree = {}
    while len(taxa) > 1:
        min_dist = taxa[0][1]
        closest_pair = [0,1]
        for j,taxon in enumerate(taxa):
            for i,dists in enumerate(taxon):
                if dists < min_dist and i!=j:
                    min_dist = dists
                    closest_pair = [j, i]
        new_labels = [taxa_labels[closest_pair[0]]+taxa_labels[closest_pair[1]]]
        new_labels.extend([taxa_labels[i] for i in range(len(taxa_labels)) if i not in closest_pair])
        tree[new_labels[0]] = {taxa_labels[closest_pair[0]]:get_distance(tree,min_dist/2,taxa_labels[closest_pair[0]]), taxa_labels[closest_pair[1]]:get_distance(tree,min_dist/2,taxa_labels[closest_pair[1]]), "to_end":min_dist/2}
        new_dist = [(taxa[closest_pair[0]][i]+taxa[closest_pair[1]][i])/2 for i in range(len(taxa)) if i not in closest_pair]
        new_dist.insert(0,0)
        new_t=[new_dist]
        for i,taxon in enumerate(taxa):
            k=1
            if i not in closest_pair:
                dist=[new_dist[k]]
                k+=1
                dist.extend([taxon[j] for j in range(len(taxon)) if j not in closest_pair])
                new_t.append(dist)
        taxa=new_t
        taxa_labels=new_labels
    print(tree)
UPMGA(taxa,taxa_labels)