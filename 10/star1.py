import sys

'''python star1.py [1|2] < input.txt'''

LEFT  = '([{<'
RIGHT = ')]}>'
PAIRS = { '{':'}', '(':')', '[':']', '<':'>' }
POINTS ={ '}':1197, ')':3, ']':57, '>':25137, '-':0 }

def parse(line):
    stack = []
    for nxt in line:
        if nxt in LEFT:
            stack.append(PAIRS[nxt])
            continue
        expect = stack.pop()
        if nxt == expect:
            continue
        return POINTS[nxt], stack
    return 0, stack

def star2score(parse_result):
    (score,stack) = parse_result
    if score!=0: return 0
    s = 0
    while len(stack)>0:
        c = stack.pop()
        s = s*5 + 1 + RIGHT.index(c)
    return s

if __name__=='__main__':
    do1 = True if len(sys.argv)<2 or sys.argv[1]=='1' else False
    scores = [ parse(line.strip()) for line in sys.stdin ]
    if do1:
        print(sum(x[0] for x in scores))
    else:
        res = sorted( filter(lambda x: x>0, (star2score(x) for x in scores)) )
        print(res[len(res)//2])
