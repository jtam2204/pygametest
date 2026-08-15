import pygame
import random, math

# Constants
window_width = 1280
window_height = 720
dicewidth = 40
basesize = 250

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font = pygame.font.Font("LuckiestGuy-Regular.ttf", 25)
bigfont = pygame.font.Font(None, 60)  # Font for displaying text
title = True
running = False
dt = 0
game_difficulty = "Normal"

# Load images
# tian=pygame.image.load('tian.png').convert()
# xia=pygame.image.load('xia.png').convert()
# tai=pygame.image.load('tai.png').convert()
# ping=pygame.image.load('ping.png').convert()

# Load background image once (outside your loop, after pygame.init())
rolldice_idle = pygame.image.load("rolldice_idle.png").convert_alpha()
rolldice_hover = pygame.image.load("rolldice_hover.png").convert_alpha()
background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (window_width, window_height))
barricade_img=pygame.image.load('barricade.png').convert_alpha()
blue_img = {
    i: pygame.transform.smoothscale(
        pygame.image.load(f"blue_{i}.png").convert_alpha(),
        (basesize, basesize)
    )
    for i in range(1, 5)  # adjust range as needed
}
blueflag_img = {
    i: pygame.transform.smoothscale(
        pygame.image.load(f"blueflag_{i}.png").convert_alpha(),
        (basesize, basesize)
    )
    for i in range(1, 4)  # adjust range as needed
}

red_img = {
    i: pygame.transform.smoothscale(
        pygame.image.load(f"red_{i}.png").convert_alpha(),
        (basesize, basesize)
    )
    for i in range(1, 5)  # adjust range as needed
}
redflag_img = {
    i: pygame.transform.smoothscale(
        pygame.image.load(f"redflag_{i}.png").convert_alpha(),
        (basesize, basesize)
    )
    for i in range(1, 4)  # adjust range as needed
}

weapon_size = (120, 80)

weapon_images = {
    1: pygame.transform.smoothscale(pygame.image.load("cannon_1.png").convert_alpha(), weapon_size),
    2: pygame.transform.smoothscale(pygame.image.load("cannon_2.png").convert_alpha(), weapon_size),
    3: pygame.transform.smoothscale(pygame.image.load("fighter_1.png").convert_alpha(), weapon_size),
    4: pygame.transform.smoothscale(pygame.image.load("fighter_2.png").convert_alpha(), weapon_size),
    5: pygame.transform.smoothscale(pygame.image.load("fighter_3.png").convert_alpha(), weapon_size),
}

def reset_game():
    global leftscore, rightscore
    global leftdefscore, rightdefscore
    global leftweapon, rightweapon
    global playerattack, battleoption, attackweapon, plane, endtime, enemyattack
    global battle_result, dice_display_time, rolled_dice, pending_attack, pending_enemy_attack, playdice
    # Reset player scores max 4
    leftscore = 4          # or whatever your starting value is
    rightscore = 4

    # Reset defenses max 8
    leftdefscore = 3
    rightdefscore = 3

    # Reset weapons
    leftweapon = [0,0,0,0,0,0]  # adjust the length if needed
    rightweapon = [0,0,0,0,0,0]

    enemyattack = False
    playerattack = False
    battleoption = [0,0,0,0,0,0,0,0]
    attackweapon = False
    plane = False
    endtime=0

    # Store dice result and timer
    battle_result = ""
    dice_display_time = 0  # Track when to stop displaying dice
    rolled_dice = []  # Store dice roll values
    playdice = False

    pending_attack = None  # store attack info while animation runs
    pending_enemy_attack = None


