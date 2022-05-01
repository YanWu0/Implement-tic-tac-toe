from keras.models import load_model
import numpy as np


def printboard(board):
    lett = []
    for i in range(9):
        if board[i] == 1:
            lett.append('x')
        elif board[i] == -1:
            lett.append('o')
        else:
            lett.append('-')
    print(lett[0], lett[1], lett[2])
    print(lett[3], lett[4], lett[5])
    print(lett[6], lett[7], lett[8])

def winner(board):

    if (board[0] == board[1] == board[2]) and (board[0] != 0):
        return board[0]
    elif (board[3] == board[4] == board[5]) and (board[3] != 0):
        return board[3]
    elif (board[6] == board[7] == board[8]) and (board[6] != 0):
        return board[6]
    elif (board[0] == board[3] == board[6]) and (board[0] != 0):
        return board[0]
    elif (board[1] == board[4] == board[7]) and (board[1] != 0):
        return board[1]
    elif (board[2] == board[5] == board[8]) and (board[2] != 0):
        return board[2]
    elif (board[0] == board[4] == board[8]) and (board[0] != 0):
        return board[0]
    elif (board[2] == board[4] == board[6]) and (board[2] != 0):
        return board[2]

    for i in range(9):
        if board[i] == 0:
            return None
    return 0

def one_hot(state):
    current_state = []
    for square in state:
        if square == 0:
            current_state.append(1)
            current_state.append(0)
            current_state.append(0)
        elif square == 1:
            current_state.append(0)
            current_state.append(1)
            current_state.append(0)
        elif square == -1:
            current_state.append(0)
            current_state.append(0)
            current_state.append(1)
    return current_state

def valid_positions(board):
    valid_pos = []
    for i in range(9):
        if board[i] == 0:
            valid_pos.append(i)
    return valid_pos

def random_action(board):
    valid_pos = valid_positions(board)
    choice = np.random.choice(len(valid_pos))
    return valid_pos[choice]

def game_q_random(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        model = load_model('tic_tac_toe.h5')
        symbol = 1
        while winner(board) is None:
            if symbol == 1:
                pre = model.predict(np.asarray([one_hot(board)]), batch_size=1)[0]
                max_val = -1000
                for j in range(9):
                    if board[j] == 0:
                        if pre[j] > max_val:
                            max_val = pre[j]
                            action = j
                board[action] = 1
                symbol = -1
            else:
                action = random_action(board)
                board[action] = -1
                symbol = 1

        res = winner(board)
        if res == 1:
            w += 1
        elif res == -1:
            l += 1
        else:
            t += 1
    return w, l, t


def game_random_q(times):
    w = 0
    l = 0
    t = 0
    for i in range(times):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        model = load_model('tic_tac_toe_2.h5')
        symbol = 1
        while winner(board) is None:
            if symbol == 1:
                action = random_action(board)
                board[action] = 1
                symbol = -1
            else:
                pre = model.predict(np.asarray([one_hot(board)]), batch_size=1)[0]
                max_val = -1000
                for j in range(9):
                    if board[j] == 0:
                        if pre[j] > max_val:
                            max_val = pre[j]
                            action = j
                board[action] = -1
                symbol = 1
        res = winner(board)
        if res == -1:
            w += 1
        elif res == 1:
            l += 1
        else:
            t += 1
    return w, l, t

print(game_q_random(100))
print(game_random_q(100))