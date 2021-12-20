#! /usr/bin/env python3
from collections import defaultdict
import sys

MAX_STEPS = 1000

def in_range(x, xrange):
    xmin, xmax = xrange
    return xmin <= x and x <= xmax


def find_x_range(vx, xrange):
    x, step = 0, 0
    steps_in_range = set()
    for step in range(1, MAX_STEPS):
        x += vx
        vx = 0 if vx == 0 else vx + (1 if vx < 0 else -1)
        if in_range(x, xrange):
            steps_in_range.add(step)
    return steps_in_range


def find_y_range(vy, yrange, max_steps):
    y, ymax, step, = 0, -sys.maxsize, 0
    steps_in_range = set()
    for step in range(1, max_steps+1):
        y += vy
        vy -= 1
        ymax = max(y, ymax)
        if in_range(y, yrange):
            steps_in_range.add(step)
    return ymax, steps_in_range


def find_best_vx_vy(xrange, yrange):
    assert(in_range(xrange[0], (0, MAX_STEPS)))
    assert(in_range(xrange[1], (0, MAX_STEPS)))
    assert(in_range(yrange[0], (-MAX_STEPS, 0)))
    assert(in_range(yrange[1], (-MAX_STEPS, 0)))
    xsteps = defaultdict(lambda: set())
    for vx in range(0, MAX_STEPS):
        for step in find_x_range(vx, xrange):
            xsteps[step].add(vx)

    max_xsteps = max(xsteps.keys())
    candidates = set()
    for vy in range(-MAX_STEPS, MAX_STEPS):
        ymax, steps = find_y_range(vy, yrange, max_xsteps)
        for step in steps:
            for vx in xsteps[step]:
                candidates.add( (ymax, vx, vy) )

    return sorted(candidates, key=lambda x:x[0], reverse=True)


def parse(inputs):
    # target area: x=20..30, y=-10..-5
    tx1,tx2 = map(int, inputs[0].strip().split(' ')[2].replace('x=','').replace(',','').split('..'))
    ty1,ty2 = map(int, inputs[0].strip().split(' ')[3].replace('y=','').split('..'))
    return (tx1,tx2), (ty1,ty2)


if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
    inputs = [ line.strip() for line in sys.stdin ]

    result = find_best_vx_vy(*parse(inputs))
    if mode == '1':
        print(result[0])
    else:
        print(len(result))
