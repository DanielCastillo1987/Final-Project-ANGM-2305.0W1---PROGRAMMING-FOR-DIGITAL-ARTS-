import sys
import pygame
import numpy as np
import random   

pygame.init()

White = (255, 255, 255)
Gray = (180, 180, 180)
Red = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)
Yellow = (255, 255, 0)
Blue = (0, 120, 255)  

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Width, Height = screen.get_size() 
pygame.display.set_caption('Tic Tac Toe AI')

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

state = "menu" 
player_class = 1
ai_class = 1
CLASS_NAMES = {1: "Knight", 2: "Thief", 3: "Wizard", 4: "John Tiktactoe"}
CLASS_DESCRIPTIONS = {1: "Knight: You can protect a move meant to disappear for one turn.'Your Stars Were Bad'", 
                      2: "Thief: Swaps one of your tiles with your opponent. 'Take Your Heart.'",
                      3: "Wizard: Makes a tile unplayable for the turn. 'We Love Casting Spells.'",
                      4: "John Tiktactoe: No power just skill. 'Gimme A Cheese With Nothing.'", 
}

player_ability_used = False
ai_ability_used = False
player_turns = 0
ai_turns = 0
protected_cell = None
protected_turns_left = 0 
blocked_cell = None
blocked_turns_left = 0 
blocked_by = None
ability_target = None
thief_own_cell = None
ability_message = ""
ability_message_timer = 0



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

def draw_ability_highlights():   
     if protected_cell is not None:
          r, c = protected_cell
          pygame.draw.rect(screen, Blue,(Board_Offset_X + c * Square_size + 3,Board_Offset_Y + r * Square_size + 3, Square_size - 6, Square_size - 6), 4)
     if blocked_cell is not None:
           r, c = blocked_cell
           pygame.draw.rect(screen, Yellow,
                           (Board_Offset_X + c * Square_size + 3,
                            Board_Offset_Y + r * Square_size + 3,
                            Square_size - 6, Square_size - 6), 4)
                
def mark_square(row, col, player):
    board[row][col] = player

def place_piece(row, col, player):
     global protected_cell 
     mark_square(row, col, player)
     Move_history.append((row, col))
     if len(Move_history) > Max_Pieces:
        old_row, old_col = Move_history.pop(0)
        if protected_cell == (old_row, old_col):
              protected_cell = None
              Move_history.insert(0, (old_row, old_col))
        else:
           board[old_row][old_col] = 0

def avaliable_square(row, col):
    if (row, col) == blocked_cell:
         return False
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
            if avaliable_square(row, col):  
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
            tick_ability_effects() 

            return True
     return False  

def set_ability_message(msg):
     global ability_message, ability_message_timer
     ability_message = msg
     ability_message_timer = 120

def human_ability_ready():
     return (not player_ability_used) and (player_turns >= 2) and player_class != 4

def ai_ability_ready():
     return (not ai_ability_used) and (ai_turns >= 2) and ai_class != 4

def tick_ability_effects():
     global protected_cell, protected_turns_left
     global blocked_cell, blocked_turns_left, blocked_by

     if protected_cell is not None and protected_turns_left > 0:
           protected_turns_left -= 1
           if protected_turns_left == 0:
                protected_cell = None
     if blocked_cell is not None and blocked_turns_left > 0:
          blocked_turns_left -= 1
          if blocked_turns_left == 0:
               blocked_cell = None
               blocked_by = None


def clear_expired_blocks():
     pass

def apply_ai_ability():
     global ai_ability_used, protected_cell, blocked_cell, blocked_by, protected_turns_left, blocked_turns_left
     if not ai_ability_ready():
          return
     if ai_class == 1:
          ai_ability_used = True
          for cell in Move_history:
               if board[cell[0]][cell[1]] == 2:
                    protected_cell = cell
                    protected_turns_left = 2 
                    set_ability_message("AI Knight protected a piece!")
                    return
          protected_cell = None
     elif ai_class == 2:
          ai_ability_used = True
          ai_cells = [(r, c) for r in range(Board_Rows) for c in range(Board_cols) if board[r][c] == 2]
          human_cells = [(r, c) for r in range(Board_Rows) for c in range(Board_cols) if board[r][c] == 1]
          if ai_cells and human_cells:
               a = random.choice(ai_cells)
               h = random.choice(human_cells)
               board[a[0]][a[1]] = 1
               board[h[0]][h[1]] = 2
               set_ability_message("AI Thief swapped a tile!")
     elif ai_class == 3:
          ai_ability_used = True
          empties = [(r, c) for r in range(Board_Rows) for c in range(Board_cols) if board[r][c] == 0]
          if empties:
               blocked_cell = random.choice(empties)
               blocked_by = 2
               blocked_turns_left = 2 
               set_ability_message("AI Wizard blocked a tile!")

