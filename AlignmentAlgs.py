settings={"match": 1,"missmatch":-1,"indel":-2,"out":"output.txt"}
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
def Needleman_wunsch(seq1,seq2):
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
    

class Fogssa_node:
    def __init__(self,p1,p2,s1,s2,score,parent):
        #So data wise, i don't like this code (shockking) but better done than untouched
        self.p1=p1
        self.p2=p2
        self.s1=s1
        self.s2=s2
        self.score=score
        self.parent=parent
        #Functionality: checking if children are there will check if node is expanded
        self.children=[]
        diff=abs(s1-p1-(s2-p2))
        minlen=min(s1-p1,s2-p2)
        Fmax=minlen*settings["match"]+diff*settings["indel"]
        Fmin=minlen*settings["missmatch"]+diff*settings["indel"]
        self.Tmax=Fmax+score
        self.Tmin=Fmin+score
    def expand(self,seq1,seq2):
        match_score=settings["match"] if seq1[self.p1]==seq2[self.p2] else settings["missmatch"]
        children=[]
        #sanity chcecks i guess
        if(self.p1+1<=self.s1):
            children.append(Fogssa_node(self.p1+1,self.p2,self.s1,self.s2,self.score+settings["indel"],self))
        if(self.p2+1<=self.s2):
            children.append(Fogssa_node(self.p1,self.p2+1,self.s1,self.s2,self.score+settings["indel"],self))
        if(self.p1+1<=self.s1 and self.p1+1<=self.s1):
            children.append(Fogssa_node(self.p1+1,self.p2+1,self.s1,self.s2,self.score+match_score,self))
        children.sort(key= lambda x: x.Tmax+x.Tmin,reverse=True)
        self.children=children
        return children
#Fogsaa
def FOGSSA(seq1,seq2):
    priority_queue=[]
    #fitness referance: dict used to check if a node at (p1, p2) is promising
    fitness_referance={}
    p1,p2=0,0
    s1,s2=len(seq1),len(seq2)
    root=Fogssa_node(0,0,s1,s2,0,None)
    alignment_path=None
    small=min(s1,s2)
    #sanity_check=small//0.3*settings["match"]+(small-(small//0.3))*settings["missmatch"]+ abs(s1-s2)*settings["indel"]
    opt=root.Tmin
    currnode=root
    while True:
        while p1 <= s1-1 or p2 <= s2-1:
            ch=currnode.expand(seq1,seq2)
            currnode=ch[0]
            p1=currnode.p1
            p2=currnode.p2
            print(currnode.score,currnode.p1, currnode.p2,currnode.Tmax, currnode.Tmin)
            if(len(ch)>1):
                priority_queue.extend(ch)
            fit=fitness_referance.get((p1,p2))
            if (fit is not None and currnode.score<=fit) or currnode.Tmax<=opt:
                priority_queue.sort(key=lambda x:x.Tmax+x.Tmin)
                currnode=priority_queue.pop()
                p1=currnode.p1
                p2=currnode.p2
            else:
                fitness_referance[(p1,p2)]=currnode.score
        if currnode.Tmax>=opt:
            opt=currnode.Tmax
            alignment_path=currnode
        priority_queue.sort(key=lambda x:x.Tmax+x.Tmin)
        currnode=priority_queue.pop()
        p1=currnode.p1
        p2=currnode.p2
        if opt>=currnode.Tmax:# or currnode.Tmax<sanity_check:
            return opt
print(Needleman_wunsch("ACGGTTGC","AGCGTC")[-1][-1])
print(FOGSSA("ACGGTTGC","AGCGTC"))