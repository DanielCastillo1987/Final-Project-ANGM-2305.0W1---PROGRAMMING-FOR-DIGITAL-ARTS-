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
           
      
                #pygame.draw.line(screen, color (col * Square_size + Square_size // 4, row * Square_size + Square_size // 4,)(col * Square_size + 3 * Square_size // 4, row * Square_size + 3 * Square_size // 4))
                #pygame.draw.line(screen, color, start_pos=:(col * Square_size + Square_size // 4, row * Square_size + 3 * Square_size // 4)), end_pos:(col * Square_size + Square_size // 4, row * Square_size + 3 * Square_size // 4)