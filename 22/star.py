#! /usr/bin/env python3
import sys
from operator import mul
from functools import reduce

class Cuboid:
    def __init__(self, dims):
        self.dims = dims
        self.active = True
        self.overlaps = []

    def subtract(self, other):
        overlap = self.overlap(other)
        if overlap is None: return
        if overlap.dims == self.dims:
            self.active = False
            return
        for cutout in self.overlaps:
            cutout.subtract(overlap)
        self.overlaps = list(filter(lambda x:x.active, self.overlaps))
        self.overlaps.append(overlap)

    def count(self):
        total = reduce(mul, (b-a+1 for a,b in self.dims))
        return total - sum(cutout.count() for cutout in self.overlaps)

    def overlap(self, other):
        dims = []
        for (a,b),(c,d) in zip(self.dims, other.dims):
            if b<c or d<a:
                return None
            dims.append( (max(a,c), min(b,d)) )
        return Cuboid(tuple(dims))


def update_state(cuboids, instruction, with_bounding_box=True):
    mode, dim = instruction.split()
    assert(mode in ('on','off'))
    cuboid = Cuboid(tuple(map(lambda x: tuple(map(int, x[2:].split('..'))), dim.split(','))))
    if with_bounding_box:
        cuboid = Cuboid(tuple([(-50,50)] * 3)).overlap(cuboid)
        if cuboid is None:
            return state

    for other in cuboids:
        other.subtract(cuboid)

    if mode == 'on':
        cuboids.append(cuboid)

    cuboids = list(filter(lambda x: x.active, cuboids))
    return cuboids


if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]

    with_bounding_box = True if mode == '1' else False
    state = []
    for instruction in (line.strip() for line in sys.stdin):
        state = update_state(state, instruction, with_bounding_box)
    print(sum(cuboid.count() for cuboid in state))
