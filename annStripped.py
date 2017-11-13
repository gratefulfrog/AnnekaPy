#!/usr/bin/python3

import urllib.request

url = 'http://greenteapress.com/thinkpython2/code/words.txt'

def pprint(word):
    print('length :', len(word),[c for c  in word])

def annVers():
    response = urllib.request.urlretrieve(url, 'words.txt')
    with open('words.txt','r') as words:
        for line in words:
            word = line.strip()
            if len(word)> 20:
                pprint(line)
                pprint (word)

def annVersListCorrected():
    response = urllib.request.urlretrieve(url, 'words.txt')
    with open('words.txt','r') as words:
        print([word.strip() for word in words if len(word.strip())>20])

        
def vers1():
    response = urllib.request.urlretrieve(url, 'words.txt')
    with open('words.txt','r') as words:
        for line in words:
            if len(line)> 20:
                pprint (line.strip())

def vers2():
    response = urllib.request.urlretrieve(url, 'words.txt')
    with open('words.txt','r') as words:
        print([word.strip() for word in words if len(word)>20])

if __name__ == '__main__':
    print('Ann Style:')
    annVers()
    print('\nAnn List Style (but corrected):')
    annVersListCorrected()
    print('\nWhat Ann wanted?:')
    vers1()
    print('\nA list of what Ann wanted?:')
    vers2()
    print('\nBut who can say what Ann wanted?')
    
    
    

            
