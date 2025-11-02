from random import choice
import time
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
        if (s1-p1) <= (s2-p2):
            Fmax=(s1-p1)*settings["match"]+((s2-p2)-(s1-p1))*settings["indel"]
            Fmin=(s1-p1)*settings["missmatch"]+((s2-p2)-(s1-p1))*settings["indel"]
        else:
            Fmax=(s2-p2)*settings["match"]+((s1-p1)-(s2-p2))*settings["indel"]
            Fmin=(s2-p2)*settings["missmatch"]+((s1-p1)-(s2-p2))*settings["indel"]
        self.upper_bound=Fmax+score
        self.lower_bound=Fmin+score
    def expand(self,seq1,seq2):
        children=[]
        children.append(Fogssa_node(self.p1+1,self.p2,self.s1,self.s2,self.score+settings["indel"],self))
        children.append(Fogssa_node(self.p1,self.p2+1,self.s1,self.s2,self.score+settings["indel"],self))
        match_score=settings["match"] if seq1[self.p1]==seq2[self.p2] else settings["missmatch"]
        children.append(Fogssa_node(self.p1+1,self.p2+1,self.s1,self.s2,self.score+match_score,self))
        children.sort(key= lambda x: (x.upper_bound,x.lower_bound))
        self.children=children
        return children
#Insert at priority 
def Insert_node_at_sorted(node:Fogssa_node,list:list,begin,end):
    child=node.children[-1]
    while begin<end:
        halfway=(end+begin)//2
        h_node = list[halfway].children[-1]
        if h_node.upper_bound>child.upper_bound or (h_node.upper_bound==child.upper_bound and h_node.lower_bound>child.lower_bound):
            end=halfway
        elif h_node.upper_bound<child.upper_bound or (h_node.upper_bound==child.upper_bound and h_node.lower_bound<child.lower_bound):
            begin=halfway+1
        elif h_node.upper_bound==child.upper_bound and h_node.lower_bound==child.lower_bound:
            begin=halfway+1
            break
    list.insert(begin,node)
#Fogsaa
def FOGSSA(seq1,seq2):
    #priority_queue=[]
    priority_queue_new=[]
    #fitness referance: dict used to check if a node at (p1, p2) is promising
    fitness_referance={}
    p1,p2=0,0
    s1,s2=len(seq1),len(seq2)
    root=Fogssa_node(0,0,s1,s2,0,None)
    alignment_path=None
    small=min(s1,s2)
    th=small*30//100
    sanity_check=th*settings["match"]+(small-th)*settings["missmatch"]+abs(s1-s2)*settings["indel"]
    lb=root.lower_bound
    currnode=root
    while True:
        while p1 <= s1-1 and p2 <= s2-1:
            if not currnode.children:
                currnode.expand(seq1,seq2)
            ch=currnode.children.pop()
            if currnode.children:
                #priority_queue.append(currnode)
                Insert_node_at_sorted(currnode,priority_queue_new,0,len(priority_queue_new))
            currnode=ch
            p1=currnode.p1
            p2=currnode.p2
            #print(currnode.score,currnode.p1, currnode.p2,currnode.upper_bound, currnode.lower_bound)
            fit=fitness_referance.get((p1,p2))
            if (fit is not None and currnode.score<=fit) or currnode.upper_bound<=lb:
                break
            else:
                fitness_referance[(p1,p2)]=currnode.score
        else:
            if currnode.upper_bound>lb:
                lb=currnode.upper_bound
                alignment_path=currnode
        #priority_queue.sort(key=lambda x:(x.children[-1].upper_bound,x.children[-1].lower_bound))
        #currnode=priority_queue.pop()
        if priority_queue_new:
            currnode=priority_queue_new.pop()
        else:
            return lb
        p1=currnode.p1
        p2=currnode.p2
        #print("Moving to node at ", p1,",",p2)
        if lb>=currnode.upper_bound or currnode.upper_bound<sanity_check:
            return lb
print(Needleman_wunsch("ACGGTTGC","AGCGTC")[-1][-1])
print(FOGSSA("ACGGTTGC","AGCGTC"))

## Randomized tests
test_seq=[''.join([choice(["A","C","T","G"]) for _ in range(100)]) for _ in range(10)]
ex_time=time.time()
[print(Needleman_wunsch(test_seq[2*i],test_seq[2*i+1])[-1][-1]) for i in range(5)]
print(time.time()-ex_time)
ex_time=time.time()
[print(FOGSSA(test_seq[2*i],test_seq[2*i+1])) for i in range(5)]
print(time.time()-ex_time)