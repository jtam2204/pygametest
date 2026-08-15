import pygame
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRPG Main Loop Example")
clock = pygame.time.Clock()
direction = 0  # Initialize direction variable

# Screen states
MAIN_MENU = "main_menu"
GAMEPLAY = "gameplay"
PAUSE = "pause"

def draw_main_menu(surface, mouse_pos, mouse_clicked):
    surface.fill((30, 30, 60))
    title_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render("Main Menu", True, (255, 255, 255))
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

def draw_gameplay(surface, mouse_pos, mouse_clicked):
    global direction
    up = 90
    down = 270
    left = 180
    right = 0

    surface.fill((60, 30, 30))
    font = pygame.font.SysFont(None, 60)
    text = font.render("Gameplay", True, (255, 255, 255))
    #surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.draw.arc(surface, (255, 255, 255), (WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100), (direction - 45) * (3.14/180), (direction + 45) * (3.14/180))

    # Simple pause button (top right)
    button_font = pygame.font.SysFont(None, 40)
    pause_button_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)
    pygame.draw.rect(surface, (100, 100, 100), pause_button_rect)
    pause_text = button_font.render("Pause", True, (255, 255, 255))
    surface.blit(pause_text, (pause_button_rect.centerx - pause_text.get_width()//2, pause_button_rect.centery - pause_text.get_height()//2))
    if mouse_clicked and pause_button_rect.collidepoint(mouse_pos) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
        return "pause"
    if pygame.key.get_pressed()[pygame.K_UP]:   
        direction = up
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        direction = down
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        direction = left
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        direction = right
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
                current_screen = GAMEPLAY
            elif action == "quit":
                pygame.quit()
                sys.exit()
        elif current_screen == GAMEPLAY:
            action = draw_gameplay(screen, mouse_pos, mouse_clicked)
            if action == "pause":
                current_screen = PAUSE
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