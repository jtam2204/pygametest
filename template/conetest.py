import math
import random
import pygame
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRPG Main Loop Example")
clock = pygame.time.Clock()
displayboxheight = 50
displaylist = [((1,0),'w', 0),((0,1),'a' ,0),((1,1),'s', 0),((2,1),'d', 0),((0,2),'Shift', 0),((1,2),'Space', 0)]
padding = 10
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
grey = (128, 128, 128)
playercolor = green
direction = 0  # Initialize direction variable
playerradius = 15
playerviewradius = 90
playerviewangle = 120
x = WIDTH//2
y = HEIGHT//2
number_of_targets = 5
targetradius = 20
targetviewradius = 70
targetviewangle = 90
target_rotation_speed = 0.5  # degrees per frame
target_speed = 1.5  # speed at which targets move toward player when they see the player
# Screen states
MAIN_MENU = "main_menu"
GAMEPLAY = "gameplay"
PAUSE = "pause"
GAMEOVER = "gameover"



def initialize_gameplay():
    global x, y, playerspeed, targetlist, score
    score = 0
    x = WIDTH // 2
    y = HEIGHT // 2
    playerspeed = 2
    targetlist = []

    min_target_spacing = targetradius * 2 + 10
    player_safe_distance = playerviewradius + targetradius + 15

    for _ in range(number_of_targets):
        placed = False
        for _ in range(500):
            target_x = random.randint(targetradius, WIDTH - targetradius)
            target_y = random.randint(targetradius, HEIGHT - targetradius)
            candidate = (target_x, target_y)

            if math.hypot(target_x - x, target_y - y) < player_safe_distance:
                continue

            if any(math.hypot(target_x - existing_x, target_y - existing_y) < min_target_spacing
                   for (existing_x, existing_y), _, _ in targetlist):
                continue

            target_value = 1
            target_viewing_direction = random.randint(0, 359)
            targetlist.append((candidate, target_value, target_viewing_direction))
            placed = True
            break

        if not placed:
            # Fallback: spread targets around the edge of the screen if random placement fails.
            angle = (len(targetlist) / max(1, number_of_targets)) * (2 * math.pi)
            distance = min(WIDTH, HEIGHT) * 0.45
            target_x = int(WIDTH // 2 + math.cos(angle) * distance)
            target_y = int(HEIGHT // 2 + math.sin(angle) * distance)
            target_x = max(targetradius, min(target_x, WIDTH - targetradius))
            target_y = max(targetradius, min(target_y, HEIGHT - targetradius))
            targetlist.append(((target_x, target_y), 1, random.randint(0, 359)))

def draw_main_menu(surface, mouse_pos, mouse_clicked):
    surface.fill((30, 30, 60))
    title_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render("Stealthy Cone Chase", True, (255, 255, 255))
    surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 120))

    # Draw Play button
    play_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 50)
    pygame.draw.rect(surface, (70, 130, 180), play_button_rect)
    play_text = button_font.render("New Game", True, (255, 255, 255))
    surface.blit(play_text, (play_button_rect.centerx - play_text.get_width()//2, play_button_rect.centery - play_text.get_height()//2))

    # Draw Quit button
    quit_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)
    pygame.draw.rect(surface, (180, 70, 70), quit_button_rect)
    quit_text = button_font.render("Quit", True, (255, 255, 255))
    surface.blit(quit_text, (quit_button_rect.centerx - quit_text.get_width()//2, quit_button_rect.centery - quit_text.get_height()//2))

    if mouse_clicked:
        if play_button_rect.collidepoint(mouse_pos):
            initialize_gameplay()  # Reset gameplay state when starting a new game
            return "play"
        elif quit_button_rect.collidepoint(mouse_pos):
            return "quit"
    return None

def draw_gameplay(surface, mouse_pos, mouse_clicked):
    global direction, x, y, playerspeed, playercolor, score
    chasing = False
    up = 90
    upright = 45
    upleft = 135
    down = 270
    downright = 315
    downleft = 225
    left = 180
    right = 0
    normalizedspeed = playerspeed * 0.7 # Adjust speed for diagonal movement
    vision_rect = pygame.Rect(x - playerviewradius, y - playerviewradius, playerviewradius * 2, playerviewradius * 2)
    #if pygame.key.get_pressed():
    #    print(f"Player position: ({x}, {y}), Direction: {direction}, Speed: {playerspeed}, Normalized Speed: {normalizedspeed}")

    surface.fill((60, 30, 30))
    font = pygame.font.SysFont(None, 60)

    # Simple pause button (top right)
    button_font = pygame.font.SysFont(None, 40) 
    pause_button_rect = pygame.Rect(WIDTH - 120, 20, 100, 40)
    pygame.draw.rect(surface, (100, 100, 100), pause_button_rect)
    pause_text = button_font.render("Pause", True, (255, 255, 255))
    surface.blit(pause_text, (pause_button_rect.centerx - pause_text.get_width()//2, pause_button_rect.centery - pause_text.get_height()//2))
    if mouse_clicked and pause_button_rect.collidepoint(mouse_pos) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
        return "pause"

    # keymaps
    for rectxy, dtext, hovered in displaylist:
        rectx, recty = rectxy
        text = font.render(dtext, True, (255, 255, 255))
        if hovered:
            pygame.draw.rect(surface, (100, 100, 100), (rectx * (displayboxheight + padding)+padding, recty * (displayboxheight + padding)+padding, max(text.get_width()+padding, displayboxheight), displayboxheight), 5, border_radius=5)
        else:
            pygame.draw.rect(surface, (50, 50, 50), (rectx * (displayboxheight + padding)+padding, recty * (displayboxheight + padding)+padding, max(text.get_width()+padding, displayboxheight), displayboxheight), 5, border_radius=5)
        if text.get_width() > displayboxheight:
            surface.blit(text, (rectx * (displayboxheight + padding) + (max(text.get_width()+padding, displayboxheight) - text.get_width()) // 2, recty * (displayboxheight + padding) + (displayboxheight - text.get_height()) // 2))
        else:
            surface.blit(text, (rectx * (displayboxheight + padding)+padding + (displayboxheight - text.get_width()) // 2, recty * (displayboxheight + padding)+padding + (displayboxheight - text.get_height()) // 2))

    def player_in_view(target_pos, target_viewing_direction):
            target_x, target_y = target_pos
            dx = x - target_x
            dy = y - target_y
            distance = math.hypot(dx, dy)
    
            if distance > targetviewradius + playerradius:
                return False
    
            player_angle = math.degrees(math.atan2(dy, dx)) 
            if player_angle < 0:
                player_angle += 360
            #print(f"Player angle: {player_angle}, target direction: {target_viewing_direction}")
    
            relative_angle = 360 - player_angle
            return target_viewing_direction - targetviewangle / 2 <= relative_angle <= target_viewing_direction + targetviewangle / 2

    def target_in_view(target_pos):
        target_x, target_y = target_pos
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)

        if distance > playerviewradius + targetradius:
            return False

        target_angle = math.degrees(math.atan2(dy, dx))
        if target_angle < 0:
            target_angle += 360
        #print(f"Target angle: {target_angle}, Player direction: {direction}")

        relative_angle = 360 - target_angle
        return direction - playerviewangle / 2 <= relative_angle <= direction + playerviewangle / 2

    # draw vision cone
    pygame.draw.arc(surface, (255, 255, 255), vision_rect, (direction - playerviewangle/2) * (3.14/180), (direction + playerviewangle/2) * (3.14/180), playerviewradius - playerradius)

    # Draw targets only when they are inside the player's vision cone
    for target_pos, target_value, target_viewing_direction in targetlist:
        if target_value > 0:
            if target_in_view(target_pos):
                pygame.draw.circle(surface, red, target_pos, targetradius)
                target_x, target_y = target_pos
                pygame.draw.arc(
                    surface,
                    yellow,
                    (target_x - targetviewradius, target_y - targetviewradius, targetviewradius * 2, targetviewradius * 2),
                    (target_viewing_direction - targetviewangle/2) * (3.14 / 180),
                    (target_viewing_direction + targetviewangle/2) * (3.14 / 180),
                    targetviewradius - targetradius,
                )
        else:
            pygame.draw.circle(surface, grey, target_pos, targetradius)

    # Rotate each target's viewing cone over time
    for i, (target_pos, target_value, target_viewing_direction) in enumerate(targetlist):
        updated_direction = (target_viewing_direction + target_rotation_speed) % 360
        targetlist[i] = (target_pos, target_value, updated_direction)

    # Move targets toward player when they have the player in view; otherwise they stop
    chasing_targets = []
    for i, (target_pos, target_value, target_viewing_direction) in enumerate(targetlist):
        if target_value <= 0:
            chasing_targets.append(False)
            continue

        # Preserve the chasing state before movement so collision checks still know if a
        # target was actively pursuing the player in the same frame.
        is_chasing = player_in_view(target_pos, target_viewing_direction)
        chasing_targets.append(is_chasing)

        if is_chasing:
            tx, ty = target_pos
            dx = x - tx
            dy = y - ty
            dist = math.hypot(dx, dy)
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
                move_dist = min(target_speed, dist)
                new_pos = (tx + nx * move_dist, ty + ny * move_dist)
            else:
                new_pos = target_pos
        else:
            new_pos = target_pos
        targetlist[i] = (new_pos, target_value, target_viewing_direction)

    # Check for collisions with targets
    playercolor = green
    for i, (target_pos, target_value, target_viewing_direction) in enumerate(targetlist): 
        if target_value <= 0:
            continue

        target_rect = pygame.Rect(target_pos[0] - targetradius, target_pos[1] - targetradius, targetradius * 2, targetradius * 2)
        player_rect = pygame.Rect(x, y, playerradius, playerradius)
        is_chasing = chasing_targets[i] if i < len(chasing_targets) else player_in_view(target_pos, target_viewing_direction)

        if player_rect.colliderect(target_rect):
            score += 1
            if is_chasing:
                playercolor = red
                print("Player caught by target!")
                score -= 1
                return "lose"
            targetlist[i] = (target_pos, 0, target_viewing_direction)
        elif is_chasing:
            playercolor = orange
    #check for win condition
    if all(target_value <= 0 for _, target_value, _ in targetlist):
        print("All targets neutralized! You win!")
        return "win"

    # Draw player
    pygame.draw.circle(surface, playercolor, (x, y), playerradius)    
    
    pressed = pygame.key.get_pressed()

    move_x = 0
    move_y = 0
    if pressed[pygame.K_w] or pressed[pygame.K_UP]:
        if pressed[pygame.K_w]:
            displaylist[0] = ((1,0),'w', 1)
            move_y -= 1
        direction = up
    else:
        displaylist[0] = ((1,0),'w', 0)
    if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
        if pressed[pygame.K_s]:
            displaylist[1] = ((0,1),'s', 1)
            move_y += 1
        direction = down
    else:
        displaylist[1] = ((0,1),'s', 0)
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        if pressed[pygame.K_a]:
            displaylist[2] = ((1,1),'a', 1)
            move_x -= 1
        direction = left
    else:
        displaylist[2] = ((1,1),'a', 0)
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        if pressed[pygame.K_d]:
            displaylist[3] = ((2,1),'d', 1)
            move_x += 1
        direction = right
    else:
        displaylist[3] = ((2,1),'d', 0) 

    if move_x != 0 and move_y != 0:
        move_amount = normalizedspeed
        if move_y < 0 and move_x > 0:
            direction = upright
        elif move_y < 0 and move_x < 0:
            direction = upleft
        elif move_y > 0 and move_x > 0:
            direction = downright
        elif move_y > 0 and move_x < 0:
            direction = downleft
    else:
        move_amount = playerspeed

    if move_x != 0:
        x += move_x * move_amount
    if move_y != 0:
        y += move_y * move_amount

    x = max(0, min(x, WIDTH - playerradius * 2))
    y = max(0, min(y, HEIGHT - playerradius * 2))

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        playerspeed = 4
        displaylist[5] = ((3,2),'Space', 1)
        print('Fast mode activated')
    elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
        playerspeed = 1
        displaylist[4] = ((0,2),'Shift', 1)
        print('Slow mode activated')
    else:
        playerspeed = 2
        displaylist[4] = ((0,2),'Shift', 0)
        displaylist[5] = ((3,2),'Space', 0)
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

def draw_gameover(surface, mouse_pos, mouse_clicked, condition):
    print(f"Game over condition: {condition}, Score: {score}")
    if condition == "win":
        surface.fill((30, 100, 30))
        gameover_title = pygame.font.SysFont(None, 60).render("You Win!", True, (255, 255, 255))
        surface.blit(gameover_title, (WIDTH//2 - gameover_title.get_width()//2, HEIGHT//2 - 120))
    elif condition == "lose":
        surface.fill((100, 30, 30))
        gameover_title = pygame.font.SysFont(None, 60).render("Game Over", True, (255, 255, 255))
        surface.blit(gameover_title, (WIDTH//2 - gameover_title.get_width()//2, HEIGHT//2 - 120))
    gameover_score = pygame.font.SysFont(None, 60).render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(gameover_score, (WIDTH//2 - gameover_score.get_width()//2, HEIGHT//2 - 60))

    button_font = pygame.font.SysFont(None, 40)
    back_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)

    # Draw Back to Menu button
    pygame.draw.rect(surface, (180, 180, 70), back_button_rect)
    back_text = button_font.render("Main Menu", True, (255, 255, 255))
    surface.blit(back_text, (back_button_rect.centerx - back_text.get_width()//2, back_button_rect.centery - back_text.get_height()//2))

    if mouse_clicked:
        if back_button_rect.collidepoint(mouse_pos):
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
            elif action == "win" or action == "lose":
                current_screen = GAMEOVER
        elif current_screen == PAUSE:
            action = draw_pause(screen, mouse_pos, mouse_clicked)
            if action == "resume":
                current_screen = GAMEPLAY
            elif action == "main_menu":
                current_screen = MAIN_MENU
        elif current_screen == GAMEOVER:
            oldaction = action  # Store the previous action to pass to draw_gameover
            action = draw_gameover(screen, mouse_pos, mouse_clicked, oldaction)
            if action == "main_menu":
                current_screen = MAIN_MENU 

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()