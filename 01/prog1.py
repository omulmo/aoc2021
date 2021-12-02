import sys

inputs=[int(x) for x in sys.stdin]

#bigger=0
#for i in range(1,len(inputs)):
#    if inputs[i]>inputs[i-1]:
#        bigger += 1
#
#print(bigger)

print(sum(map(lambda x: x[1]>x[0], [inputs[i:i+2] for i in range(0,len(inputs)-1)])))

