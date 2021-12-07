import sys

a = list(map(int, sys.stdin.readline().split(',')))

f = lambda n: sum([ abs(x-n) for x in a ])

print(min([f(i) for i in range(min(a), max(a))]))
