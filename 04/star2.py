import sys

def bingo(board, lucky_numbers):
    score = sum(filter(lambda x: x not in lucky_numbers, board))

    won = lambda row: sum(map(lambda x: x in lucky_numbers, row))==5

    for i in range(0,5):
        if won(board[i*5:5+i*5]):
            print(f'won: {board[i*5:i*5+5]}, drawn={lucky_numbers}')
            return True, score
        if won(board[i::5]):
            print(f'won: {board[i::5]}, drawn={lucky_numbers}')
            return True, score
    return False, score


drawn_numbers = list(map(int, sys.stdin.readline().split(',')))
sys.stdin.readline()

boards = []
board = []
for line in sys.stdin:
    board.extend(map(int, line.strip().replace('  ',' ').split()))
    if len(board)==25:
        boards.append(board)
        board = []

for i in range(1,len(drawn_numbers)):
    remains = []
    last_score = 0
    for b in boards:
        is_bingo, score = bingo(b, drawn_numbers[:i])
        if not is_bingo:
            remains.append(b)
        else:
            last_score = score
    print(f'Round {i}: {len(remains)} boards left')
    boards = remains
    if len(remains)==0:
        print(last_score * drawn_numbers[i-1])
        break
