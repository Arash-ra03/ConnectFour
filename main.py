import math

import numpy as np
import pygame

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
            int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int(j * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS, 5)
            pygame.draw.circle(screen, BACKGROUND_COLOR, (
            int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int(j * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS - 5)

    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
            if board[j][i] == 1:
                pygame.draw.circle(screen, RED, (
                    int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int((j + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(i * SQUARE_SIZE + SQUARE_SIZE / 2), int((j + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
game_over = False

width = COL_COUNT * SQUARE_SIZE  # initialize the game window
height = (ROW_COUNT + 1) * SQUARE_SIZE
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()
pygame.display.set_caption('Connect 4')

x = SQUARE_SIZE / 2
y = SQUARE_SIZE / 2

draw_board(board)
turn = 1
# drop_piece(board, 1, 3,first_row(board,3))
# drop_piece(board, 2, 3,first_row(board,3))
print(board)
draw_board(board)
font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and x < width - 2 * RADIUS:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                x += SQUARE_SIZE
                if turn == 0:
                    pygame.draw.circle(screen, RED, (x, y), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (x, y), RADIUS)
            pygame.display.update()

            if event.key == pygame.K_LEFT and x > 2 * RADIUS:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                x -= SQUARE_SIZE
                if turn == 0:
                    pygame.draw.circle(screen, RED, (x, y), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (x, y), RADIUS)
            pygame.display.update()

            if event.key == pygame.K_DOWN:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
                if turn == 0:
                    col = int(math.floor(x / SQUARE_SIZE))
                    if is_valid(board, col):
                        row = first_row(board, col)
                        drop_piece(board, 1, col, row)
                        EMPTY_COUNT = EMPTY_COUNT - 1
                        if check_win(board, 1):
                            label = font.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            print("PLAYER1 WIN")
                            game_over = True
                if turn == 1:
                    col = int(math.floor(x / SQUARE_SIZE))
                    if is_valid(board, col):
                        row = first_row(board, col)
                        drop_piece(board, 2, col, row)
                        EMPTY_COUNT = EMPTY_COUNT - 1
                        if check_win(board, 2):
                            label = font.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            print("PLAYER2 WIN")
                            game_over = True
                if EMPTY_COUNT == 0:
                    label = font.render("Tied Up!!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    print("TIED UP")
                    game_over = True

                draw_board(board)
                turn += 1
                turn = turn % 2
                if game_over:
                    pygame.time.wait(4000)

    pygame.display.update()

pygame.quit()

print(board)
