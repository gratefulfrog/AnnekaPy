#!/usr/local/bin/python3
# try to find word boxes
# set intersection on letters method
# note that the range of word lengths is [2,21]
# but [2,18] is the range for which cVec and constraintArray have no empty elts

#mutlithreaded version seems slower than single trheading???

from functools import reduce
from decimal import Decimal
import itertools,time
import threading

nbThreads = 4

def validateSolution(wIndexLis):
    #print('validate solution : wIndexLis :', wIndexLis)
    #return None
    try:
        for i in range(N):
            wiDict[reduce(lambda l,r:l+r,[wVec[j][i] for j in wIndexLis])]
        return [wVec[i] for i in wIndexLis]
    except KeyError:
        return None
    
def transpose(wlis):
    res = []
    for i in range(len(wlis)):
        res.append(reduce(lambda l,r: l+r,
                          map(lambda w: w[i],wlis)))
    return res

class seeker(threading.Thread):
    def __init__(self,name,foundEvt, solIt,size):
        threading.Thread.__init__(self,daemon=True)
        self.name = name
        self.foundEvt = foundEvt
        self.solutionIterator = solIt
        self.size=size
        #print(self.name,'starting')

    def run(self):
        global found
        count = 0
        try:
            for tuple in self.solutionIterator:
                res = validateSolution(tuple)
                if res:
                    print(self.name,': Solution :',[(wiDict[w],w) for w in res])
                    trans = transpose(res)
                    print(self.name, ': Transpose :',[(wiDict[w],w) for w in trans])
                    self.foundEvt.set()
                    return
                count +=1
                if count%modLoop == 0:
                    print(self.name,
                          ': {:.2e}'.format(count),'explored', '{:.2e}'.format(self.size-count),
                          'remaining', '  Percent solution space explored :',
                          ': {:.2e}'.format(100*count/self.size),
                          '%' )
        except Exception as e:
            print(e)
            self.foundEvt.set()
            # self.foundEvt.set()
            return
        print(self.name,': failed...')


# N                  : the size of the box
# wVec               : the vector of words of length N, the vector index has no significance
# wiDict             : dictionary such that
#                    : keys are words
#                    : value is the word's index in wVec
# cVec               : the vector sets of characters that appear a position as per index,
#                    : * i.e. cVec[3] is the set of characters that appear at postion 3
# cpDict             : is a dictionary such that
#                    : * Keys are tuples (char,pos)
#                    : * values are sets of word indices.
#                    : * i.e. cpDict[('d',2)] is the set of indices of words with a 'd' at positon 2
# constrainCharArray : an NxN array of sets of characters that could appear at the array position (i,j)
N      = 0
wVec   = []
wiDict = {}
cVec   = []
cpDict = {}
constrainCharArray = None

def boxWords(n, file='words.txt'):
    """
    create wVec:   vector of words of the correct length n index->word
    create cpDict: dictionary of (char,pos)->set(index) in wVec
    create cVec:   vector of set of characters possible at index: 
                   index -> set of characters that are possible in index position
    """
    global cVec
    global N
    N = n
    cVec = [set() for i in range(n)]
    
    with open(file,'r') as f:
        for w in f:
            word=w.strip()
            if len(word) == n:
                updateDataStructs(word)
    for ind in pSet:
        print(wVec[ind])
    #parPalin()
    #getConstraintArrays()

def parPalin():
    for (i,j) in itertools.product(pSet,pSet):
        if wVec[i][0] == wVec[j][1] and wVec[j][0] == wVec[i][1]:
            print(wVec[i],wVec[j])
                
    
pSet = set()
    
def updateDataStructs(word):
    """
    update wVec:   vector of words of the correct length n index->word
    update cpDict: dictionary of (char,pos)->set(index) in wVec
    update cVec:   vector of set of characters: index -> set of characters that are in index position, 
                   and that fit constraints
    """
    global wVec
    global wiDict
    global cVec
    global pSet
    index = len(wVec)
    wVec.append(word)
    wiDict[word]=index
    for i in range(len(word)):
        addCP((word[i],i),index)
        cVec[i].add(word[i])
    if isPalindrone(word):
        pSet.add(index)