def draw_dice(xcord, ycord, roll):
    pygame.draw.rect(screen, "white", (xcord, ycord, dicewidth, dicewidth))
    pygame.draw.rect(screen, "black", (xcord, ycord, dicewidth, dicewidth), 2)  # Border

    if roll in [1, 3, 5]:
        pygame.draw.circle(screen, "black", (xcord + dicewidth / 2, ycord + dicewidth / 2), 5)
    if roll >= 2:
        pygame.draw.circle(screen, "black", (xcord + dicewidth / 4, ycord + dicewidth / 4), 5)
        pygame.draw.circle(screen, "black", (xcord + 3 * dicewidth / 4, ycord + 3 * dicewidth / 4), 5)
    if roll >= 4:
        pygame.draw.circle(screen, "black", (xcord + 3 * dicewidth / 4, ycord + dicewidth / 4), 5)
        pygame.draw.circle(screen, "black", (xcord + dicewidth / 4, ycord + 3 * dicewidth / 4), 5)
    if roll == 6:
        pygame.draw.circle(screen, "black", (xcord + dicewidth / 4, ycord + dicewidth / 2), 5)
        pygame.draw.circle(screen, "black", (xcord + 3 * dicewidth / 4, ycord + dicewidth / 2), 5)

def dice_roll():
    return random.randint(1, 6)  

def dice_battle():
    print("Rolling dice for battle")
    global battle_result, rolled_dice, dice_display_time, playerattack, pending_enemy_attack
    rolled_dice = [dice_roll(), dice_roll(), dice_roll(), dice_roll()]
    d1, d2, d3, d4 = rolled_dice
    draw_dice(window_width / 2 - 40 - dicewidth, window_height / 2 - 40 - dicewidth, d1)
    draw_dice(window_width / 2 - 40 - dicewidth, window_height / 2 + 40, d2)
    draw_dice(window_width / 2 + 40, window_height / 2 - 40 - dicewidth, d3)
    draw_dice(window_width / 2 + 40, window_height / 2 + 40, d4)
    if d1 + d2 > d3 + d4:
        battle_result = "Your Turn"
    elif d1 + d2 < d3 + d4:
        battle_result = "Opponent's Turn"
    else:
        battle_result = "Roll again"

