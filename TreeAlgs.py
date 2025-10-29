# TreeAlgs.py
# Implementation of the UPGMA (Unweighted Pair Group Method with Arithmetic Mean) algorithm for CREATING PHYLOGNETIC TREES
# This code is a simple demonstration and is sunject to optimization, readablility and error handling improvements.
# Might become a method in a future class, idk.
from TreeObject import PhyloTree
def UPMGA(taxa,taxa_labels):
    tree = PhyloTree(taxa_labels)
    while len(taxa) > 1:
        min_dist = taxa[0][1]
        closest_pair = [0,1]
        for j,taxon in enumerate(taxa):
            for i,dists in enumerate(taxon):
                if dists < min_dist and i!=j:
                    min_dist = dists
                    closest_pair = [j, i]

        cluster_label = taxa_labels[closest_pair[0]]+taxa_labels[closest_pair[1]]
        left_label = taxa_labels[closest_pair[0]]
        right_label = taxa_labels[closest_pair[1]]
        dist = min_dist / 2.0
        right_dist=dist-tree.nodes[right_label].height
        left_dist=dist-tree.nodes[left_label].height
        # Add cluster to PhyloTree (branch lengths computed from node heights)
        tree.add_cluster(cluster_label, left_label, right_label, left_dist,right_dist)

        new_dist = [(taxa[closest_pair[0]][i]+taxa[closest_pair[1]][i])/2 for i in range(len(taxa)) if i not in closest_pair]
        new_dist.insert(0,0)
        new_t=[new_dist]
        k=1
        for i,taxon in enumerate(taxa):
            if i not in closest_pair:
                dist=[new_dist[k]]
                k+=1
                dist.extend([taxon[j] for j in range(len(taxon)) if j not in closest_pair])
                new_t.append(dist)
        taxa=new_t
        taxa_labels=tree.working_labels
    return tree
def OTU_S_calculator(taxa):
    n=len(taxa)
    return [sum(t)/(n-2) for t in taxa]
# OTU_M matrix calculator
# M[i][j] = D[i][j] - S[i] - S[j]
# where D is the original distance matrix and S is the OTU_S vector
# Returns a lower triangular matrix
# Unoptimized version - runs repeat calculations upon each call , consider caching S if performance is an issue or ommitting caltulation for known M
def OTU_M_calculator(taxa, S):
    m=[]
    for i in range(len(taxa)-1):
        row_i=[]
        for j in range(i+1, len(taxa)):
            row_i.append(taxa[i][j]-S[i]-S[j])
        m.append(row_i)
    return m
# Neighbor-Joining algorithm placeholder
def NJ(taxa,taxa_labels):
    tree=PhyloTree(taxa_labels)
    while len(taxa_labels)>2:
        S=OTU_S_calculator(taxa)
        M=OTU_M_calculator(taxa,S)
        min_m=float('inf')
        to_join=[-1,-1]
        for idxi,i in enumerate(M):
            for idxj,j in enumerate(i):
                if j<min_m:
                    min_m=j
                    to_join=[idxi,idxi+idxj+1]
        cluster_label = taxa_labels[to_join[0]]+taxa_labels[to_join[1]]
        left_label = taxa_labels[to_join[0]]
        right_label = taxa_labels[to_join[1]]
        distij=taxa[to_join[0]][to_join[1]]
        left_dist= (distij - S[to_join[0]] + S[to_join[1]])/2
        right_dist = (distij - S[to_join[1]] + S[to_join[0]])/2
        tree.add_cluster(cluster_label,left_label,right_label,left_dist,right_dist)

        new_dist = [(taxa[to_join[0]][i]+taxa[to_join[1]][i]-distij)/2 for i in range(len(taxa)) if i not in to_join]
        new_dist.insert(0,0)
        new_t=[new_dist]
        k=1
        for i,taxon in enumerate(taxa):
            if i not in to_join:
                dist=[new_dist[k]]
                k+=1
                dist.extend([taxon[j] for j in range(len(taxon)) if j not in to_join])
                new_t.append(dist)
        taxa=new_t
        taxa_labels=tree.working_labels
    ## Pair remaining two
    cluster_label=taxa_labels[0]+taxa_labels[1]
    tree.add_cluster(cluster_label,taxa_labels[0],taxa_labels[1],taxa[0][1],taxa[0][1])
    return tree