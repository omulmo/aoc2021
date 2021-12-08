import sys

DIGITS = [ 'abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg' ]

def analyze(signals, digits):
    assert(len(signals)==10)
    assert(len(digits)==4)
    candidates = [ [] for _ in '0123456789' ]
    for signal in signals:
        for i in range(len(DIGITS)):
            if len(signal)==len(DIGITS[i]):
                candidates[i].append(signal)
    match = {}
    for i in range(10):
        if len(candidates[i])==1:
            match[candidates[i][0]] = i
    result = []
    for digit in digits:
        if digit in match:
            result.append(match[digit])
        else:
            result.append(-1)

    return result

digits = []
for line in sys.stdin:
    signalset = list(map(lambda x: ''.join(sorted(x)), line.strip().replace(' | ', ' ').split(' ')))
    res = analyze(signalset[0:10], signalset[10:])
    print(res)
    digits.extend( res )
    
print(sum(map(lambda x: 1 if x in [1,4,7,8] else 0, digits)))
