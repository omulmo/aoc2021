#! /usr/bin/env python3
from audioop import mul
from collections import defaultdict
from sortedcontainers import SortedSet
import sys


class Cave:
    def __init__(self, inputs, repeat=1):
        self.w = len(inputs[0])
        self.h = len(inputs)
        self.data = dict( ((x,y),int(inputs[y][x])) for x in range(self.w) for y in range(self.h) )
        self.width = repeat*self.w
        self.height = repeat*self.h

    def nbors(self, pos):
        x,y = pos
        for a,b in (x-1,y), (x+1,y), (x,y-1), (x,y+1):
            if a<0 or a==self.width: continue
            if b<0 or b==self.height: continue
            added_risk = a//self.w + b//self.h
            yield (a,b), (self.data[a%self.w,b%self.h] + added_risk - 1) % 9 + 1 


def dist(pos_a, pos_b):
    (x1,y1), (x2,y2) = pos_a, pos_b
    return abs(x1-x2) + abs(y1-y2)


def shortest_path(cave):
    startpos = (0,0)
    endpos = (cave.width-1, cave.height-1)
    queue = SortedSet(key=lambda state: state[1]+state[2])
    mincost = defaultdict(lambda: sys.maxsize)
    mincost[startpos] = 0    
    queue.add( (startpos, 0, dist(startpos,endpos)) )
    while len(queue) > 0:
        pos,cost,heur = queue.pop(0)
        if mincost[pos] < cost:
            continue
        if cost+heur > mincost[endpos]:
            continue
        mincost[pos] = cost
        for (newpos, risk) in cave.nbors(pos):
            queue.add( (newpos, cost+risk, dist(newpos, endpos)) )

    return mincost[endpos]

if __name__=='__main__':
    mapsize = 1 if len(sys.argv)<2 or sys.argv[1]=='1' else 5
    inputs = [ line.strip() for line in sys.stdin ]
    print(shortest_path(Cave(inputs, mapsize)))

