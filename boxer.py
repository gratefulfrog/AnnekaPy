#!/usr/bin/python3
# try to find word boxes
# brute-force/massive-ignorance method

from functools import reduce
import itertools,time

def boxWords(n, file='words.txt'):
    res0 = set()
    with open(file,'r') as f:
        for w in f:
            word=w.strip()
            if len(word) == n:
                res0.add(word)
    res1=set()
    for word in res0:
        for l in word:
            if l in map(lambda x: x[0], res0):
                res1.add(word)
    return res1

def transpose(wlis):
    res = []
    for i in range(len(wlis)):
        res.append(reduce(lambda l,r: l+r,
                          map(lambda w: w[i],wlis)))
    return res

iterPrint = 100000

def iboxN(n):
    words=boxWords(n)
    if not words:
        print('failed: no words')
        return False
    count = 0
    source=[]
    for i in range(n):
        source.append(words)
    for candidate in itertools.product(*source):
        if all(w in words for w in transpose(candidate)):
            print(candidate,tuple(transpose(candidate)))
            return True
        else:
            count+=1
            if not count%iterPrint:
                print(n,'{:,}'.format(count))
    print('failed')
    return False


if __name__ == '__main__':
    import sys
    if len(sys.argv)==2:
        c = int(sys.argv[1])
        for i in range(c,0,-1):
            print('Searching for the combination of :', i, 'letters...')
            time.sleep(2)
            if iboxN(i):
                break
    else:
        print('length arguments missing...')

    
    
    

            
