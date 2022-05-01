import pickle
import numpy as np

def winner(board): # 0=tie none=not finish
    dia_1 = board[0, 0] + board[1, 1] + board[2, 2]
    dia_2 = board[0, 2] + board[1, 1] + board[2, 0]
    for i in range(3):
        if sum(board[i,:])==3 or sum(board[:,i])==3 or dia_1 == 3 or dia_2 ==3:
            return 1
        elif sum(board[i,:])==-3 or sum(board[:,i])==-3 or dia_1 == -3 or dia_2 ==-3:
            return -1
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                return None
    return 0

def printboard(board):
    showboard = []
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                showboard.append("_")
            elif board[i,j] == 1:
                showboard.append('x')
            else:
                showboard.append('o')
    print('The current board is:')
    print(showboard[0], showboard[1], showboard[2])
    print(showboard[3], showboard[4], showboard[5])
    print(showboard[6], showboard[7], showboard[8])
    print(' ')

def valid_position(board):
    valid_positions = []
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                valid_positions.append([i,j])
    return valid_positions

def human_action(board):
    while True:
        row = int(input('choose a row (starting index is 0):'))
        col = int(input('choose a col (starting index is 0):'))
        if board[row, col] == 0:
            action = [row, col]
            return action
        else:
            print("The selected position is not valid")

def random_action(board):
    valid_pos = valid_position(board)
    choice = np.random.choice(len(valid_pos))
    r = valid_pos[choice][0]
    c = valid_pos[choice][1]
    return r, c

def value_action(board):
    global dict
    valid_pos = valid_position(board)
    max_num = -1000
    for r, c in valid_pos:
        next_board = board.copy()
        next_board[r, c] = 1
        next_board_re = next_board.reshape(9)
        next_str = str(next_board_re)
        if dict.get(next_str) is None:
            value = 0
        else:
            value = dict[next_str]
        if value > max_num:
            max_num = value
            row = r
            col = c
    return row, col

def game_value_human(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        print('MC_100,000 vs Human')
        board = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        printboard(board)
        symbol = 1
        while winner(board) is None:
            if symbol == 1:
                r, c = value_action(board)
                board[r, c] = 1
                symbol = -1
                printboard(board)
            else:
                r, c = human_action(board)
                board[r, c] = -1
                symbol = 1
                printboard(board)
        win = winner(board)
        if win == 1:
            print('MC_100,000 wins !')
        elif win == -1:
            print('Human wins !')
        else:
            print('Tie !')

def game_human_value(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        print('Human vs MC_100,000')
        board = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        printboard(board)
        symbol = 1
        while winner(board) is None:
            if symbol == 1:
                r, c = human_action(board)
                board[r, c] = 1
                symbol = -1
                printboard(board)
            else:
                r, c = value_action(board)
                board[r, c] = -1
                symbol = 1
                printboard(board)
        win = winner(board)
        if win == 1:
            print('Human wins !')
        elif win == 1:
            print('MC_100,000 wins !')
        else:
            print('Tie !')

def game_value_random(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        board = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        symbol = 1
        while winner(board) is None:
            if symbol == 1:
                r, c = value_action(board)
                board[r, c] = 1
                symbol = -1
                printboard(board)
            else:
                r, c = random_action(board)
                board[r, c] = -1
                symbol = 1
                print(board)
        win = winner(board)
        if win == 1:
            w += 1
        elif win == -1:
            l += 1
        else:
            t += 1
    return w, l, t

def game_random_value(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        board = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        symbol = 1
        win = None
        while win is None:
            if symbol == 1:
                r, c = random_action(board)
                board[r, c] = 1
                symbol = -1
                win = winner(board)
            else:
                r, c = value_action(board)
                board[r, c] = -1
                symbol = 1
                win = winner(board)

        if win == -1:
            w += 1
        elif win == 1:
            l += 1
        else:
            t += 1
    return w, l, t


def game_random_random(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        board = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        symbol = 1
        win = None
        while win is None:
            if symbol == 1:
                r, c = random_action(board)
                board[r, c] = 1
                symbol = -1
                win = winner(board)
            else:
                r, c = random_action(board)
                board[r, c] = -1
                symbol = 1
                win = winner(board)

        if win == -1:
            w += 1
        elif win == 1:
            l += 1
        else:
            t += 1
    return w, l, t

fr = open('MC_p1', 'rb')
dict = pickle.load(fr)
fr.close()
print(len(dict))
print(game_value_random(100))


fr = open('MC_p2', 'rb')
dict = pickle.load(fr)
fr.close()
print(len(dict))
print(game_value_random(100))


#ans = input("play first or second?")
#if ans =='second':
#    fr = open('MC_p1', 'rb')
#    dict = pickle.load(fr)
#    fr.close()
#    game_value_human(1)
#else:
#    fr = open('MC_p2', 'rb')
#    dict = pickle.load(fr)
#    fr.close()
#    game_human_value(1)