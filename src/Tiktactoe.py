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
Move_history = []
Max_Pieces = 6
Max_Depth = 6

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

def place_piece(row, col, player):
     mark_square(row, col, player)
     Move_history.append((row, col))
     if len(Move_history) > Max_Pieces:
        old_row, old_col = Move_history.pop(0)
        board[old_row][old_col] = 0

def avaliable_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(Board_Rows):
        for col in range(Board_cols):
            if check_board[row][col] == 0:
                return False
    return True

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

def minimax(minimax_board, depth, is_maximizing, history):
     if check_win(2, minimax_board):
          return float('inf')
     elif check_win(1, minimax_board):
          return float('-inf')

     if depth >= Max_Depth:
          return 0

     if is_maximizing:
          best_score = -1000
          for row in range(Board_Rows):
               for col in range(Board_cols):
                    if minimax_board[row][col] == 0:
                         new_board = minimax_board.copy()
                         new_board[row][col] = 2
                         new_history = history + [(row, col)]
                         if len(new_history) > Max_Pieces:
                              old_r, old_c = new_history.pop(0)
                              new_board[old_r][old_c] = 0
                         score = minimax(new_board, depth + 1, False, new_history)
                         best_score = max(score, best_score)
          return best_score
     else:
          best_score = 1000
          for row in range(Board_Rows):
               for col in range(Board_cols):
                    if minimax_board[row][col] == 0:
                         new_board = minimax_board.copy()
                         new_board[row][col] = 1
                         new_history = history + [(row, col)]
                         if len(new_history) > Max_Pieces:
                              old_r, old_c = new_history.pop(0)
                              new_board[old_r][old_c] = 0 
                         score = minimax(new_board, depth + 1, True, new_history)
                         best_score = min(score, best_score)
          return best_score

def best_move():
     best_score = -1000
     move = (-1, -1)
     for row in range(Board_Rows):
        for col in range(Board_cols):
             if board[row][col] == 0:
                  new_board = board.copy() 
                  new_board[row][col] = 2
                  new_history = Move_history + [(row, col)]
                  if len(new_history) > Max_Pieces:
                       old_r, old_c = new_history.pop(0)
                       new_board[old_r][old_c] = 0  
                  score = minimax(new_board, 0, False, new_history)
                  if score > best_score:
                       best_score = score
                       move = (row, col)

     if move != (-1, -1):
            place_piece(move[0], move[1], 2)
            return True
     return False  
                            

def restart_game():
     global Move_history
     screen.fill(Black)
     draw_lines()
     for row in range(Board_Rows):
          for col in range(Board_cols):
               board[row][col] = 0
     Move_history = []

draw_lines()
player = 1
game_over = False

while True:
     screen.fill(Black)
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               sys.exit()

          if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
               mouseX = event.pos[0] // Square_size
               mouseY = event.pos[1] // Square_size

               if avaliable_square(mouseY, mouseX):
                    board[mouseY][mouseX] = player
                    if check_win(player):
                       game_over = True
                       Move_history.append((mouseY, mouseX))

                    else:
                         board[mouseY][mouseX] = 0
                         place_piece(mouseY, mouseX, player) 
                         
                         player = player % 2 + 1
                         if not game_over:
                              if best_move():
                                   if check_win(2):
                                        game_over = True
                                   else:
                                        player = 1

                    if not game_over:
                         if is_board_full():
                              game_over = True
          if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()
            game_over = False
            player = 1
     if not game_over:
          draw_lines()
          draw_figures()
     else:
          if check_win(1):
               draw_figures(Green)
               draw_lines(Green)

          elif check_win(2):
            draw_figures(Red)
            draw_lines(Red)
          else: 
            draw_figures(Gray)
            draw_lines(Gray)
     
     pygame.display.update()