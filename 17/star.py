#! /usr/bin/env python3
import sys

def in_range(x, xrange):
    xmin, xmax = xrange
    return xmin <= x and x <= xmax

def is_a_hit(x,y,tx,ty):
    return in_range(x,tx) and in_range(y,ty) 

def will_it_hit(vx, vy, targetx, targety):
    x,y = 0,0
    xmin,xmax = targetx
    ymin,ymax = targety
    hit = False
    while x<max and y<ymin:
        x += vx
        y += vy
        vx = 0 if vx==0 else vx + (1 if vx < 0 else -1)
        vy -= 1
        if is_a_hit(x,y,targetx,targety):
            hit = True
    return True


def parse(inputs):
    # target area: x=20..30, y=-10..-5
    tx1,tx2 = map(int, inputs[0].strip().split(' ')[2].replace('x=','').replace(',').split('..'))
    ty1,ty2 = map(int, inputs[0].strip().split(' ')[3].replace('y=','').split('..'))
    return (tx1,tx2), (ty1,ty2)


if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
