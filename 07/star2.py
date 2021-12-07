import sys

a = list(map(int, sys.stdin.readline().split(',')))

geosum = lambda n: n*(n+1)//2

f = lambda n: sum([ geosum(abs(x-n)) for x in a ])

print(min([f(i) for i in range(min(a), max(a))]))
