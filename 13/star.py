#! /usr/bin/env python3
import sys

class Paper:
    def __init__(self, inputs):
        self.data = set()
        self.w = 0
        self.h = 0
        self.instructions = []
        coords = True
        for line in (x.strip() for x in inputs):
            if len(line)==0:
                coords = False
                continue
            if coords:
                x,y = map(int,line.split(','))      # 43,12
                self.w = max(self.w, x)
                self.h = max(self.h, y)
                self.data.add( (x,y) )
            else:
                axis, pos = line.split(' ')[2].split('=')    # fold along x=32
                self.instructions.append( (axis,int(pos)) )

    def stars(self):
        return len(self.data)

    def fold(self, instructions=sys.maxsize):
        while instructions>0 and len(self.instructions)>0:
            instructions -= 1
            axis, line = self.instructions.pop(0)
            folded = set()
            for x,y in self.data:
                if axis=='x' and x > line:
                    x = line - (x-line)
                if axis=='y' and y > line:
                    y = line - (y-line)
                folded.add( (x,y) )
            self.data = folded
            if axis == 'x': self.w = line-1
            if axis == 'y': self.h = line-1
        return self

    def __repr__(self):
        return '\n'.join( ''.join('#' if (x,y) in self.data else '.' for x in range(self.w+1)) for y in range(self.h+1) )

if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
    if mode == '1':
        print(Paper(sys.stdin).fold(1).stars())
    else:
        print()
        print(Paper(sys.stdin).fold())
        print()
