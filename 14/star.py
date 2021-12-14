#! /usr/bin/env python3
from collections import defaultdict
import sys

def parse(inputs):
    polymer = defaultdict(lambda: 0)
    a = inputs[0][0]
    for b in inputs[0][1:]:
        polymer[a,b] +=1
        a = b
    last_token = a

    ruleset = {}
    for line in inputs[2:]:
        combo, insert = line.split(' -> ')
        a,b = combo[:]
        ruleset[a,b] = insert
    return polymer, last_token, ruleset


def sequence(polymer, ruleset):
    result = defaultdict(lambda: 0)
    for (a,b),count in polymer.items():
        if (a,b) in ruleset:
            n = ruleset[a,b]
            result[a,n] += count
            result[n,b] += count
        else:
            result[a,b] += count
    return result


def score(polymer, last_token):
    buckets = defaultdict(lambda: 0)
    for (a,b),count in polymer.items():
        buckets[a] += count
    buckets[last_token] += 1

    v = sorted(buckets.items(), key=lambda x:x[1])
    hi, lo = v[-1], v[0]
    return hi[1]-lo[1]


if __name__=='__main__':
    iterations = 10 if len(sys.argv)<2 or sys.argv[1]=='1' else 40

    polymer, last_token, ruleset = parse([line.strip() for line in sys.stdin])

    for i in range(iterations):
        polymer = sequence(polymer, ruleset)
    print(score(polymer, last_token))

