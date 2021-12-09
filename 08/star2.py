from collections import defaultdict
from functools import reduce
import sys

DIGITS = [ 'abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg' ]
#
#        aaa
#       b   c
#       b   c
#        ddd
#       e   f
#       e   f
#        ggg

def analyze(signals, digits):
    assert(len(signals)==10)
    assert(len(digits)==4)
    signals = sorted(signals, key=len)

    # 1,4,7,8 = known because of unique no. of segments
    # 2,3,5 = 5 segments
    # 0,6,9 = 6 segments
    one = signals[0]
    seven = signals[1]
    four = signals[2]
    eight = signals[9]

    a = seven.difference(one)
    bd = four.difference(one)
    eg = eight.difference(seven).difference(bd)

    # of 2,3,5 bd only exist in 5
    five=set()
    for signal in signals[3:6]:
        if bd.issubset(signal):
            five = set(signal)
    assert(len(five)==5)

    nine = seven.union(five)
    e = eight.difference(nine)
    six = five.union(e)
    c = eight.difference(six)
    f = one.difference(c)
    g = eg.difference(e)

    # 3 = acfg + d
    acfg = a.union(c).union(f).union(g)
    d, three = set(), set()
    for signal in signals[3:6]:
        diff = signal.difference(acfg)
        if len(diff)==1:
            d = diff
            three = signal
    assert(len(three)==5)
    zero = eight.difference(d)
    two = three.union(e).difference(f)

    patterns = [zero,one,two,three,four,five,six,seven,eight,nine]
    return reduce(lambda cur,nxt: cur*10+nxt, map(patterns.index, digits))


sum = 0
for line in sys.stdin:
    signalset = list(map(set, line.strip().replace(' | ', ' ').split(' ')))
    sum += analyze(signalset[0:10], signalset[10:])
    
print(sum)