import random as rng

grid = [['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']]
def reset_grid():
    grid.clear()
    for i in range(3):
        grid.append(['-', '-', '-'])

def show_grid():
    print('  a b c')
    for rowNum, row in enumerate(grid):
        print(rowNum + 1, end=' ')
        for space in row:
            print(space, end=' ')
        print()

def get_winner():
    if set([j for i in grid for j in i]) == {'x', 'o'}: # check for tie
        return 'Nobody'
    for i, row in enumerate(grid): # check rows and columns
        col = [grid[j][i] for j in range(3)]
        if set(row) == {'x'} or set(col) == {'x'}:
            return 'x'
        if set(row) == {'o'} or set(col) == {'o'}:
            return 'o'
    diag1 = [grid[i][i] for i in range(3)] # check diagonals
    diag2 = [grid[i][-i-1] for i in range(3)]
    if set(diag1) == {'x'} or set(diag2) == {'x'}:
        return 'x'
    if set(diag1) == {'o'} or set(diag2) == {'o'}:
        return 'o'

def get_input():
    pos = input().lower()  # get input and convert to indices
    pos = pos[::-1] if pos[1].isalpha() else pos
    row, col = int(pos[1]) - 1, ord(pos[0]) - 97
    if 0 <= col <= 2 and 0 <= row <= 2:
        return row, col

def start_game():
    reset_grid()
    turn = 'x'
    while get_winner() is None:
        print(turn + '\'s turn')
        show_grid()

        try:
            x, y = (rng.randint(0, 2), rng.randint(0, 2)) if turn == 'x' else get_input()
        except (TypeError, IndexError):
            print('Invalid input. Use a3, 2c, etc.'); continue
        if grid[x][y] == '-': # prevent placing on claimed spaces
            grid[x][y] = turn
        else:
            print('you absolute fucking idiot... \n'); continue

        turn = 'x' if turn == 'o' else 'o' # swap turns
        print(50 * '\n') # clear console for next turn
    show_grid()
    print(get_winner(), 'wins')

def start_random():
    reset_grid()
    turn, count = 'x', 0
    while get_winner() is None:
        if 1:
            x, y = rng.randint(0,2), rng.randint(0,2)
        if grid[x][y] == '-':
            grid[x][y] = turn
        else:
            continue
        turn = 'x' if turn == 'o' else 'o'
        count += 1

    return get_winner()

def loop_random(n=5000):
    ties, x, o = 0, 0, 0
    for _ in range(n):
        winner = start_random()
        show_grid()
        print()
        if winner == 'Nobody':
            ties += 1
        elif winner == 'x':
            x += 1
        elif winner == 'o':
            o += 1

    print('tie', 'x', 'o', sep='     ')
    print(ties/n, x/n, o/n)

loop_random()