def restart_game():
     global Move_history, player, game_over, next_starter
     global player_ability_used, ai_ability_used  
     global player_turns, ai_turns 
     global protected_cell, blocked_cell, blocked_by 
     global protected_turns_left, blocked_turns_left     
     global protected_cell, blocked_cell 
     global ability_target, thief_own_cell 
     screen.fill(Black)
     draw_lines()
     for row in range(Board_Rows):
          for col in range(Board_cols):
               board[row][col] = 0
     Move_history = []
     player = next_starter
     game_over = False
     player_ability_used = False
     ai_ability_used = False
     player_turns = 0
     ai_turns = 0
     protected_cell = None
     protected_turns_left = 0   
     blocked_cell = None
     blocked_turns_left = 0 
     blocked_by = None     
     ability_target = None
     thief_own_cell = None



def next_round():
      global Move_history, player, game_over, next_starter
      global protected_cell, protected_turns_left
      global blocked_cell, blocked_turns_left, blocked_by
      for row in range(Board_Rows):
           for col in range(Board_cols):
                board[row][col] = 0
      Move_history = []
      player = next_starter
      game_over = False
      protected_cell = None
      protected_turns_left = 0
      blocked_cell = None
      blocked_turns_left = 0
      blocked_by = None

def restart_series():
     global series_wins, series_over, next_starter
     series_wins = {1: 0, 2: 0}
     series_over = False
     next_starter = 1 
     next_round()

