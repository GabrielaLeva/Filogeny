settings={"match": 1,"missmatch":-1,"indel":-1,"out":"output.txt"}
def read_result(i,j,matrix,seq1,seq2,local=False):
    a = ["",""]
    while i>0 or j>0:
        if local and matrix[j][i]==0:
            break
        score=settings["match"] if seq1[i-1]==seq2[j-1] else settings["missmatch"]
        if matrix[j][i]==matrix[j-1][i-1]+score:
            a[0] = seq1[i-1] + a[0]
            a[1] = seq2[j-1] + a[1]
            i-=1
            j-=1
        elif i>0 and matrix[j][i] == matrix[j][i-1] + settings["indel"]:
            a[0] = seq1[i-1] + a[0]
            a[1] = "-" + a[1]
            i-=1
        else:
            a[0] = "-" + a[0]
            a[1] = seq2[j-1] + a[1]
            j-=1
    return a
def global_alignment(seq1,seq2):
    matrix = [list(range(0,(len(seq1)+1)*settings["indel"],settings["indel"]))]
    for i2,letter2 in enumerate(seq2):
        matrix.append([matrix[i2][0]+settings["indel"]])
        for i1,letter1 in enumerate(seq1):
            ind1=matrix[i2+1][i1]+settings["indel"]
            ind2=matrix[i2][i1+1]+settings["indel"]
            m= settings["match"] if letter1==letter2 else settings["missmatch"]
            m+=matrix[i2][i1]
            matrix[i2+1].append(max(ind1,ind2,m))
    return matrix
