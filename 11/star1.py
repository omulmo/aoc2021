import sys

class Cave:
    def __init__(self, inputs):
        self.width = len(inputs[0])
        self.height = len(inputs)
        self.map = dict( ((col,row), int(inputs[row][col])) for col in range(self.width) for row in range(self.height) )
        self.iterations = 0
        self.flashes = 0

    def view(self):
        return '\n'.join( (''.join(f'{self.map[col,row]}' for col in range(self.width)) for row in range(self.height)) )

    def step(self, ntimes=1):
        if ntimes>1:
            self.step(ntimes-1)
        self.iterations += 1
        flash = set()
        for pos in self.map.keys():
            self.map[pos] += 1
            if self.map[pos] > 9: flash.add(pos)

        has_flashed = set()
        while len(flash)>0:
            pos = flash.pop()
            if pos in has_flashed: continue
            self.map[pos] = 0
            has_flashed.add(pos)
            for nbor in self.nbors(pos):
                self.map[nbor] += 1
                if self.map[nbor] > 9: flash.add(nbor)
        
        self.flashes += len(has_flashed)
        for pos in has_flashed:
            self.map[pos] = 0

    def nbors(self, pos):
        x,y = pos
        for a in x-1, x, x+1:
            for b in y-1, y, y+1:
                if (a,b) == pos: continue
                if a<0 or a==self.width: continue
                if b<0 or b==self.height: continue
                yield a,b

    def time_to_synchronize(self):
        prev = self.flashes
        while self.iterations<10000:
            self.step()
            if self.flashes - prev == self.width*self.height:
                return self.iterations
            prev = self.flashes
        return -1


if __name__=='__main__':
    c = Cave([line.strip() for line in sys.stdin])
    c.step(100)
    print(f'After 100 steps: {c.flashes} flashes')
    print(f'In sync after {c.time_to_synchronize()} iterations')
