import sys

inputs=[int(x) for x in sys.stdin]

bigger=0
for i in range(1,len(inputs)):
    if inputs[i]>inputs[i-1]:
        bigger += 1

print(bigger)

