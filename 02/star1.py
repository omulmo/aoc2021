import sys

x, y = 0, 0

for line in sys.stdin:
    direction, n = line.strip().split()
    n = int(n)
    if direction=='forward':
        x += n
    elif direction=='down':
        y += n
    elif direction=='up':
        y -= n
    else:
        raise Exception

print(x * y)
