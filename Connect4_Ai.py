import math
import random
from copy import deepcopy
import numpy as np
import pygame
import button

ROW_COUNT = 6
COL_COUNT = 7
EMPTY_COUNT = ROW_COUNT * COL_COUNT
BACKGROUND_COLOR = (222, 227, 227)
BLUE = (57, 132, 237)
RED = (224, 76, 63)
YELLOW = (240, 205, 50)
GRAY = (107, 106, 101)
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2


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


def draw_board(board):
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (i * SQUARE_SIZE, j * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, GRAY, (
                int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int(j * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS,
                               5)
            pygame.draw.circle(screen, BACKGROUND_COLOR, (
                int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int(j * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                               RADIUS - 5)

    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
            if board[j][i] == 1:
                pygame.draw.circle(screen, RED, (
                    int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int((j + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS - 5)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int((j + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS - 5)
    pygame.display.update()


def successors(board, piece):
    succesors = []
    for col in range(COL_COUNT):
        new_board = deepcopy(board)
        if is_valid(board, col):
            drop_piece(new_board, piece, col, first_row(new_board, col))
            succesors.append(new_board)
    return succesors


def node_is_terminal(board):  # Check for terminal node
    return check_win(board, AI_PIECE) or check_win(board, PLAYER_PIECE) or len(successors(board, PLAYER_PIECE)) == 0


def slice_score(slice, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if (piece == PLAYER_PIECE):
        opp_piece = AI_PIECE
    slice = slice.tolist()
    if slice.count(piece) == 4:
        score += 100
    elif slice.count(piece) == 3 and slice.count(0) == 1:
        score += 5
    elif slice.count(piece) == 2 and slice.count(0) == 2:
        score += 2
    if slice.count(opp_piece) == 3 and slice.count(0) == 1:
        score -= 4
    elif slice.count(opp_piece) == 2 and slice.count(0) == 2:
        score -= 1
    return score


def heuristic(board, piece):
    h = 0
    boardC = deepcopy(board)
    boardC = np.array(boardC)

    center_col_array = board[:, COL_COUNT // 2]
    center_col_array = center_col_array.tolist()
    center_count = center_col_array.count(piece)
    h += center_count * 3

    for i in range(ROW_COUNT):  # Horizental Scoring
        row_array = boardC[i, :]
        for j in range(COL_COUNT - 3):
            slice = row_array[j:j + 4]
            h += slice_score(slice, piece)

    for i in range(COL_COUNT):  # Vertical Scoring
        col_array = board[: i]
        for j in range(ROW_COUNT - 3):
            slice = col_array[j:j + 4]
            h += slice_score(slice, piece)

    return h


def minimax(board, depth, maximizing_player):  # Minimax algorithm

    succesor_ai = successors(board, AI_PIECE)
    succesor_pl = successors(board, PLAYER_PIECE)
    is_terminal = node_is_terminal(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, PLAYER_PIECE):
                return (None, -10000000000000)
            elif check_win(board, AI_PIECE):
                return (None, 10000000000000)
            else:
                return (None, 0)
        else:
            return (None, heuristic(board, AI_PIECE))
    if maximizing_player:
        value = -math.inf
        c_board = random.choice(succesor_ai)
        for boards in succesor_ai:
            new_score = minimax(boards, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                c_board = boards
        return c_board, value
    else:
        value = math.inf
        c_board = random.choice(succesor_pl)
        for boards in succesor_pl:
            new_score = minimax(boards, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                c_board = boards
        return c_board, value


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):  # Minimax include alpha_beta pruning
    succesor_ai = successors(board, AI_PIECE)
    succesor_pl = successors(board, PLAYER_PIECE)
    is_terminal = node_is_terminal(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(board, PLAYER_PIECE):
                return (None, -10000000000000)
            elif check_win(board, AI_PIECE):
                return (None, 10000000000000)
            else:
                return (None, 0)
        else:
            return (None, heuristic(board, AI_PIECE))
    if maximizing_player:
        value = -math.inf
        c_board = random.choice(succesor_ai)
        for boards in succesor_ai:
            new_score = minimax_alpha_beta(boards, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                c_board = boards
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return c_board, value
    else:
        value = math.inf
        c_board = random.choice(succesor_pl)
        for boards in succesor_pl:
            new_score = minimax_alpha_beta(boards, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                c_board = boards
            beta = min(beta, value)
            if alpha >= beta:
                break
        return c_board, value


board = create_board()
game_over = False

width = COL_COUNT * SQUARE_SIZE  # Initialize the game window
height = (ROW_COUNT + 1) * SQUARE_SIZE
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()
pygame.display.set_caption('Connect 4')

x = SQUARE_SIZE / 2  # Initial cordinate of circle
y = SQUARE_SIZE / 2

turn = random.randint(0, 1)  # Switching turns between player and ai

chosen = 0  # Select mode between minimax and alpha_beta pruning
print(board)
draw_board(board)

menu = 1  # Variable for menu screen
# load button images
mini_image = pygame.image.load('pics/Min-2.png').convert_alpha()
alpha_image = pygame.image.load('pics/Alpha-2.png').convert_alpha()
title_image = pygame.image.load('pics/Connect4-2.png').convert_alpha()
coin_image = pygame.image.load('pics/Coin.png').convert_alpha()
# create button
mini_button = button.Button(width / 2 - 120, 430, mini_image, 0.5)
alpha_button = button.Button(width / 2 - 120, 300, alpha_image, 0.5)
title_button = button.Button(width / 2 - 250, 70, title_image, 1)
coin_button = button.Button(width / 2, 230, coin_image, 1)
m = True
font_con = pygame.font.SysFont("Phosphate", 72)
while not game_over:
    if not menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and x < width - 2 * RADIUS:
                    pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                    x += SQUARE_SIZE
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (x, y), RADIUS - 5)
                pygame.display.update()

                if event.key == pygame.K_LEFT and x > 2 * RADIUS:
                    pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                    x -= SQUARE_SIZE
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (x, y), RADIUS - 5)

                pygame.display.update()

                if event.key == pygame.K_DOWN:
                    # pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                    if turn == PLAYER:
                        col = int(math.floor(x / SQUARE_SIZE))
                        if is_valid(board, col):
                            row = first_row(board, col)
                            drop_piece(board, 1, col, row)
                            EMPTY_COUNT = EMPTY_COUNT - 1
                            if check_win(board, 1):
                                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                                label = font_con.render("Player 1 wins!!", 1, RED)
                                screen.blit(label, (40, 10))
                                print("PLAYER1 WIN")
                                m = False
                                game_over = True
                            if EMPTY_COUNT <= 0:
                                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                                label = font_con.render("Tied Up!!", 1, BLUE)
                                screen.blit(label, (40, 10))
                                print("TIED UP")
                                m = False
                                game_over = True
                            turn += 1
                            turn = turn % 2
                            if m:
                                pygame.draw.circle(screen, RED, (x, y), RADIUS - 5)
                            draw_board(board)

        if turn == AI and chosen == 0 and not game_over:
            board, min_score = minimax_alpha_beta(board, 6, -math.inf, math.inf, True) #Depth = 6
            if board.all() == None:
                EMPTY_COUNT = 1
            pygame.time.wait(500)
            EMPTY_COUNT = EMPTY_COUNT - 1
            if EMPTY_COUNT <= 0:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                label = font_con.render("Tied Up!!", 1, BLUE)
                screen.blit(label, (40, 10))
                print("TIED UP")
                game_over = True
            if check_win(board, 2):
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                label = font_con.render("AI wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                print("AI WINS")
                game_over = True

            draw_board(board)
            turn += 1
            turn = turn % 2

        elif turn == AI and chosen == 1 and not game_over:
            board, min_score = minimax(board, 4, True)    #Depth = 4
            if board.all() == None:
                EMPTY_COUNT = 1
            pygame.time.wait(500)
            EMPTY_COUNT = EMPTY_COUNT - 1
            if EMPTY_COUNT <= 0:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                label = font_con.render("Tied Up!!", 1, BLUE)
                screen.blit(label, (40, 10))
                print("TIED UP")
                game_over = True
            if check_win(board, 2):
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                label = font_con.render("AI wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                print("AI WINS")
                game_over = True
            draw_board(board)
            turn += 1
            turn = turn % 2

        if game_over:
            pygame.time.wait(4000)

        pygame.display.update()
    else:
        screen.fill((59, 59, 59))  # 43, 43, 43
        if title_button.draw(screen):
            pass
        if coin_button.draw(screen):
            pass
        if mini_button.draw(screen):
            menu = 0
            chosen = 1
            screen.fill(BACKGROUND_COLOR)
            draw_board(board)
        elif alpha_button.draw(screen):
            menu = 0
            chosen = 0
            screen.fill(BACKGROUND_COLOR)
            draw_board(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        pygame.display.update()
pygame.quit()

print(board)
