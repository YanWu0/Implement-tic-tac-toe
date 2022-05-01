import numpy as np
import pickle

def winner(board): # 0=tie none=not finish

    for i in range(3):
        if (sum(board[i,:])==3) or (sum(board[:,i])==3):
            return 1
        elif (sum(board[i,:])==-3) or (sum(board[:,i])==-3):
            return -1

    dia_1 = board[0, 0] + board[1, 1] + board[2, 2]
    dia_2 = board[0, 2] + board[1, 1] + board[2, 0]

    if (dia_1 == 3) or (dia_2 == 3):
        return 1
    elif (dia_1 == -3) or (dia_2 ==-3):
        return -1

    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                return None
    return 0

def valid_position(board):
    valid_positions = []
    for i in range(3):
        for j in range(3):
            if board[i,j] == 0:
                valid_positions.append([i,j])
    return valid_positions

# training
def train(rounds=1000, epsil=0.3, gamma=0.9):
    state_value_dic_1 = {}
    state_value_dic_2 = {}
    for i in range(rounds):
        if i % 1000 == 0:
            print('Training the '+str(i)+' round')
        states_1 = []
        states_2 = []
        symbol = 1
        board = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        while winner(board) is None:
            if symbol == 1:
                valid_pos = valid_position(board)
                decimal = np.random.uniform(0, 1)
                if decimal <= epsil:
                    choice = np.random.choice(len(valid_pos))
                    r = valid_pos[choice][0]
                    c = valid_pos[choice][1]
                    board[r,c] = symbol
                    states_1.append(str(board.reshape(9)))
                    symbol = -1 * symbol
                else:
                    max_val = -999
                    for r,c in valid_pos:
                        tem_board = board.copy()
                        tem_board[r,c] = symbol
                        string = str(tem_board.reshape(9))
                        if state_value_dic_1.get(string) is None:
                            val = 0
                        else:
                            val = state_value_dic_1.get(string)
                        if val > max_val:
                            max_val = val
                            row = r
                            col = c
                    board[row,col] = symbol
                    states_1.append(str(board.reshape(9)))
                    symbol = -1 * symbol
            else:
                valid_pos = valid_position(board)
                decimal = np.random.uniform(0, 1)
                if decimal <= epsil:
                    choice = np.random.choice(len(valid_pos))
                    r = valid_pos[choice][0]
                    c = valid_pos[choice][1]
                    board[r, c] = symbol
                    states_2.append(str(board.reshape(9)))
                    symbol = -1 * symbol
                else:
                    max_val = -999
                    for r, c in valid_pos:
                        tem_board = board.copy()
                        tem_board[r, c] = symbol
                        string = str(tem_board.reshape(9))
                        if state_value_dic_2.get(string) is None:
                            val = 0
                        else:
                            val = state_value_dic_2.get(string)
                        if val > max_val:
                            max_val = val
                            row = r
                            col = c
                    board[row, col] = symbol
                    states_2.append(str(board.reshape(9)))
                    symbol = -1 * symbol

        win = winner(board)
        if win == 1:
            reward_1 = 1
            reward_2 = 0
        elif win == -1:
            reward_1 = 0
            reward_2 = 1
        elif win == 0:
            reward_1 = 0.1
            reward_2 = 0.5

        values_1 = np.zeros(len(states_1))
        for j in range(len(states_1)):
            values_1[j] = reward_1 * (gamma ** (len(states_1) - j - 1))
        for k in range(len(states_1)):
            if state_value_dic_1.get(states_1[k]) is None:
                state_value_dic_1[states_1[k]] = values_1[k]
            else:
                state_value_dic_1[states_1[k]] = state_value_dic_1[states_1[k]] + (1/(1+i))*(values_1[k] - state_value_dic_1[states_1[k]])

        values_2 = np.zeros(len(states_2))
        for j in range(len(states_2)):
            values_2[j] = reward_2 * (gamma ** (len(states_2) - j - 1))
        for k in range(len(states_2)):
            if state_value_dic_2.get(states_2[k]) is None:
                state_value_dic_2[states_2[k]] = values_2[k]
            else:
                state_value_dic_2[states_2[k]] = state_value_dic_2[states_2[k]] + (1/(1+i))*(values_2[k] - state_value_dic_2[states_2[k]])

    fw_1 = open('MC_p1', 'wb')
    pickle.dump(state_value_dic_1, fw_1)
    fw_1.close()
    fw_2 = open('MC_p2', 'wb')
    pickle.dump(state_value_dic_2, fw_2)
    fw_2.close()

train(250000)


















