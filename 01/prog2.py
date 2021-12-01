import sys

inputs=[int(x) for x in sys.stdin]

sums=[sum(inputs[i:i+3]) for i in range(0,len(inputs)-2)]

bigger=0
for i in range(1,len(sums)):
    if sums[i]>sums[i-1]:
        bigger += 1

print(bigger)

