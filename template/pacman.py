import pygame
import sys
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Example")
clock = pygame.time.Clock()

# Screen states
MAIN_MENU = "main_menu"
GAMEPLAY = "gameplay"
PAUSE = "pause"

# Classic Pac-Man map: 1 = wall, 0 = dot, 2 = empty (no dot, no wall)
LEVEL = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,0,1],
    [1,0,1,2,1,0,1,2,0,0,0,2,1,0,1,2,1,0,1],
    [1,0,1,2,1,0,1,2,1,1,1,2,1,0,1,2,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,2,1,0,1,1,1,1,1,1,1,0,1,2,1,0,1],
    [1,0,1,2,1,0,0,0,0,2,0,0,0,0,1,2,1,0,1],
    [1,0,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,0,1],
    [1,0,1,2,0,0,0,0,0,2,0,0,0,0,0,2,1,0,1],
    [1,0,1,2,1,1,1,1,0,1,0,1,1,1,1,2,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROWS = len(LEVEL)
COLS = len(LEVEL[0])

TILE_SIZE = WIDTH // COLS

class Pacman:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.dir = (0, 0)
        self.radius = TILE_SIZE // 2 - 2

    def move(self, dx, dy, walls):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and not walls[ny][nx]:
            self.x, self.y = nx, ny

    def draw(self, surface):
        px = self.x * TILE_SIZE + TILE_SIZE // 2
        py = self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(surface, (255, 255, 0), (px, py), self.radius)

class Ghost:
    def __init__(self, x, y, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.radius = TILE_SIZE // 2 - 4
        self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

    def move(self, walls):
        # Try to move in the current direction, else pick a new random direction
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(directions)
        dx, dy = self.dir
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and not walls[ny][nx]:
            self.x, self.y = nx, ny
        else:
            # Pick a new direction that is not blocked
            for d in directions:
                nx, ny = self.x + d[0], self.y + d[1]
                if 0 <= nx < COLS and 0 <= ny < ROWS and not walls[ny][nx]:
                    self.dir = d
                    self.x, self.y = nx, ny
                    break

    def draw(self, surface):
        px = self.x * TILE_SIZE + TILE_SIZE // 2
        py = self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(surface, self.color, (px, py), self.radius)
        # Eyes
        eye_radius = self.radius // 3
        pygame.draw.circle(surface, (255,255,255), (px-eye_radius, py-eye_radius), eye_radius)
        pygame.draw.circle(surface, (255,255,255), (px+eye_radius, py-eye_radius), eye_radius)
        pygame.draw.circle(surface, (0,0,0), (px-eye_radius, py-eye_radius), eye_radius//2)
        pygame.draw.circle(surface, (0,0,0), (px+eye_radius, py-eye_radius), eye_radius//2)

def get_walls_and_dots():
    walls = [[False]*COLS for _ in range(ROWS)]
    dots = []
    for y in range(ROWS):
        for x in range(COLS):
            if LEVEL[y][x] == 1:
                walls[y][x] = True
            elif LEVEL[y][x] == 0:
                dots.append((x, y))
    return walls, dots

def draw_main_menu(surface, mouse_pos, mouse_clicked):
    surface.fill((30, 30, 60))
    title_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render("Pac-Man", True, (255, 255, 0))
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

def draw_gameplay(surface, mouse_pos, mouse_clicked, game_state):
    surface.fill((0, 0, 0))
    walls, dots, pacman, ghosts, win, lose = (
        game_state["walls"],
        game_state["dots"],
        game_state["pacman"],
        game_state["ghosts"],
        game_state["win"],
        game_state["lose"],
    )

    # Draw walls
    for y in range(ROWS):
        for x in range(COLS):
            if walls[y][x]:
                pygame.draw.rect(surface, (0, 0, 200), (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw dots
    for (x, y) in dots:
        px = x * TILE_SIZE + TILE_SIZE // 2
        py = y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(surface, (255, 255, 255), (px, py), 5)

    # Draw Pac-Man
    pacman.draw(surface)

    # Draw Ghosts
    for ghost in ghosts:
        ghost.draw(surface)

    # Pause button
    button_font = pygame.font.SysFont(None, 40)
    pause_button_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)
    pygame.draw.rect(surface, (100, 100, 100), pause_button_rect)
    pause_text = button_font.render("Pause", True, (255, 255, 255))
    surface.blit(pause_text, (pause_button_rect.centerx - pause_text.get_width()//2, pause_button_rect.centery - pause_text.get_height()//2))
    if mouse_clicked and pause_button_rect.collidepoint(mouse_pos):
        return "pause"

    # Win message
    if win:
        font = pygame.font.SysFont(None, 60)
        text = font.render("You Win!", True, (255, 255, 0))
        surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    # Lose message
    if lose:
        font = pygame.font.SysFont(None, 60)
        text = font.render("Game Over!", True, (255, 0, 0))
        surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    return None

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
    game_state = {}

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
                # Reset game state
                walls, dots = get_walls_and_dots()
                pacman = Pacman()
                # Place ghost in the center of the map
                ghost1 = Ghost(COLS // 2, ROWS // 2, color=(255,0,0))
                ghost2 = Ghost(COLS // 2 - 1, ROWS // 2, color=(0,255,255))
                ghosts = [ghost1, ghost2]
                game_state = {
                    "walls": walls,
                    "dots": dots,
                    "pacman": pacman,
                    "ghosts": ghosts,
                    "win": False,
                    "lose": False,
                }
                current_screen = GAMEPLAY
            elif action == "quit":
                pygame.quit()
                sys.exit()
        elif current_screen == GAMEPLAY:
            pacman = game_state["pacman"]
            walls = game_state["walls"]
            dots = game_state["dots"]
            ghosts = game_state["ghosts"]
            win = game_state["win"]
            lose = game_state["lose"]

            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if not win and not lose:
                if keys[pygame.K_LEFT]:
                    dx, dy = -1, 0
                elif keys[pygame.K_RIGHT]:
                    dx, dy = 1, 0
                elif keys[pygame.K_UP]:
                    dx, dy = 0, -1
                elif keys[pygame.K_DOWN]:
                    dx, dy = 0, 1
                if dx != 0 or dy != 0:
                    pacman.move(dx, dy, walls)

                # Eat dots
                if (pacman.x, pacman.y) in dots:
                    dots.remove((pacman.x, pacman.y))

                # Move ghosts
                for ghost in ghosts:
                    ghost.move(walls)

                # Check collision with ghosts
                for ghost in ghosts:
                    if pacman.x == ghost.x and pacman.y == ghost.y:
                        game_state["lose"] = True

                # Win condition
                if not dots:
                    game_state["win"] = True

            action = draw_gameplay(screen, mouse_pos, mouse_clicked, game_state)
            if action == "pause":
                current_screen = PAUSE
        elif current_screen == PAUSE:
            action = draw_pause(screen, mouse_pos, mouse_clicked)
            if action == "resume":
                current_screen = GAMEPLAY
            elif action == "main_menu":
                current_screen = MAIN_MENU

        pygame.display.flip()
        clock.tick(10)  # Slow down for grid movement

if __name__ == "__main__":
    main()