import sys
from operator import mul
from functools import reduce

'''python3 start1.py [1|2] < input.txt'''

class Graph:
    def __init__(self, inputs):
        self.data = {}
        self.height = 0
        for y,row in enumerate(inputs):
            self.height += 1
            self.width = len(row)
            for x,item in enumerate(row):
                 self.data[x,y] = int(item)

    def __getitem__(self, k):
        return self.data[k]

    def nbors(self, pos):
        x, y = pos
        for a,b in (x-1,y), (x+1,y), (x,y-1), (x,y+1):
            if a<0 or a==self.width: continue
            if b<0 or b==self.height: continue
            yield (a,b)

    def is_local_min(self, x, y):
        smaller = True
        for a,b in self.nbors((x,y)):
            if a<0 or a==self.width: continue
            if b<0 or b==self.height: continue
            smaller = smaller and self[a,b] > self[x,y]
        return smaller

    def get_local_mins(self):
        for x,y in self.data.keys():
            if self.is_local_min(x,y):
                yield (x,y)

    def get_basin_size(self, lowest_pos):
        todo = set([lowest_pos])
        visited=set()
        count=0
        while len(todo)>0:
            pos = todo.pop()
            if pos in visited: continue
            if self[pos]==9: continue
            count += 1
            visited.add(pos)
            for pos in self.nbors(pos):
                todo.add(pos)
        return count

    def get_basins(self):
        basin_sizes = []
        for pos in self.get_local_mins():
            basin_sizes.append(self.get_basin_size(pos))
        return sorted(basin_sizes, reverse=True)


if __name__ == '__main__':
    g = Graph([ x.strip() for x in sys.stdin])
    if len(sys.argv)<2 or sys.argv[1]=='1':
        risk_level = sum(map(lambda pos: 1 + g[pos], (pos for pos in g.get_local_mins())))
        print(risk_level)
    else:
        print(reduce(mul, g.get_basins()[:3]))