def computerturn(difficulty='normal'):
    print("Computer's turn with difficulty:", difficulty)
    global leftweapon, leftdefscore, leftscore, rightdefscore, rightweapon, pending_enemy_attack, attackweapon, enemyattack

    enemyoption = []
    preferoption = [0] * 8

        # --- CAN DO OPTIONS ---
    if rightdefscore < 8:  
        enemyoption.append(0)  # build shield
    if 0 in rightweapon or 1 in rightweapon:  
        enemyoption.append(1)  # build cannon
    if 0 in rightweapon or 3 in rightweapon:  
        enemyoption.append(2)  # build fighter
    if 4 in rightweapon:  
        enemyoption.append(3)  # load fighter

    # attack enemy cannon
    if (2 in rightweapon or 5 in rightweapon) and (2 in leftweapon or 1 in leftweapon):  
        enemyoption.append(4)
    # attack enemy fighter
    if 5 in rightweapon and (5 in leftweapon or 4 in leftweapon or 3 in leftweapon):  
        enemyoption.append(5)
    # attack shield
    if 2 in rightweapon and leftdefscore > 0:  
        enemyoption.append(6)
    # attack castle (rules updated)
    if 5 in rightweapon and leftscore > 0:  
        enemyoption.append(7)  # fighter can always attack castle
    elif 2 in rightweapon and leftdefscore == 0 and leftscore > 0:  
        enemyoption.append(7)  # cannon only if no shield

        # --- DIFFICULTY SCALING ---
    if difficulty == 'easy':
        scale = 0.6
        fighter_priority = 1
        castle_priority = 1
    elif difficulty == 'normal':
        scale = 1.0
        fighter_priority = 2
        castle_priority = 2
    elif difficulty == 'hard':
        scale = 1.8   # overall aggressiveness
        fighter_priority = 3  # high priority against loaded fighters
        castle_priority = 3   # castle finishing blows strongly preferred
    else:
        scale = 1.0
        fighter_priority = 2
        castle_priority = 2

    # --- BASE WEIGHTING ---
    if 0 in rightweapon: preferoption[1] += int(1 * scale); preferoption[2] += int(2 * scale)
    if 1 in rightweapon: preferoption[1] += int(1 * scale)
    if 2 in rightweapon: preferoption[6] += int(2 * scale); preferoption[7] += int(castle_priority * scale)
    if 3 in rightweapon: preferoption[2] += int(1 * scale)
    if 4 in rightweapon: preferoption[3] += int(2 * scale)
    if 5 in rightweapon: preferoption[5] += int(2 * scale); preferoption[7] += int(castle_priority * scale)
    if 5 not in rightweapon: preferoption[2] += int(1 * scale); preferoption[3] += int(1 * scale)

    if rightdefscore == 0: preferoption[0] += int(2 * scale)
    elif rightdefscore < 3: preferoption[0] += int(1 * scale)
    if rightscore < 3:
        preferoption[0] += int(1 * scale); preferoption[3] += int(1 * scale)
        preferoption[5] += int(1 * scale); preferoption[7] += int(castle_priority * scale)

    if leftdefscore == 0: preferoption[7] += int(castle_priority * scale)
    elif leftdefscore > 3: preferoption[6] += int(1 * scale)

    if leftscore >= 1: preferoption[6] += int(1 * scale); preferoption[7] += int(castle_priority * scale)
    if leftscore >= 2: preferoption[6] += int(1 * scale); preferoption[7] += int(castle_priority * scale)
    if leftscore >= 3: preferoption[6] += int(1 * scale); preferoption[7] += int(castle_priority * scale)
    if leftscore == 4: preferoption[6] += int(1 * scale); preferoption[7] += int(castle_priority * scale)

    if 2 in leftweapon: preferoption[4] += int(1 * scale)
    if 4 in leftweapon: preferoption[3] += int(1 * scale); preferoption[5] += int(1 * scale)
    if 5 in leftweapon: preferoption[3] += int(2 * scale); preferoption[5] += int(fighter_priority * scale)

    # --- NEW RULE: Prioritize attacking loaded enemy fighter if castle not low ---
    if 5 in leftweapon:  # enemy has loaded fighter
        if leftscore > 1:  # only if castle not at critical
            preferoption[4] += int(2 * scale)  # cannon attack fighter
            preferoption[6] += int(2 * scale)  # fighter attack fighter

    # --- CHOOSE ACTION USING WEIGHTED RANDOMNESS ---
    compareoption = [preferoption[i] for i in enemyoption]

    if difficulty == 'easy': randomness = 0.5
    elif difficulty == 'normal': randomness = 0.3
    elif difficulty == 'hard': randomness = 0.1
    else: randomness = 0.3

    total = sum(compareoption)
    if total > 0:
        weights = [(c + randomness) / (total + randomness*len(compareoption)) for c in compareoption]
        preferindex = random.choices(enemyoption, weights=weights, k=1)[0]
    else:
        preferindex = random.choice(enemyoption)

    if preferindex >= 4:
        enemyattack = True
        if 2 in rightweapon and (preferindex != 5 or (preferindex == 7 and leftdefscore < 0)):
            weapon_index = rightweapon.index(2)
        else:
            weapon_index = rightweapon.index(5)

        if  preferindex <=5: # attack cannon or fighter
            attackweapon = True
        else: # attack shield or castle
            attackweapon = False

        pending_enemy_attack = {
            'type': preferindex,  # which attack
            'weapon_index': weapon_index,
            'plane': (
                (rightweapon[weapon_index] == 5 if weapon_index is not None else False)
                or (preferindex == 7 and 5 in rightweapon and leftdefscore > 0)
            )
        }
    else:
        # --- ACTION EXECUTION FUNCTIONS --- 
        def build_shield(): 
            global rightdefscore 
            rightdefscore += 1 
        def build_cannon(): 
            if 1 in rightweapon: rightweapon[rightweapon.index(1)] = 2 
            elif 0 in rightweapon: rightweapon[rightweapon.index(0)] = 1 
        def build_fighter(): 
            if 3 in rightweapon: rightweapon[rightweapon.index(3)] = 4 
            elif 0 in rightweapon: rightweapon[rightweapon.index(0)] = 3 
        def load_fighter(): 
            if 4 in rightweapon: rightweapon[rightweapon.index(4)] = 5 
        # --- MAP ACTION INDEX TO FUNCTION --- 
        action_map = { 0: build_shield, 1: build_cannon, 2: build_fighter, 3: load_fighter} 
        # Execute chosen action 
        action_map[preferindex]()
        pending_enemy_attack = None
    pygame.display.update()
    clock.tick(60)
    print("Computer chose option:", preferindex)
    
