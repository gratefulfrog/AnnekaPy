#!/usr/bin/python3

from functools import reduce

def excludes (letter, file):
    """
    return an object of the form: 
    [<set of letter>, <set of words containing that letter>]
    where the set is all the words in the word file that contain the letter.
    We call this object an 'excludeSet' in the rest of the file.
    """
    res = set()
    for word in file:
        if letter in word:
            res.add(word)
    return [set(letter),res]

def exludesAdd(excludeSetLis):
    """
    argument is a list of excludeSets, i.e.
    [[<set of letters>,<set of excluded words>],
     [<set of letters>,<set of excluded words>],
     ...]
    this function returns a new exclude set by combining all the letters and performing a
    union over all the sets.

    """
    return reduce(lambda l,r: [l[0].union(r[0]),l[1].union(r[1])],
                  excludeSetLis)

def lis0(fileName):
    """
    returns a list of excludeSets sorted by the lenght of the set of words excluded
    least excluded first.
    This is used to start the search process.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    res = []
    for letter in alphabet:
        with open (fileName, 'r') as f:
            res.append(excludes(letter,f))
    return increasing(res)

def increasing(lis):
    """
    sorts the lis in place by shortest set of excluded words
    """
    lis.sort(key= lambda x:len(x[1]))
    return lis

def purge(lis):
    """
    remove exlcudeSets with duplicate sets of letters from the list
    """
    res = [lis[0]]
    for elt in lis[1:]:
        if not elt in res:
            res.append(elt)
    return res

def lis1n(sortedNLetterSetList, sorted1LetterSetlist, n=10):
    """
    this will combine the first n exclude sets of the 1st with all the exclude sets of the
    2nd argument and return the resulting exlcuded set list sorted and purged of duplicates
    """
    res = []
    for i in range(n): # just take top n
        letterSet = sortedNLetterSetList[i]
        for otherLetterSet in sorted1LetterSetlist:
            if otherLetterSet[0].intersection(letterSet[0]) != otherLetterSet[0]:
                res.append(exludesAdd([letterSet,otherLetterSet]))
    return increasing(purge(res))

def run(c,n,fileName= 'words.txt'):
    """
    search for the combination of c letters that exclude the least words,
    limiting the search to the top n candidates at each iteration
    returns 4 things:
    best combination
    nb words excluded by best combiation
    2nd best combination
    nb words excluded by 2nd best combiation
    """
    l0 = lis0(fileName)
    res = l0
    for i in range(c-1):
        res = lis1n(res,l0,n)
    return res[0][0],      \
           len(res[0][1]), \
           res[1][0],      \
           len(res[1][1]),

if __name__ == '__main__':
    import sys
    c = 5
    d = 3
    if len(sys.argv)==2:
        c = int(sys.argv[1])
    elif len(sys.argv)==3:
        [c,d] = [int(x) for x in sys.argv[1:]]
    print('Searching for the combination of :',c,'letters at depth :',d)
    try:
        res = run(c,d)
        c0 = list(res[0])
        c0.sort()
        c1 = list(res[2])
        c1.sort()
        print('The combination :',"'%s'"%(''.join(x for x in c0)),'excludes only  :',res[1],'words')
        print('Next comes      :',"'%s'"%(''.join(x for x in c1)),'which excludes :',res[3],'words')
    except:
        print('Ooops! Looks like we had a problem. Maybe memory ran out? Try searching at less depth!')
    
    
    

            