def isPalindrone(word):
    if len(word)==0:
        return True
    elif word[0] != word[-1]:
        return False
    else:
        return isPalindrone(word[1:-1])

def getConstraintArrays():
    """
    take the vector of all characters at given index position
    then run through the word box and take intersections such that
    the possibilites box looks like this
    
    cVec[0]                           cVec[1].intersection(cVec[0])    cVec[2].intersection(cVec[0])    ... cVec[N-1].intersection(cVec[0])      
    cVec[0].instersection(cVec[1])    cVec[1]                          cVec[2].intersection(cVec[1])    ... cVec[N-1].intersection(cVec[1])      
    cVec[0].instersection(cVec[2])    cVec[1].intersection(cVec[2])    cVec[2]                          ... cVec[N-1].intersection(cVec[2])
    ...
    cVec[0].instersection(cVec[N-1])  cVec[1].intersection(cVec[N-1])  cVec[2].intersection(cVec[N-1])  ... cVec[N-1]

    """
    global constrainCharArray
    global constrainWordIndexArray
    constrainCharArray      = [[None for i in range(N)] for j in range(N)]
    constrainWordIndexArray = [[None for i in range(N)] for j in range(N)]
    for(i,j) in itertools.product(range(N), range(N)): # rows x cols
        if i != j:
            constrainCharArray[i][j] = cVec[i].intersection(cVec[j])
        else:
            constrainCharArray[i][j] = cVec[i]
    # solution
    solution = [unionize2GetIndices(constrainCharArray[i][0],i) for i in range(N)]
    for(i,j) in itertools.product(range(N), range(N)): # rows x cols
        solution[i] = solution[i].intersection(unionize2GetIndices(constrainCharArray[i][j],j)).intersection(unionize2GetIndices(constrainCharArray[i][j],i))
        if not solution:
            print('failed')
            return
    print('finding a solution')
    showSolution(solution)

modLoop = 1_000_000
    
def showSolution(solutionArray):
    size = reduce(lambda x,y:x*y,map(len,solutionArray))
    print('Solution Space Size : ', '{:.2e}'.format(size),'reduced to :', ': {:.2e}'.format(100*size/(pow(len(wVec),N))),'% of brute force space')
    for i in [set(x) for x in spread(list(solutionArray[-1]),nbThreads)]:
        #print(i)
        createSeeker(itertools.product(*solutionArray[:-1],i),reduce(lambda x,y:x*y,map(len,solutionArray[:-1]+[i])))
    foundEvent.wait()
    """
    for t in threads:
        t.join()
        print(t.name,'ended.')
    """
    
def spread (lis,n):
    l = len(lis)
    r = l%n
    d = l//n
    res=[]
    s = 0
    for i in range(n):
        offset = 1 if r else 0
        end = s + d + offset
        res.append(lis[s:end])
        s =end
        r-=1
    return res

def unionize2GetIndices(setOfChars,pos):
    u = set()
    for c in setOfChars:
        u = u.union(cpDict[(c,pos)])
    return u
            
def addCP(tup, ind):
    """
    tup may be any tuple, even ((c,p),(cc,pp)) etc.
    """
    global cpDict
    cpSet =  getCP(tup)
    cpSet.add(ind)        

def getCP(tup):
    res = None
    try:
        res = cpDict[tup]
    except KeyError:
        res = cpDict[tup] =  set()
    return res

foundEvent = threading.Event()
lk = threading.Lock()
#threads = []
threadCounter=0

def createSeeker(solutionIerator,sz):
    global threadCounter
    t = seeker('s-'+str(threadCounter),foundEvent,solutionIerator,sz)
    #threads.append(t)
    t.start()
    threadCounter+=1

def run(n):
    boxWords(n)    
    
if __name__ == '__main__':
    import sys
    if len(sys.argv)==1 :
        print('length arguments missing...')
        print('$ ./ppiBoxer.py depth [nbThreads]')
        sys.exit()
    if len(sys.argv)==3:
        nbThreads = int(sys.argv[2])
    n = int(sys.argv[1])
    start = time.time()
    print('Setting up the data Structures for a size :', n, 'search...')
    boxWords(n)
    print('Elapsed time :','{:,}'.format(round(time.time()-start,2)), 'seconds')

    
    
    

            
