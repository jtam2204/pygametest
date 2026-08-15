import pygame
import sys
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

# Screen states
MAIN_MENU = "main_menu"
GAMEPLAY = "gameplay"
PAUSE = "pause"
MODE_SELECT = "mode_select"

# Game constants
GRID_SIZE = 3
CELL_SIZE = 120
GRID_ORIGIN = (WIDTH // 2 - (CELL_SIZE * GRID_SIZE) // 2, HEIGHT // 2 - (CELL_SIZE * GRID_SIZE) // 2)

def draw_main_menu(surface, mouse_pos, mouse_clicked):
    surface.fill((30, 30, 60))
    title_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render("Tic-Tac-Toe", True, (255, 255, 255))
    surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 120))

    # Draw Play button
    play_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
    pygame.draw.rect(surface, (70, 130, 180), play_button_rect)
    play_text = button_font.render("Play", True, (255, 255, 255))
    surface.blit(play_text, (play_button_rect.centerx - play_text.get_width()//2, play_button_rect.centery - play_text.get_height()//2))

    # Draw Quit button
    quit_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)
    pygame.draw.rect(surface, (180, 70, 70), quit_button_rect)
    quit_text = button_font.render("Quit", True, (255, 255, 255))
    surface.blit(quit_text, (quit_button_rect.centerx - quit_text.get_width()//2, quit_button_rect.centery - quit_text.get_height()//2))

    if mouse_clicked:
        if play_button_rect.collidepoint(mouse_pos):
            return "play"
        elif quit_button_rect.collidepoint(mouse_pos):
            return "quit"
    return None

def draw_mode_select(surface, mouse_pos, mouse_clicked):
    surface.fill((30, 30, 60))
    title_font = pygame.font.SysFont(None, 50)
    button_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render("Select Game Mode", True, (255, 255, 255))
    surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 120))

    # Player vs Player
    pvp_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 40, 300, 50)
    pygame.draw.rect(surface, (70, 130, 180), pvp_rect)
    pvp_text = button_font.render("Player vs Player", True, (255, 255, 255))
    surface.blit(pvp_text, (pvp_rect.centerx - pvp_text.get_width()//2, pvp_rect.centery - pvp_text.get_height()//2))

    # Player vs Computer
    pvc_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 30, 300, 50)
    pygame.draw.rect(surface, (180, 130, 70), pvc_rect)
    pvc_text = button_font.render("Player vs Computer", True, (255, 255, 255))
    surface.blit(pvc_text, (pvc_rect.centerx - pvc_text.get_width()//2, pvc_rect.centery - pvc_text.get_height()//2))

    if mouse_clicked:
        if pvp_rect.collidepoint(mouse_pos):
            return "pvp"
        elif pvc_rect.collidepoint(mouse_pos):
            return "pvc"
    return None

def check_winner(board):
    # Rows, columns, diagonals
    for i in range(GRID_SIZE):
        if board[i][0] != "" and all(board[i][j] == board[i][0] for j in range(GRID_SIZE)):
            return board[i][0]
        if board[0][i] != "" and all(board[j][i] == board[0][i] for j in range(GRID_SIZE)):
            return board[0][i]
    if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(GRID_SIZE)):
        return board[0][0]
    if board[0][GRID_SIZE-1] != "" and all(board[i][GRID_SIZE-1-i] == board[0][GRID_SIZE-1] for i in range(GRID_SIZE)):
        return board[0][GRID_SIZE-1]
    return None

def board_full(board):
    return all(board[i][j] != "" for i in range(GRID_SIZE) for j in range(GRID_SIZE))

def computer_move(board):
    # Improved AI: win, block, or pick random
    def can_win(b, mark):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if b[r][c] == "":
                    b[r][c] = mark
                    if check_winner(b) == mark:
                        b[r][c] = ""
                        return (r, c)
                    b[r][c] = ""
        return None

    # Try to win
    move = can_win(board, "O")
    if move:
        board[move[0]][move[1]] = "O"
        return board

    # Try to block player
    move = can_win(board, "X")
    if move:
        board[move[0]][move[1]] = "O"
        return board

    # Otherwise random
    empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == ""]
    if empty:
        row, col = random.choice(empty)
        board[row][col] = "O"
    return board

def draw_gameplay(surface, mouse_pos, mouse_clicked, board, current_player, winner, draw, vs_computer):
    surface.fill((60, 30, 30))
    font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 40)

    # Draw grid
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(surface, (255, 255, 255),
                         (GRID_ORIGIN[0], GRID_ORIGIN[1] + i * CELL_SIZE),
                         (GRID_ORIGIN[0] + GRID_SIZE * CELL_SIZE, GRID_ORIGIN[1] + i * CELL_SIZE), 3)
        pygame.draw.line(surface, (255, 255, 255),
                         (GRID_ORIGIN[0] + i * CELL_SIZE, GRID_ORIGIN[1]),
                         (GRID_ORIGIN[0] + i * CELL_SIZE, GRID_ORIGIN[1] + GRID_SIZE * CELL_SIZE), 3)

    # Draw X and O
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            mark = board[row][col]
            if mark:
                mark_text = font.render(mark, True, (255, 255, 255))
                x = GRID_ORIGIN[0] + col * CELL_SIZE + CELL_SIZE // 2 - mark_text.get_width() // 2
                y = GRID_ORIGIN[1] + row * CELL_SIZE + CELL_SIZE // 2 - mark_text.get_height() // 2
                surface.blit(mark_text, (x, y))

    # Draw status
    if winner:
        status = f"{winner} wins!"
    elif draw:
        status = "Draw!"
    else:
        if vs_computer and current_player == "O":
            status = "Computer's turn"
        else:
            status = f"{current_player}'s turn"
    status_text = small_font.render(status, True, (255, 255, 0))
    surface.blit(status_text, (WIDTH//2 - status_text.get_width()//2, GRID_ORIGIN[1] - 50))

    # Simple pause button (top right)
    pause_button_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)
    pygame.draw.rect(surface, (100, 100, 100), pause_button_rect)
    pause_text = small_font.render("Pause", True, (255, 255, 255))
    surface.blit(pause_text, (pause_button_rect.centerx - pause_text.get_width()//2, pause_button_rect.centery - pause_text.get_height()//2))

    # Restart button if game over
    restart_button_rect = None
    if winner or draw:
        restart_button_rect = pygame.Rect(WIDTH//2 - 100, GRID_ORIGIN[1] + GRID_SIZE * CELL_SIZE + 20, 200, 50)
        pygame.draw.rect(surface, (70, 130, 180), restart_button_rect)
        restart_text = small_font.render("Restart", True, (255, 255, 255))
        surface.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width()//2, restart_button_rect.centery - restart_text.get_height()//2))

    # Handle clicks
    if mouse_clicked:
        if pause_button_rect.collidepoint(mouse_pos):
            return "pause", None, None
        if winner or draw:
            if restart_button_rect and restart_button_rect.collidepoint(mouse_pos):
                return "restart", None, None
        if not winner and not draw:
            # Only allow player to move if it's their turn
            if not (vs_computer and current_player == "O"):
                mx, my = mouse_pos
                gx, gy = mx - GRID_ORIGIN[0], my - GRID_ORIGIN[1]
                if 0 <= gx < CELL_SIZE * GRID_SIZE and 0 <= gy < CELL_SIZE * GRID_SIZE:
                    col = gx // CELL_SIZE
                    row = gy // CELL_SIZE
                    if board[row][col] == "":
                        board[row][col] = current_player
                        next_player = "O" if current_player == "X" else "X"
                        return None, board, next_player
    return None, None, None

def draw_pause(surface, mouse_pos, mouse_clicked):
    surface.fill((30, 60, 30))
    pause_title = pygame.font.SysFont(None, 60).render("Paused", True, (255, 255, 255))
    surface.blit(pause_title, (WIDTH//2 - pause_title.get_width()//2, HEIGHT//2 - 120))

    button_font = pygame.font.SysFont(None, 40)
    resume_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
    back_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)

    # Draw Resume button
    pygame.draw.rect(surface, (70, 180, 100), resume_button_rect)
    resume_text = button_font.render("Resume", True, (255, 255, 255))
    surface.blit(resume_text, (resume_button_rect.centerx - resume_text.get_width()//2, resume_button_rect.centery - resume_text.get_height()//2))

    # Draw Back to Menu button
    pygame.draw.rect(surface, (180, 180, 70), back_button_rect)
    back_text = button_font.render("Main Menu", True, (255, 255, 255))
    surface.blit(back_text, (back_button_rect.centerx - back_text.get_width()//2, back_button_rect.centery - back_text.get_height()//2))

    if mouse_clicked:
        if resume_button_rect.collidepoint(mouse_pos):
            return "resume"
        elif back_button_rect.collidepoint(mouse_pos):
            return "main_menu"
    return None

def main():
    current_screen = MAIN_MENU
    board = [[""] * GRID_SIZE for _ in range(GRID_SIZE)]
    current_player = "X"
    winner = None
    draw = False
    vs_computer = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if current_screen == MAIN_MENU:
            action = draw_main_menu(screen, mouse_pos, mouse_clicked)
            if action == "play":
                current_screen = MODE_SELECT
            elif action == "quit":
                pygame.quit()
                sys.exit()
        elif current_screen == MODE_SELECT:
            action = draw_mode_select(screen, mouse_pos, mouse_clicked)
            if action == "pvp":
                board = [[""] * GRID_SIZE for _ in range(GRID_SIZE)]
                current_player = "X"
                winner = None
                draw = False
                vs_computer = False
                current_screen = GAMEPLAY
            elif action == "pvc":
                board = [[""] * GRID_SIZE for _ in range(GRID_SIZE)]
                current_player = "X"
                winner = None
                draw = False
                vs_computer = True
                current_screen = GAMEPLAY
        elif current_screen == GAMEPLAY:
            winner = check_winner(board)
            draw = board_full(board) and not winner

            # Computer move if needed
            if vs_computer and current_player == "O" and not winner and not draw:
                pygame.time.wait(500)  # Small delay for realism
                board = computer_move(board)
                current_player = "X"
                winner = check_winner(board)
                draw = board_full(board) and not winner

            action, new_board, new_player = draw_gameplay(screen, mouse_pos, mouse_clicked, board, current_player, winner, draw, vs_computer)
            if action == "pause":
                current_screen = PAUSE
            elif action == "restart":
                board = [[""] * GRID_SIZE for _ in range(GRID_SIZE)]
                current_player = "X"
                winner = None
                draw = False
            elif new_board is not None and new_player is not None:
                board = new_board
                current_player = new_player
        elif current_screen == PAUSE:
            action = draw_pause(screen, mouse_pos, mouse_clicked)
            if action == "resume":
                current_screen = GAMEPLAY
            elif action == "main_menu":
                current_screen = MAIN_MENU

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()