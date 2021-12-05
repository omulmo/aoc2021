import sys

def reduce(array, bit, filter_on_majority):
    if len(array)==1: return array[0]
    ones = sum(map(lambda x: 1 if x & bit else 0, array))
    zeros = len(array) - ones
    if filter_on_majority:
        match = bit if ones >= zeros else 0
    else:
        match = bit if ones < zeros else 0
    return reduce(list(filter(lambda x: x & bit == match, array)), bit//2, filter_on_majority)

inputs = [ line.strip() for line in sys.stdin ]
maxbit = len(inputs[0])-1
numbers = [ int(i, base=2) for i in inputs ]

oxygen = reduce(numbers, 2**maxbit, True)
co2 = reduce(numbers, 2**maxbit, False)

print(oxygen * co2)