# computerturn function end ------------------------------------------------------------------------------------------------------------
def title_screen():
    global game_difficulty

    # --- Button sizes ---
    button_size = (150, 50)

    # --- Load button frames ---
    btn_idle = pygame.transform.smoothscale(pygame.image.load("button_idle.png").convert_alpha(), button_size)
    btn_hover = pygame.transform.smoothscale(pygame.image.load("button_hover.png").convert_alpha(), button_size)
    btn_select = pygame.transform.smoothscale(pygame.image.load("button_select.png").convert_alpha(), button_size)

    # --- Difficulty images (scaled smaller than button) ---
    diff_scale = 0.85   # shrink inside frame
    diff_size = (int(button_size[0] * diff_scale), int(button_size[1] * diff_scale))

    diff_easy_img = pygame.transform.smoothscale(pygame.image.load("difficulty_easy.png").convert_alpha(), diff_size)
    diff_normal_img = pygame.transform.smoothscale(pygame.image.load("difficulty_normal.png").convert_alpha(), diff_size)
    diff_hard_img = pygame.transform.smoothscale(pygame.image.load("difficulty_hard.png").convert_alpha(), diff_size)

    # --- Button rects ---
    start_button = pygame.Rect(window_width/2 - button_size[0]/2, window_height/2 + 80, *button_size)
    quit_button = pygame.Rect(window_width/2 - button_size[0]/2, window_height/2 + 240, *button_size)

    spacing = 20
    total_width = button_size[0]*3 + spacing*2
    start_x = window_width/2 - total_width/2
    easy_button = pygame.Rect(start_x, window_height/2 + 160, *button_size)
    normal_button = pygame.Rect(start_x + button_size[0] + spacing, window_height/2 + 160, *button_size)
    hard_button = pygame.Rect(start_x + (button_size[0] + spacing)*2, window_height/2 + 160, *button_size)

    # --- Title image ---
    title_image = pygame.image.load("title.png").convert_alpha()
    title_image = pygame.transform.smoothscale(title_image, title_image.get_size())
    title_rect = title_image.get_rect(center=(window_width/2, window_height/2))

    # --- Start/Quit button drawer ---
    def draw_std_button(rect, text, mouse_pos):
        img = btn_hover if rect.collidepoint(mouse_pos) else btn_idle
        screen.blit(img, rect)

        # Overlay text
        text_surf = font.render(text, True, "white")
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    # --- Difficulty button drawer ---
    def draw_diff_button(rect, image, mouse_pos, selected=False):
        if selected:
            frame = btn_select
        elif rect.collidepoint(mouse_pos):
            frame = btn_hover
        else:
            frame = btn_idle

        # Draw frame first
        screen.blit(frame, rect)

        # Center smaller image inside the frame
        img_rect = image.get_rect(center=rect.center)
        screen.blit(image, img_rect)

    # Default difficulty
    game_difficulty = "Normal"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return True
                elif quit_button.collidepoint(mouse_pos):
                    return False
                elif easy_button.collidepoint(mouse_pos):
                    game_difficulty = "Easy"
                elif normal_button.collidepoint(mouse_pos):
                    game_difficulty = "Normal"
                elif hard_button.collidepoint(mouse_pos):
                    game_difficulty = "Hard"

        # Draw screen
        screen.fill("gray20")
        screen.blit(title_image, title_rect)

        # Draw buttons
        draw_std_button(start_button, "Start", mouse_pos)
        draw_diff_button(easy_button, diff_easy_img, mouse_pos, selected=(game_difficulty=="Easy"))
        draw_diff_button(normal_button, diff_normal_img, mouse_pos, selected=(game_difficulty=="Normal"))
        draw_diff_button(hard_button, diff_hard_img, mouse_pos, selected=(game_difficulty=="Hard"))
        draw_std_button(quit_button, "Quit", mouse_pos)

        pygame.display.update()
        clock.tick(60)

