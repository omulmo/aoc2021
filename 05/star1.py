from collections import defaultdict
import sys

'''To run: python star1.py [1[2] < input.txt'''

vents = defaultdict(lambda: 0)
diagonal = False if len(sys.argv)<2 else sys.argv[1] == '2' 

for line in sys.stdin:
    x1,y1,x2,y2 = map(int, line.strip().replace(' -> ', ',').split(','))
    nx = x2 - x1
    ny = y2 - y1
    if not diagonal and (nx!=0 and ny!=0):
        continue
    dx = 0 if nx == 0 else -1 if nx < 0 else 1
    dy = 0 if ny == 0 else -1 if ny < 0 else 1
    for i in range(0, max(abs(nx),abs(ny))+1):
        vents[x1+i*dx, y1+i*dy] += 1

print( sum( map(lambda x: 1 if x>1 else 0, vents.values()) ) )



        