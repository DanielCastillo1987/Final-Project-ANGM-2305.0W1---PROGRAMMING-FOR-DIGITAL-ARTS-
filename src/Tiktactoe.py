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