def attack_animation(side='left'):
    print("Animating", side, "attack")
    global attackx, attacky, playerattack, pending_attack, plane, attackweapon, r, boomcolour, dt, pending_enemy_attack, enemyattack
    whatattack = pending_attack if side == 'left' else pending_enemy_attack
    whattarget = rightweapon if side == 'left' else leftweapon
    whatside= 1 if side == 'left' else -1
    targetattack=playerattack if side == 'left' else enemyattack
    
    if whatattack is None:
        return
    
    i = whatattack['type']
    if i == 4:  # attack cannon
        if 2 in whattarget:
            targetindex = whattarget.index(2)
        elif 1 in whattarget:
            targetindex = whattarget.index(1)
    elif i == 5:  # attack fighter
        for w in [5,4,3]:
            if w in whattarget:
                targetindex = whattarget.index(w)
                break
    elif i >= 6:  # attack shield
        targetindex = 10
    targety = (targetindex+1)*35 + targetindex*80 + 40 if targetindex<6 else window_height/2
    base_speed = 500
    if attackweapon:
        targetx = window_width/2 + (whatside * 140)
    else:
        if side == 'left':
            targetx = window_width - basesize//2
        else:
            targetx = basesize//2
    speed = base_speed 
    attackindex = (whatattack['weapon_index'] if whatattack['weapon_index'] is not None else 0)
    plane = whatattack['plane']
    condition = (attackx <= targetx if side == 'left' else attackx >= targetx)
    if targetattack and condition:
        if pygame.time.get_ticks() - playerattacktime < 100:
            attacky = (attackindex+1)*35 + attackindex*80 + 40
        else:
            attackx += whatside * speed * dt
            if plane:
                laser_1 = pygame.draw.line(screen, 'crimson', (attackx-whatside*45, attacky-30), (attackx-whatside*15, attacky-30), 4)
                laser_2 = pygame.draw.line(screen, 'crimson', (attackx-whatside*45, attacky+26), (attackx-whatside*15, attacky+26), 4)
            else:
                connon_ball = pygame.draw.circle(screen, 'black', (attackx, attacky), 10)
            r = 5
    else:
        boom_radius= 80
        if targetattack and r < boom_radius:
            if r <= boom_radius/5: boomcolour='yellow2'
            elif r <= boom_radius/5 *2: boomcolour='tan1'
            elif r <= boom_radius/5 *3: boomcolour='salmon4'
            elif r <= boom_radius/5 *4: boomcolour='grey20'
            pygame.draw.circle(screen, boomcolour, (attackx+whatside*10, targety), r)
            r += 2
        else:
            apply_attack_effect(whatattack, side)                     
            plane = False
            attackx = window_width/2 - 110
    pygame.display.update()

def apply_attack_effect(attack, side):
    print("Applying", side, "attack effect")
    global rightscore, rightdefscore, rightweapon, leftdefscore, leftscore, leftweapon, attackweapon, plane
    global playerattack, enemyattack, pending_attack, pending_enemy_attack
    i = attack['type']
    if side == 'left':
        if plane:
            if 5 in leftweapon:
                leftweapon[leftweapon.index(5)] = 4
        if i == 4:  # attack cannon
            if 2 in rightweapon:
                rightweapon[rightweapon.index(2)] = 0
            elif 1 in rightweapon:
                rightweapon[rightweapon.index(1)] = 0
            attackweapon = True
        elif i == 5:  # attack fighter
            for w in [5,4,3]:
                if w in rightweapon:
                    rightweapon[rightweapon.index(w)] = 0
                    break
            attackweapon = True
        elif i == 6:  # attack shield
            rightdefscore -= 1
            attackweapon = False
        elif i == 7:  # attack castle
            rightscore -= 1
            attackweapon = False
        pending_attack = None
        playerattack = False
    else:
        if plane:
            if 5 in rightweapon:
                rightweapon[rightweapon.index(5)] = 4
        if i == 4:  # attack cannon
            if 2 in leftweapon:
                leftweapon[leftweapon.index(2)] = 0
            elif 1 in leftweapon:
                leftweapon[leftweapon.index(1)] = 0
            attackweapon = True
        elif i == 5:  # attack fighter
            for w in [5,4,3]:
                if w in leftweapon:
                    leftweapon[leftweapon.index(w)] = 0
                    break
            attackweapon = True
        elif i == 6:  # attack shield
            leftdefscore -= 1
            attackweapon = False
        elif i == 7:  # attack castle
            leftscore -= 1
            attackweapon = False
        pending_enemy_attack = None
        enemyattack = False
    pygame.display.update()

