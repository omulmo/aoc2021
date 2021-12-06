import sys

'''To run: python3 star1.py [days] < input.txt   (default: 80)'''

days = 80 if len(sys.argv)<2 else int(sys.argv[1]) 

state = [0]*9

for fish_state in map(int, sys.stdin.readline().strip().split(',')):
    state[fish_state] += 1

for day in range(1,days+1):
    breeding = state.pop(0)
    state[6] += breeding
    state.append(breeding)

print(f'After {days} days: {sum(state)}')
