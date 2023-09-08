import time
from copy import deepcopy

import numpy as np

ROW_COUNT = 6
COL_COUNT = 7
Q_PIECE = 1
RAND_PIECE = 2

def create_board():
    board = np.zeros((6, 7))
    return board


def first_row(board, col):
    for i in range(ROW_COUNT):
        if board[ROW_COUNT - i - 1][col] == 0:
            return ROW_COUNT - i - 1
    return False


def is_valid(board, col):
    return board[0][col] == 0


def drop_piece(board, piece, col, row):
    board[row][col] = piece


def check_win(board, piece):
    for i in range(COL_COUNT - 3):
        for j in range(ROW_COUNT):
            if board[j][i] == piece and board[j][i + 1] == piece and board[j][i + 2] == piece and board[j][
                i + 3] == piece:
                return True

    for i in range(COL_COUNT):
        for j in range(ROW_COUNT - 3):
            if board[j][i] == piece and board[j + 1][i] == piece and board[j + 2][i] == piece and board[j + 3][
                i] == piece:
                return True

    return False

def valid_actions(board):
    succesors = []
    for col in range(COL_COUNT):
        if is_valid(board, col):
            succesors.append(col)
    return succesors


def node_is_terminal(board):  # Check for terminal node
    return check_win(board, Q_PIECE) or check_win(board, RAND_PIECE) or len(valid_actions(board)) == 0


def get_coordinates(agent_state, board_states):
    x, y = board_states[agent_state]
    return x,y

def get_agent_state(x, y, board_state):
    return board_state.index((x, y))

def create_board_states():
    board_states = []
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
            board_states.append((i, j))
    return board_states

def get_new_state(board, board_states, action): #Action = {0,1,2,3,4,5,6} Number of columns
    if is_valid(board, action) == False:
        return -1, action, 0
    row = first_row(board, action)
    return get_agent_state(action, row, board_states), action, row

def step (action, board,agent_state , piece, board_state):
    game_over = False
    reward = 0
    new_agent_state , x, y = get_new_state(board, board_state, action)
    if new_agent_state == -1:
        game_over = True
        reward = -1
        return agent_state, reward, game_over

    drop_piece(board, piece, action, first_row(board, action))
    win = check_win(board, piece)
    if win :
        reward = 1
        game_over = True
    return new_agent_state, reward, game_over

def one_game(agent1 ,agent2):
    board = create_board()
    board_states = create_board_states()
    state = 0
    game_over = False
    while not game_over:
        valid = valid_actions(board)
        action1 = QLearningAgent.choose_action(agent1, state, valid)
        new_state1 , reward1, end1 = step(action1, board, state, 1, board_states)
        QLearningAgent.update_q_value(agent1, state, action1, new_state1, reward1)
        if end1 & reward1>0:
            #print(board)
            return 1
        if end1 & reward1 == -1:
            #print(board)
            return 2
        valid = valid_actions(board)
        action2 = QLearningAgent.choose_action(agent2, new_state1, valid)
        new_state2 , reward2 , end2 = step(action2, board, new_state1, 2, board_states)
        QLearningAgent.update_q_value(agent2, new_state1, action2, new_state2, reward2)

        if end2 & reward2>0:
            #print(board)
            return 2
        if end2 & reward2 == -1:
            #print(board)
            return 1
        if len(valid_actions(board)) == 0:
            return 0
        state = new_state2
    return 0

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, learning_rate=0.01, discount_factor=0.9, epsilon= 0.3):   #learning_rate ---> alpha     discount_factor ---> gamma
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = []

    def get_q_value(self, state, action):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(COL_COUNT)
        return self.q_table[state][action]

    def update_q_value(self, state, action, new_state, reward):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(COL_COUNT)
        first_term = (1 - self.learning_rate) * self.q_table[state, action]
        second_term = self.discount_factor * self.q_table[new_state, :].max()
        third_term =  self.learning_rate * (reward + second_term)
        new_q_value = first_term + third_term
        self.q_table[state][action] = new_q_value

    def choose_action(self, state, valid_moves):
        rnd = np.random.random()
        if rnd < self.epsilon:
            action = np.random.choice(valid_moves)
        else:
            action = self.q_table[state, :].argmax()
        return action


board = create_board()
board_states = create_board_states()

agent1 = QLearningAgent()
agent1.q_table = np.zeros((42 , 7))
agent2 = QLearningAgent()
agent2.epsilon = 1
agent2.q_table = np.zeros((42 , 7))

stats = 0
games_number = 100000
# start = time.time()
# for i in range(games_number):
#     if i %1000 == 0:
#         print(i)
#     res = one_game(agent1, agent2)
#     if res == 1:
#         stats += 1
# end = time.time()
# print("The time of execution of above program is :",
#       (end-start)/60, "min")
# print(stats)
# print("Win Percentage: "+str(stats/games_number))
#
# file1  = open("agent1.txt", "w+")
# for i in range (42):
#     for j in range(7):
#         file1.write(str(agent1.q_table[i][j]))
#         file1.write(" ")
#     file1.write("\n")

# file2 = open("agent2.txt", "w+")
# for i in range (42):
#     for j in range(7):
#         file1.write(str(agent2.q_table[i][j]))
#         file1.write(" ")
#     file1.write("\n")
x = np.zeros((42, 7))
file1  = open("agent1.txt", "r")
for i in range(42):
    str1 = file1.readline()
    a = str1.split(" ")
    for j in range (7):
        x[i][j] = float(a[j])

agent1.q_table = deepcopy(x)
agent1.epsilon = 0
for i in range(games_number):
    if i%1000 == 0:
        print(i)
    res = one_game(agent1, agent2)
    if res == 1:
        stats+=1
print(stats)
print("Win Percentage: " + str(stats/games_number))