def draw_scores():
      text = f"YOU (O): {series_wins[1]}    AI (X): {series_wins[2]}    First to {Wins_To_Take_Series}"
      text += f"    YOU: {CLASS_NAMES[player_class]}  vs  AI: {CLASS_NAMES[ai_class]}"
      font_size = max(28, Square_size // 3)
      font = pygame.font.SysFont(None, font_size) 
      surface = font.render(text, True, White)

      while surface.get_width() > Width * 0.9 and font_size > 16:
            font_size -= 2 
            font = pygame.font.SysFont(None, font_size)
            surface = font.render(text, True, White)

      rect = surface.get_rect(center=(Width // 2, Board_Offset_Y // 2 + 70))
      screen.blit(surface, rect)

      if series_over:
           if series_wins[1] >= Wins_To_Take_Series:
                msg = "You won the set!  Press R to play again"
           else:
                msg = "You lost the set!  Press R to play again" 

           font_size2 = max(32, Square_size // 2)

           font2 = pygame.font.SysFont(None, font_size2)
           surface2 = font2.render(msg, True, White)
           while surface2.get_width() > Width * 0.9 and font_size2 > 16:
                font_size2 -= 2
                font2 = pygame.font.SysFont(None, font_size2)
                surface2 = font2.render(msg, True, White)
           
           rect2 = surface2.get_rect(center=(Width // 2, Height - Board_Offset_Y // 2 - 60))
           screen.blit(surface2, rect2)

def draw_menu():
      title_size = max(48, Square_size // 2)
      font = pygame.font.SysFont(None, title_size)
      title = font.render("TIC TAC TOE", True, White)
      screen.blit(title, title.get_rect(center=(Width // 2, Height // 2 - Square_size // 2)))
      prompt_size = max(28, Square_size // 4)
      font2 = pygame.font.SysFont(None, prompt_size)
      prompt = font2.render("Press SPACE to choose a class", True, White)
      screen.blit(prompt, prompt.get_rect(center=(Width // 2, Height // 2 + Square_size // 2)))




def draw_class_select():
     title_size = max(40, Square_size // 3)
     font = pygame.font.SysFont(None, title_size)
     title = font.render("CHOOSE YOUR CLASS", True, White)
     screen.blit(title, title.get_rect(center=(Width // 2, Height // 2 - Square_size)))

     option_size = max(28, Square_size // 5)
     font2 = pygame.font.SysFont(None, option_size)
     labels = ["1. Knight", "2. Theif", "3. Wizard", "4. John Tiktactoe",]

     start_y = Height // 2
     for i, label in enumerate(labels):
          color = Green if (i + 1) == player_class else White
          surface = font2.render(label, True, color)
          screen.blit(surface, surface.get_rect(center=(Width // 2, start_y + i * (option_size + 16))))
     hint = font2.render("Press 1-4 to choose, ENTER to confirm", True, Gray)
     screen.blit(hint, hint.get_rect(center=(Width // 2, Height - option_size * 2)))

     desc_size = max(24, Square_size // 6) 
     font3 = pygame.font.SysFont(None, desc_size)
     desc = CLASS_DESCRIPTIONS[player_class]
     desc_surface = font3.render(desc, True, Gray)
     while desc_surface.get_width() > Width * 0.9 and desc_size > 14:
          desc_size -= 2
          font3 = pygame.font.SysFont(None, desc_size)
          desc_surface = font3.render(desc, True, Gray)
     screen.blit(desc_surface, desc_surface.get_rect(center=(Width // 2, Height - desc_size * 3.5 - 10))) 


def draw_ability_hud():
     font_size = max(22, Square_size // 7)
     font = pygame.font.SysFont(None, font_size)
     if ability_message:
          color = Yellow
          text = ability_message
     elif player_class == 4:
          text = "No ability — just skill."
          color = Gray
     elif player_ability_used:
          text = "Ability used."
          color = Gray
     elif player_turns >= 2 and player == 1 and state == "playing":
          text = "Press E to use your ability."
          color = Green
     elif ability_target in ("thief_own", "thief_target"):
          text = "Click your own tile to swap."
          color = Yellow
     elif ability_target == "wizard":
          text = "Click an empty tile to block."
          color = Yellow
     elif ability_target == "knight":
          text = "Click one of your tiles to protect."
          color = Yellow
     else:
          text = ""
          color = Gray
     if text:
          surf = font.render(text, True, color)
          screen.blit(surf, surf.get_rect(center=(Width // 2, Height - Square_size // 2 - 40)))


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

          if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if state == "menu":
                     state = "class_select"
                elif state == "playing" and game_over and not series_over:
                     next_round()

          if event.type == pygame.KEYDOWN and state == "class_select":
               if event.key in (pygame.K_1, pygame.K_KP1): player_class = 1
               if event.key in (pygame.K_2, pygame.K_KP2): player_class = 2
               if event.key in (pygame.K_3, pygame.K_KP3): player_class = 3
               if event.key in (pygame.K_4, pygame.K_KP4): player_class = 4
               if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    ai_class = random.randint(1, 4)
                    restart_series()
                    state = "playing"

          if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
               if state == "playing" and not game_over and player == 1 and human_ability_ready():
                    if player_class == 1:
                         ability_target = "knight"
                         set_ability_message("Knight: choose a tile to protect.")
                    elif player_class == 2:
                         ability_target = "thief_own"
                         set_ability_message("Thief: choose your own tile.")
                    elif player_class == 3:
                         ability_target = "wizard"
                         set_ability_message("Wizard: choose a tile to block.")

          if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1 and state == "playing":
               mouseX = (event.pos[0] - Board_Offset_X) // Square_size
               mouseY = (event.pos[1] - Board_Offset_Y) // Square_size
               if 0 <= mouseX < Board_cols and 0 <= mouseY < Board_Rows:

                    if ability_target is not None:
                         if ability_target == "knight":
                              if board[mouseY][mouseX] == 1:
                                   protected_cell = (mouseY, mouseX)
                                   protected_turns_left = 2 
                                   player_ability_used = True
                                   ability_target = None
                                   set_ability_message("Knight: piece protected for the turn.")
                         elif ability_target == "thief_own":
                              if board[mouseY][mouseX] == 1:
                                   thief_own_cell = (mouseY, mouseX)
                                   ability_target = "thief_target"
                                   set_ability_message("Thief: choose an opponent tile to swap.")
                         elif ability_target == "thief_target":
                              if board[mouseY][mouseX] == 2 and thief_own_cell is not None:
                                   o_r, o_c = thief_own_cell
                                   board[o_r][o_c], board[mouseY][mouseX] = 2, 1
                                   player_ability_used = True
                                   ability_target = None
                                   thief_own_cell = None
                                   set_ability_message("Thief: tiles swapped.")
                         elif ability_target == "wizard":
                              if board[mouseY][mouseX] == 0:
                                   blocked_cell = (mouseY, mouseX)
                                   blocked_by = 1
                                   blocked_turns_left = 2
                                   
                                   player_ability_used = True
                                   ability_target = None
                                   set_ability_message("Wizard: cell blocked for one turn.")
                         continue


               if 0 <= mouseX < Board_cols and 0 <= mouseY < Board_Rows:
                    if avaliable_square(mouseY, mouseX):
                         #if blocked_by == 2: 
                              #blocked_cell = None
                              #blocked_by = None
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
                            tick_ability_effects()
                            player_turns += 1 
                            player = player % 2 + 1
                            if not game_over:
                                 if ai_turns >= 2 and not ai_ability_used:
                                      apply_ai_ability()

                                 if best_move():
                                      ai_turns += 1 
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
     if state == "playing" and not game_over and not series_over and player == 2:
          if ai_turns >= 2 and not ai_ability_used:
               apply_ai_ability()
          #if blocked_by == 1:
               #blocked_cell = None
               #blocked_by = None
          if best_move():
                ai_turns += 1  
                if check_win(2):
                     game_over = True
                     series_wins[2] += 1
                     next_starter = 1
                     if series_wins[2] >= Wins_To_Take_Series:
                          series_over = True
                else:
                     player = 1
     if state == "menu":
          draw_menu()
     elif state == "class_select":
          draw_class_select()
     else:

          if not game_over:
               draw_lines()
               draw_figures()
               draw_ability_highlights()   
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
     if state == "playing":
          draw_ability_hud()
     pygame.display.update()