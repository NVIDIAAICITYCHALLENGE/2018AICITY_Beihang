import json
import os
import sys
import re

def deal(x, sc):
    x = re.split('[\s,]+', x)
    x = [i for i in x if len(i)>0]
    print len(x)
    res = []
    for i in xrange(0, len(x), 4):
        res.append([float(x[i+j]) for j in xrange(4)])
        res[-1][-1]*=sc
    return res


if __name__=='__main__':
    fd = open('LOC-modL2')
    u = {}
    tar = None
    for line in fd.readlines():
        line = line[:-1].upper()
        if len(line)<=0: continue
        if 'LOC' in line:
            print line
            if line[line.find('LOC')+3] in '1':
                sc = 4./3*1.1*1.06
            elif line[line.find('LOC')+3] in '2':
                sc = 4./3*1.1*1.06
            elif line[line.find('LOC')+3] in '3':
                sc = 1.16
            else:
                sc = 1.16
            item = []
            u[line[:6].lower().capitalize()] = item
            tar = item
        elif '#' in line:
            continue
        else:
            if tar is not None:
                tar += deal(line, sc)
    fd.close()
    for i in u:
        if 'Loc1' in i:
            it = u[i]
            u[i] = [j for j in u[i] if j[2]<7 and j[2] > -17]
        if 'Loc2' in i and False:
            it = u[i]
            u[i] = [j for j in u[i] if j[2]>1 and j[2] < 150]
    print u
    json.dump(u, open('LOCF2.txt', 'w'), indent=2)
    print 'done'
