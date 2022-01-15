#! /usr/bin/env python3
import sys
import math

class Snailfish:
    def __init__(self, left=None, right=None, digit=None):
        self.left = left
        self.right = right
        self.digit = digit
        self.isleaf = (digit is not None)
        self.prev = None
        self.next = None

    def setNext(self, snailfish):
        self.next = snailfish
        if snailfish is not None:
            snailfish.prev = self

    def setPrev(self, snailfish):
        self.prev = snailfish
        if snailfish is not None:
            snailfish.next = self

    def first(self):
        if self.isleaf: return self
        return self.left.first()

    def last(self):
        if self.isleaf: return self
        return self.right.last()

    def split(self):
        self.left = Snailfish(digit=math.floor(self.digit/2))
        self.left.setPrev(self.prev)
        self.right = Snailfish(digit=math.ceil(self.digit/2))
        self.right.setPrev(self.left)
        self.right.setNext(self.next)
        self.isleaf = False
        self.next = None
        self.prev = None
        self.digit = None

    def explode(self):
        if self.left.prev:
            self.left.prev.digit += self.left.digit
        if self.right.next:
            self.right.next.digit += self.right.digit
        self.setPrev(self.left.prev)
        self.setNext(self.right.next)
        self.isleaf = True
        self.digit = 0

    def magnitude(self):
        return self.digit if self.isleaf else 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def isPair(self):
        return False if self.isleaf else (self.left.isleaf and self.right.isleaf)

    def __repr__(self):
        return f'{self.digit}' if self.isleaf else f'[{self.left},{self.right}]'


def parse_inner(snailfish_string, pos, list_of_digits):
    c = snailfish_string[pos]
    if c.isdigit():
        start, stop = pos, pos+1
        while snailfish_string[stop].isdigit():
            stop += 1
        digit = Snailfish(digit=int(snailfish_string[start:stop]))
        list_of_digits.append(digit)
        return digit, stop
    assert(c=='[')
    left,pos = parse_inner(snailfish_string, pos+1, list_of_digits)
    assert(snailfish_string[pos]==',')
    right,pos = parse_inner(snailfish_string, pos+1, list_of_digits)
    assert(snailfish_string[pos]==']')
    return Snailfish(left=left,right=right), pos+1


def parse(snailfish_string):
    digits=[]
    snailfish, pos = parse_inner(snailfish_string, 0, digits)
    assert(pos == len(snailfish_string))
    
    prev = None
    for sf in digits:
        sf.setPrev(prev)
        prev = sf

    return snailfish

def magnitude(pattern):    
    return parse(pattern).magnitude()

def find_pair_at_depth4(snailfish, depth=0):
    if depth>4 or snailfish.isleaf: return None
    if depth==4 and snailfish.isPair():
        return snailfish
    result = find_pair_at_depth4(snailfish.left, depth+1)
    if result is None:
        result = find_pair_at_depth4(snailfish.right, depth+1)
    return result

def try_explode(snailfish):
    sf = find_pair_at_depth4(snailfish)
    if sf is None:
        return False
    sf.explode()
    return True

def try_split(snailfish):
    sf = snailfish.first()
    while sf:
        if sf.isleaf and sf.digit > 9:
            sf.split()
            return True
        sf = sf.next
    return False

def reduce(snailfish):
    rule_triggered = True
    while rule_triggered:
        rule_triggered = try_explode(snailfish)
        if not rule_triggered:
            rule_triggered = try_split(snailfish)
    return snailfish

def add(patterns):
    sf = parse(patterns[0])
    for pattern in patterns[1:]:
        sf2 = parse(pattern)
        sf.last().setNext(sf2.first())
        sf = Snailfish(left=sf, right=sf2)
        reduce(sf)
    return sf

if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
    inputs = [ line.strip() for line in sys.stdin ]

    if mode == '1':
        print(add(inputs).magnitude())

    if mode == '2':
        max_magnitude = 0
        for i in range(len(inputs)):
            for j in range(len(inputs)):
                if i == j: continue
                patterns = [ inputs[i], inputs[j] ]
                max_magnitude = max(max_magnitude, add(patterns).magnitude())
        print(max_magnitude)