def game_loop(): # main game loop ------------------------------------------------------------------------------------------------------------
    global leftscore, rightscore, endtime
    global leftdefscore, rightdefscore
    global leftweapon, rightweapon
    global playerattack, battleoption, attackweapon, plane, enemyattack
    global battle_result, dice_display_time, rolled_dice
    global attackx, attackindex, playerattacktime
    global r, boomcolour 
    global dt
    global pending_attack, playerattack, pending_enemy_attack

    running = True
    endtime = 0  # make sure this resets at the start of each game

    while running:
        mouse = pygame.mouse.get_pos()
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False   # quit the game completely
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= mouse[0] <= 160 and 20 <= mouse[1] <= 60 and not playerattack and battle_result != 'Your Turn' and battle_result != 'Opponent\'s Turn':
                    dice_display_time = pygame.time.get_ticks()  # Record time when rolled 
                    dice_battle()
                    if battle_result == "Opponent's Turn":
                        computerturn(game_difficulty)
                        attackx = window_width/2 + 110
                        playerattacktime = pygame.time.get_ticks()
                        battle_result = " "
                if battle_result == "Your Turn":
                    for i in range(8):
                        topleftx = i*40+(i+1)*10
                        toplefty = window_height-50
                        if topleftx <= mouse[0] <= topleftx+40 and toplefty <= mouse[1] <= toplefty + 40 and battleoption[i] == 1:
                            if i == 0: # build shield
                                leftdefscore += 1
                            if i == 1: # build cannon
                                if 1 in leftweapon:
                                    leftweapon[leftweapon.index(1)] = 2
                                else:
                                    leftweapon[leftweapon.index(0)] = 1
                            if i == 2: # build fighter
                                if 3 in leftweapon:
                                    leftweapon[leftweapon.index(3)] = 4
                                else:
                                    leftweapon[leftweapon.index(0)] = 3
                            if i == 3: # load fighter
                                leftweapon[leftweapon.index(4)]=5
                            if i >= 4:  # attack options
                                weapon_index = leftweapon.index(2) if 2 in leftweapon and (i!=5 or (i == 7 and rightdefscore < 0)) else leftweapon.index(5)
                                pending_attack = {
                                    'type': i,  # which attack
                                    #'plane': (i == 5 or (i==4 and 2 not in leftweapon) or (i==7 and 5 in leftweapon)),
                                    'weapon_index': weapon_index,
                                    'plane': ((leftweapon[weapon_index] == 5 if weapon_index != None else False) or (i==7 and 5 in leftweapon and rightdefscore >0))
                                }
                                if  i <=5: # attack cannon or fighter
                                    attackweapon = True
                                else: # attack shield or castle
                                    attackweapon = False
                                attackx = window_width/2 - 110
                                playerattack = True
                                playerattacktime = pygame.time.get_ticks()
                            battle_result = " "
    # === DRAWING ===
    # Clear screen /background
        screen.blit(background_img, (0, 0))
        screen.blit(barricade_img, (window_width/2 - barricade_img.get_width()/2, window_height/2 - barricade_img.get_height()/2))

    #left main score
    # --- LEFT CASTLE ---
        leftrect_xcord = 0
        leftrect_ycord = window_height//2 - basesize//2

        if leftscore > 0:
            screen.blit(blue_img[leftscore], (leftrect_xcord, leftrect_ycord))

    #left defense
    # --- LEFT CASTLE FLAGS ---
        if 1 <= leftdefscore <=3:
            screen.blit(blueflag_img[leftdefscore], (leftrect_xcord, leftrect_ycord))     
        if leftdefscore >=3:
            screen.blit(blueflag_img[3], (leftrect_xcord, leftrect_ycord))

        # --- LEFT CASTLE SHIELDS ---
        castle_center_left = (leftrect_xcord + basesize // 2, leftrect_ycord + basesize // 2)
        base_radius = int((basesize * math.sqrt(2)) / 2)  # half the diagonal

        for level in range(4, min(leftdefscore, 8) + 1):
            radius = base_radius + (level - 3) * 20
            pygame.draw.circle(screen, "yellow", castle_center_left, radius, 3)

        # --- LEFT WEAPONS ---
        for i in range(6):
            weaponx = window_width / 2 - 110
            weapony = (i+1)*35 + i*80
            if leftweapon[i] in weapon_images:
                img = weapon_images[leftweapon[i]]
                rect = img.get_rect(midleft=(weaponx - 120, weapony + 40))
                screen.blit(img, rect)

    # --- RIGHT CASTLE ---
        rightrect_xcord = window_width-basesize
        rightrect_ycord = window_height//2- basesize//2
        if rightscore > 0:
            screen.blit(red_img[rightscore], (rightrect_xcord, rightrect_ycord))

    # --- RIGHT CASTLE FLAGS ---
        if 1 <= rightdefscore <=3:
            screen.blit(redflag_img[rightdefscore], (rightrect_xcord, rightrect_ycord))     
        if rightdefscore >=3:
            screen.blit(redflag_img[3], (rightrect_xcord, rightrect_ycord))
    # --- RIGHT CASTLE SHIELDS ---
        castle_center_right = (rightrect_xcord + basesize // 2, rightrect_ycord + basesize // 2)

        for level in range(4, min(rightdefscore, 8) + 1):
            radius = base_radius + (level - 3) * 20
            pygame.draw.circle(screen, "yellow", castle_center_right, radius, 3)

    # --- RIGHT WEAPONS ---
        for i in range(6):
            weaponx = window_width / 2 + 110
            weapony = (i+1)*35 + i*80
            if rightweapon[i] in weapon_images:
                img = weapon_images[rightweapon[i]]
                img_flipped = pygame.transform.flip(img, True, False)  # mirror horizontally
                rect = img_flipped.get_rect(midright=(weaponx + 120, weapony + 40))
                screen.blit(img_flipped, rect)
        # === DRAWING END ===

        # Show dice results for 1.5 second
        if pygame.time.get_ticks() - dice_display_time < 1500 and rolled_dice:
            draw_dice(window_width / 2 - 40 - dicewidth, window_height / 2 - 40 - dicewidth, rolled_dice[0])
            draw_dice(window_width / 2 - 40 - dicewidth, window_height / 2 + 40, rolled_dice[1])
            draw_dice(window_width / 2 + 40, window_height / 2 - 40 - dicewidth, rolled_dice[2])
            draw_dice(window_width / 2 + 40, window_height / 2 + 40, rolled_dice[3])

        if battle_result!= ' ':
            # Display battle result text
            text_surface = font.render(battle_result, True, (255, 255, 255))
            screen.blit(text_surface, (window_width // 2 - len(battle_result)*7, window_height - 150))

        if pending_attack!= None: 
            print("Player will attack")
            attack_animation('left')
        print ("Player attack status:", playerattack, "Pending attack:", pending_attack)
        if pending_enemy_attack!=None:
            print("Enemy will attack")
            attack_animation('right')
        print ("Enemy attack status:", enemyattack, "Pending enemy attack:", pending_enemy_attack)          

        if battle_result == 'Your Turn':
            rules = {
                0: (leftdefscore < 8), # build shield
                1: (0 in leftweapon or 1 in leftweapon), # build cannon
                2: (0 in leftweapon or 3 in leftweapon), # build fighter
                3: (4 in leftweapon), # load fighter
                4: ((2 in leftweapon or 5 in leftweapon) and (2 in rightweapon or 1 in rightweapon)), # attack cannon
                5: (5 in leftweapon and (5 in rightweapon or 4 in rightweapon or 3 in rightweapon)), # attack fighter
                6: (2 in leftweapon and rightdefscore > 0),     # attack shield
                7: ((5 in leftweapon or (rightdefscore == 0 and 2 in leftweapon)) and rightscore > 0),  # attack castle
            }

            for i, condition in rules.items():
                battleoption[i] = int(condition)

            for i in range(8): # draw buttons
                if battleoption[i] == 1:
                    topleftx = i*40+(i+1)*10
                    toplefty =window_height-50
                    if topleftx <= mouse[0] <= topleftx+40 and toplefty <= mouse[1] <= toplefty + 40:
                        if i<3: # hover
                            pygame.draw.rect(screen, 'palegreen3', (topleftx-1, toplefty-1, 42, 42))
                        elif i==3:
                            pygame.draw.rect(screen, 'turquoise2', (topleftx-1, toplefty-1, 42, 42))
                        else:
                            pygame.draw.rect(screen, 'orangered1', (topleftx-1, toplefty-1, 42, 42))
                    else:
                        if i<3: # idle
                            pygame.draw.rect(screen, 'palegreen4', (topleftx-1, toplefty-1, 42, 42))
                        elif i==3:
                            pygame.draw.rect(screen, 'turquoise4', (topleftx-1, toplefty-1, 42, 42))
                        else:
                            pygame.draw.rect(screen, 'orangered3', (topleftx-1, toplefty-1, 42, 42))
                    if i in [0,6]: # shield
                        pygame.draw.polygon(screen, 'grey', [(topleftx + 5,toplefty+10), (topleftx+20,toplefty+5), (topleftx+35,toplefty+10),(topleftx+30,toplefty+25), (topleftx+20,toplefty+35), (topleftx+10,toplefty+25)])
                        pygame.draw.polygon(screen, 'gold', [(topleftx + 4,toplefty+10), (topleftx+19,toplefty+5), (topleftx+34,toplefty+10),(topleftx+29,toplefty+25), (topleftx+19,toplefty+35), (topleftx+9,toplefty+25)], 2)
                    if i in [1,4]: # cannon
                        pygame.draw.rect(screen, 'brown', (topleftx+5, toplefty+25, 30, 10))
                        pygame.draw.rect(screen, 'grey', (topleftx+13, toplefty+5, 14, 30))
                    if i in [2,3,5]: # fighter jet
                        pygame.draw.polygon(screen, 'grey', [(topleftx+20,toplefty+15), (topleftx+35,toplefty+30), (topleftx+5,toplefty+30)])
                        pygame.draw.polygon(screen, 'grey', [(topleftx+20,toplefty+30), (topleftx+30,toplefty+35), (topleftx+10,toplefty+35)])
                        pygame.draw.polygon(screen, 'grey90', [(topleftx+20,toplefty+5), (topleftx+27,toplefty+25), (topleftx+20,toplefty+35), (topleftx+13,toplefty+25)])
                        if i == 3: # load fighter
                            pygame.draw.polygon(screen, 'brown3', [(topleftx+20, toplefty+10), (topleftx+23, toplefty+15), (topleftx+23, toplefty+30), (topleftx+17, toplefty+30), (topleftx+17, toplefty+15)])
                    if i == 7: # star 
                        pygame.draw.polygon(screen, 'gold', [(topleftx+20,toplefty), (topleftx+24,toplefty+15), (topleftx+40,toplefty+16), (topleftx+28,toplefty+25), (topleftx+33,toplefty+40), (topleftx+20,toplefty+33), (topleftx+7,toplefty+40), (topleftx+12,toplefty+25), (topleftx,toplefty+16), (topleftx+16,toplefty+15)])

        mouse = pygame.mouse.get_pos()
        if playerattack or enemyattack:
            playdice = False
        else:
            playdice = True

        #Roll Dice button      
        if playdice:
            if 20 <= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+40: 
                screen.blit(rolldice_hover, (20, 20))
            else: 
                screen.blit(rolldice_idle, (20, 20))
        
         # --- End game check ---
        if (leftscore == 0 or rightscore == 0) and endtime == 0:
            endtime = pygame.time.get_ticks()

        if leftscore == 0:
            text = bigfont.render('You lose', True, 'white') 
            screen.blit(text, (window_width/2 - (len('You lose')/2)*22, window_height/2)) 

        if rightscore == 0:
            text = bigfont.render('You win', True, 'white') 
            screen.blit(text, (window_width/2 - (len('You win')/2)*22, window_height/2)) 

        if endtime and pygame.time.get_ticks() - endtime > 2000:
            return True  # return control back to title screen

        # --- Update display ---
        pygame.display.update()
        dt = clock.tick(60) / 1000
while True:
    reset_game()             # <-- reset all scores, weapons, shields
    if not title_screen():   # Quit pressed
        break  
    if not game_loop():      # if game loop returns False, quit
        break

pygame.quit()
