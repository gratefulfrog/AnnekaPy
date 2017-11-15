#!/usr/local/bin/python3


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


"""
[0,1,2,3,4,5,6,7,8,9]
l = 10
n = 3
r = 1
d= 3
for i in range(n):
s=0, offset = 1 if r else 0, end = s+d+o = 0+3+1 = 4 = [0:4] ==> [0,1,2,3]
s= end = 4, r-=1, offset=1 if r else 0 , end = s+d+o = 4+3+0 = 7  => [4:7] = [4,5,6]
s= end = 7, r-=1, offset= 1 if r else 0, end = s+d+o  = 7+3+0 = 10 => [7:10] = [7,8,9]


"""
