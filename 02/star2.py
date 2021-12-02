import sys

x, y, aim = 0, 0, 0

for line in sys.stdin:
    direction, n = line.strip().split()
    n = int(n)
    if direction=='forward':
        x += n
        y += aim*n
    elif direction=='down':
        aim += n
    elif direction=='up':
        aim -= n
    else:
        raise Exception

print(x * y)
