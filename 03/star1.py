import sys

inputs = [ line.strip() for line in sys.stdin ]
maxbit = len(inputs[0])

numbers = [ int(i, base=2) for i in inputs ]


gamma, eps = 0, 0

for pos in range(0,maxbit):
    bit = 2**pos
    ones = sum(map(lambda x: 1 if x & bit else 0, numbers))
    zeros = len(numbers) - ones
    if ones>zeros:
        gamma |= bit
    else:
        eps |= bit

print(gamma * eps)
