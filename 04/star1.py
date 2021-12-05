import sys

def bingo(board, lucky_numbers, diagonals_count=False):
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
    for b in boards:
        is_bingo, score = bingo(b, drawn_numbers[:i])
        if is_bingo:
            print(score * drawn_numbers[i-1])
            sys.exit(0)

