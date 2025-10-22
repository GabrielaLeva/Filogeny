# UPMGA.py
# Implementation of the UPGMA (Unweighted Pair Group Method with Arithmetic Mean) algorithm for CREATING PHYLOGNETIC TREES
# This code is a simple demonstration and is sunject to optimization, readablility and error handling improvements.
# Might become a method in a future class, idk.

def get_distance(tree, dist, label):
    if label not in tree:
        return dist
    else:
        return dist-tree[label]["to_end"]
def get_new_labels(taxa_labels, closest_pair):
    new_labels = [taxa_labels[closest_pair[0]]+taxa_labels[closest_pair[1]]]
    new_labels.extend([taxa_labels[i] for i in range(len(taxa_labels)) if i not in closest_pair])
    return new_labels
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
        new_labels=get_new_labels(taxa_labels, closest_pair)
        tree[new_labels[0]] = {taxa_labels[closest_pair[0]]:get_distance(tree,min_dist/2,taxa_labels[closest_pair[0]]), taxa_labels[closest_pair[1]]:get_distance(tree,min_dist/2,taxa_labels[closest_pair[1]]), "to_end":min_dist/2}
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
        taxa_labels=new_labels
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
    tree={}
    og_labels=taxa_labels.copy()
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
        new_labels=get_new_labels(taxa_labels,to_join)
        distij=taxa[to_join[0]][to_join[1]]
        tree[new_labels[0]]={taxa_labels[to_join[0]]:(distij-S[to_join[0]]+S[to_join[1]])/2,taxa_labels[to_join[1]]:(distij-S[to_join[1]]+S[to_join[0]])/2}
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
        taxa_labels=new_labels # Placeholder
    ## Pair remaining two
    last_labels=taxa_labels[0]+taxa_labels[1]
    tree[last_labels]={taxa_labels[0]:taxa[0][1],taxa_labels[1]:taxa[0][1]}
    return tree