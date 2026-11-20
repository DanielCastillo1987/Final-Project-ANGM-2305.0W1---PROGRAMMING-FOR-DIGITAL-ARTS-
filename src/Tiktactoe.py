import sys
import pygame
import numpy as np

pygame.init()

White = (255, 255, 255)
Gray = (180, 180, 180)
Red = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Width, Height = screen.get_size() 
pygame.display.set_caption('Tic Tac Toe AI')


#Width = 300
#Height = 300
Board_Rows = 3
Board_cols = 3
Board_Size = min(Width, Height) - 40 
Square_size = Board_Size // Board_cols
Board_Offset_X = (Width - Square_size * Board_cols) // 2
Board_Offset_Y = (Height - Square_size * Board_Rows) // 2
Line_Width = max(3, Square_size // 40)  
Circle_radius = Square_size // 3
Circle_width = max(5, Square_size // 15)
Cross_width = max(5, Square_size // 12) 

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tic Tac Toe AI')

board = np.zeros((Board_Rows, Board_cols))
Move_history = []
Max_Pieces = 6
Max_Depth = 6

Wins_To_Take_Series = 3 
series_wins = {1: 0, 2: 0} 
series_over = False
next_starter = 1    

def draw_lines(color=White):
    for i in range(1, Board_Rows):
          pygame.draw.line(screen, color,
                           start_pos=(Board_Offset_X, Board_Offset_Y + Square_size * i),
                           end_pos=(Board_Offset_X + Square_size * Board_cols, Board_Offset_Y + Square_size * i),
                           width=Line_Width)
          pygame.draw.line(screen, color,
                            start_pos=(Board_Offset_X + Square_size * i, Board_Offset_Y),
                            end_pos=(Board_Offset_X + Square_size * i, Board_Offset_Y + Square_size * Board_Rows),
                            width=Line_Width)

def draw_figures(color=White):
    for row in range(Board_Rows):
        for col in range(Board_cols):
            if board[row][col] == 1:
                center = (int(Board_Offset_X + col * Square_size + Square_size // 2),
                           int(Board_Offset_Y + row * Square_size + Square_size // 2))
                pygame.draw.circle(screen, color, center, Circle_radius, Circle_width)                                      
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                start_pos=(Board_Offset_X + col * Square_size + Square_size // 4,
                                             Board_Offset_Y + row * Square_size + Square_size // 4),
                                end_pos=(Board_Offset_X + col * Square_size + 3 * Square_size // 4,
                                         Board_Offset_Y + row * Square_size + 3 * Square_size // 4),
                                width=Cross_width)
                pygame.draw.line(screen, color,
                                start_pos=(Board_Offset_X + col * Square_size + 3 * Square_size // 4,
                                            Board_Offset_Y + row * Square_size + Square_size // 4),
                                end_pos=(Board_Offset_X + col * Square_size + Square_size // 4,
                                         Board_Offset_Y + row * Square_size + 3 * Square_size // 4),
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

def next_round():
      global Move_history, player, game_over, next_starter
      for row in range(Board_Rows):
           for col in range(Board_cols):
                board[row][col] = 0
      Move_history = []
      player = next_starter
      #player = 1
      game_over = False

def restart_series():
     global series_wins, series_over, next_starter
     series_wins = {1: 0, 2: 0}
     series_over = False
     next_starter = 1 
     next_round()

def draw_scores():
      font = pygame.font.SysFont(None, max(28, Square_size // 3))
      text = f"YOU (O): {series_wins[1]}    AI (X): {series_wins[2]}    First to {Wins_To_Take_Series}"
      surface = font.render(text, True, White)
      rect = surface.get_rect(center=(Width // 2, Board_Offset_Y // 2))
      screen.blit(surface, rect)

      if series_over:
           if series_wins[1] >= Wins_To_Take_Series:
                msg = "You won the set!  Press R to play again"
           else:
                msg = "You lost the set!  Press R to play again" 
           font2 = pygame.font.SysFont(None, max(32, Square_size // 2))
           surface2 = font2.render(msg, True, White)
           rect2 = surface2.get_rect(center=(Width // 2, Height - Board_Offset_Y // 2))
           screen.blit(surface2, rect2)


draw_lines()
player = next_starter
game_over = False

while True:
     screen.fill(Black)
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               sys.exit()

          if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               sys.exit()
          if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

          if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
               mouseX = (event.pos[0] - Board_Offset_X) // Square_size
               mouseY = (event.pos[1] - Board_Offset_Y) // Square_size


               if 0 <= mouseX < Board_cols and 0 <= mouseY < Board_Rows:
                    if avaliable_square(mouseY, mouseX):
                         board[mouseY][mouseX] = player
                         if check_win(player):
                              game_over = True
                              Move_history.append((mouseY, mouseX))
                              series_wins[1] += 1
                              next_starter = 2
                              if series_wins[1] >= Wins_To_Take_Series:
                                   series_over = True  

                         else:
                            board[mouseY][mouseX] = 0
                            place_piece(mouseY, mouseX, player) 
                            player = player % 2 + 1
                            if not game_over:
                                 if best_move():
                                      if check_win(2):
                                           game_over = True
                                           series_wins[2] += 1
                                           next_starter = 1 
                                           if series_wins[2] >= Wins_To_Take_Series:
                                                series_over = True 
                                      else:
                                           player = 1


          if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game_over and not series_over:
                     next_round()

          if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_series()
     if not game_over and not series_over and player == 2:
          if best_move():
                if check_win(2):
                     game_over = True
                     series_wins[2] += 1
                     next_starter = 1
                     if series_wins[2] >= Wins_To_Take_Series:
                          series_over = True
                else:
                     player = 1
            #game_over = False
            #player = 1
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

     draw_scores()
     pygame.display.update()