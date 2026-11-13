import sys
import pygame
import numpy as np

pygame.init()

White = (255, 255, 255)
Gray = (180, 180, 180)
Red = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)

Width = 300
Height = 300
Line_Width = 5
Board_Rows = 3
Board_cols = 3
Square_size = Width // Board_cols
Circle_radius = Square_size // 3
Circle_width = 15
Cross_width = 25

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tic Tac Toe AI')

board = np.zeros((Board_Rows, Board_cols))

def draw_lines(color=White):
    for i in range(1, Board_Rows):
        pygame.draw.line(screen, color, start_pos=(0, Square_size * i), end_pos=(Width, Square_size * i), width=Line_Width)
        pygame.draw.line(screen, color, (Square_size * i, 0), (Square_size * i, Height), Line_Width)

def draw_figures(color=White):
    for row in range(Board_Rows):
        for col in range(Board_cols):
            if board[row][col] == 1:
                center = (int(col * Square_size + Square_size // 2),
                           int(row * Square_size + Square_size // 2))
                pygame.draw.circle(screen, color, center, Circle_radius, Circle_width)                                      
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                start_pos=(col * Square_size + Square_size // 4,
                                             row * Square_size + Square_size // 4),
                                end_pos=(col * Square_size + 3 * Square_size // 4,
                                         row * Square_size + 3 * Square_size // 4),
                                width=Cross_width)
                pygame.draw.line(screen, color,
                                start_pos=(col * Square_size + 3 * Square_size // 4,
                                            row * Square_size + Square_size // 4),
                                end_pos=(col * Square_size + Square_size // 4,
                                         row * Square_size + 3 * Square_size // 4),
                                width=Cross_width)
def mark_square(row, col, player):
    board[row][col] = player

def avaliable_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(Board_Rows):
        for col in range(Board_cols):
            if check_board[row][col] == 0:
                return True
            return False

def check_win(player, check_board=board):
    for col in range(Board_cols):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True

    for row in range(Board_Rows):
            if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
                return True

            if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
                return True
            
            if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
                            return True
            return False

                #pygame.draw.line(screen, color (col * Square_size + Square_size // 4, row * Square_size + Square_size // 4,)(col * Square_size + 3 * Square_size // 4, row * Square_size + 3 * Square_size // 4))
                #pygame.draw.line(screen, color, start_pos=:(col * Square_size + Square_size // 4, row * Square_size + 3 * Square_size // 4)), end_pos:(col * Square_size + Square_size // 4, row * Square_size + 3 * Square_size // 4)