import pygame
import random

# Constants
window_width = 1280
window_height = 720
dicewidth = 40

# Variables
leftscore = 4  # max 4
leftdefscore = 3  # max 8
rightscore = 4
rightdefscore = 3
leftweapon = [0,0,0,0,0,0]
rightweapon = [0,0,0,0,0,0]
playerattack = False
attackx = window_width/2 - 110
battleoption = [0,0,0,0,0,0,0,0]
attackweapon = False
plane = False
endtime=0

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)
bigfont = pygame.font.Font(None, 60)  # Font for displaying text
running = True
dt = 0
tian=pygame.image.load('tian.png').convert()
xia=pygame.image.load('xia.png').convert()
tai=pygame.image.load('tai.png').convert()
ping=pygame.image.load('ping.png').convert()

# Store dice result and timer
battle_result = ""
dice_display_time = 0  # Track when to stop displaying dice
rolled_dice = []  # Store dice roll values

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
    global battle_result, rolled_dice, dice_display_time, playerattack
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
    dice_display_time = pygame.time.get_ticks()  # Record time when rolled

def computerturn():
    global leftweapon, leftdefscore, leftscore, rightdefscore, rightweapon
    enemyoption=[]
    preferoption = [0,0,0,0,0,0,0,0]
    compareoption =[]
    preferindex=[]
    # can dos
    if rightdefscore < 8:
        enemyoption.append(0)
    if 0 in rightweapon or 1 in rightweapon:
        enemyoption.append(1)
    if 0 in rightweapon or 3 in rightweapon:
        enemyoption.append(2)
    if 4 in rightweapon:
        enemyoption.append(3)
    if (2 in rightweapon or 5 in rightweapon) and (2 in leftweapon or 1 in leftweapon):
        enemyoption.append(4)
    if 5 in rightweapon and (5 in leftweapon or 4 in leftweapon or 3 in leftweapon):
        enemyoption.append(5)
    if 2 in rightweapon and leftdefscore>0:
        enemyoption.append(6)
    if (5 in rightweapon or (leftdefscore == 0 and 2 in rightweapon)) and leftscore>0:
        enemyoption.append(7)
    print(enemyoption)
    #prefer to do
    if 0 in rightweapon:
        preferoption[1]+=2
        preferoption[2]+=3
    if 1 in rightweapon:
        preferoption[1]+=1
    if 2 in rightweapon:
        preferoption[6]+=1
        preferoption[7]+=1
    if 3 in rightweapon:
        preferoption[2]+=2
    if 4 in rightweapon:
        preferoption[3]+=3
    if 5 in rightweapon:
        preferoption[5]+=1
        preferoption[7]+=2
    if 5 not in rightweapon:
        preferoption[2]+=1
        preferoption[3]+=1
    if rightdefscore==0:
        preferoption[0] += 2
    if rightdefscore<3:
        preferoption[0] += 2
    if rightdefscore<8:
        preferoption[0] += 1
    if rightscore < 3:
        preferoption[0] += 2
        preferoption[3] += 1
        preferoption[5] += 1
        preferoption[7] += 1
    if leftdefscore == 0:
        preferoption[7] += 1
    if leftdefscore > 3:
        preferoption[6] += 1
    if leftscore>=1:
        preferoption[6] += 1
        preferoption[7] += 1
    if leftscore>=2:
        preferoption[6] += 1
        preferoption[7] += 1
    if leftscore>=3:
        preferoption[6] += 1
        preferoption[7] += 1
    if leftscore==4:
        preferoption[6] += 1
        preferoption[7] += 1
    if 2 in leftweapon:
        preferoption[4] += 1
    if 4 in leftweapon:
        preferoption[3] += 2
        preferoption[5] += 1
    if 5 in leftweapon:
        preferoption[3] += 3
        preferoption[5] += 4
    for i in enemyoption:
        compareoption.append(preferoption[i])
    preferindex =  enemyoption[compareoption.index(max(compareoption))]
    if preferindex == 0:
        rightdefscore+=1
    if preferindex == 1:
        if 1 in rightweapon:
            rightweapon[rightweapon.index(1)]=2
        elif 0 in rightweapon:
            rightweapon[rightweapon.index(0)]=1
    if preferindex == 2:
        if 3 in rightweapon:
            rightweapon[rightweapon.index(3)]=4
        elif 0 in rightweapon:
            rightweapon[rightweapon.index(0)]=3
    if preferindex == 3:
        rightweapon[rightweapon.index(4)]=5
    if preferindex == 4:
        if 2 not in rightweapon:
            rightweapon[rightweapon.index(5)]=4
        if 2 in leftweapon:
            leftweapon[leftweapon.index(2)] = 0
        else:
            leftweapon[leftweapon.index(1)] = 0
    if preferindex == 5:
        rightweapon[rightweapon.index(5)]=4
        if 5 in leftweapon:
            leftweapon[leftweapon.index(5)] = 0
        elif 4 in leftweapon:
            leftweapon[leftweapon.index(4)] = 0
        else:
            leftweapon[leftweapon.index(3)] = 0
    if preferindex == 6:
        leftdefscore -= 1
    if preferindex == 7:
        leftscore -= 1
        if 2 not in rightweapon:
            rightweapon[rightweapon.index(5)]=4

while running: # main game loop ------------------------------------------------------------------------------------------------------------------------
# Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 20<= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+40 and not playerattack: 
                dice_battle()
                if battle_result == "Opponent's Turn":
                    computerturn()
            if battle_result == "Your Turn":
                for i in range(8):
                    topleftx = i*40+(i+1)*10
                    toplefty =window_height-50
                    if topleftx <= mouse[0] <= topleftx+40 and toplefty <= mouse[1] <= toplefty + 40 and battleoption[i] == 1:
                        if i == 0:
                            leftdefscore += 1
                        if i == 1:
                            if 1 in leftweapon:
                                leftweapon[leftweapon.index(1)] = 2
                            else:
                                leftweapon[leftweapon.index(0)] = 1
                        if i == 2:
                            if 3 in leftweapon:
                                leftweapon[leftweapon.index(3)] = 4
                            else:
                                leftweapon[leftweapon.index(0)] = 3
                        if i == 3:
                            leftweapon[leftweapon.index(4)]=5
                        if i >= 4:
                            playerattack =True
                            playerattacktime = pygame.time.get_ticks()
                            if i == 4:
                                if 2 not in leftweapon:
                                    plane = True
                                if 2 in rightweapon:
                                    rightweapon[rightweapon.index(2)] = 0
                                elif 1 in rightweapon:
                                    rightweapon[rightweapon.index(1)] = 0
                                attackweapon = True
                            if i == 5:
                                plane = True
                                if 5 in rightweapon:
                                    rightweapon[rightweapon.index(5)] = 0
                                elif 4 in rightweapon:
                                    rightweapon[rightweapon.index(4)] = 0
                                elif 3 in rightweapon:
                                    rightweapon[rightweapon.index(3)] = 0
                                attackweapon = True
                            if i == 6:
                                rightdefscore -=1
                                attackweapon = False
                            if i == 7:
                                rightscore -= 1
                                attackweapon = False
                                if 2 not in leftweapon:
                                    plane = True
                            if plane:
                                attackindex = leftweapon.index(5)
                                leftweapon[leftweapon.index(5)] = 4
                            else:    
                                attackindex = leftweapon.index(2)
                        battle_result = " "

    # Clear screen
    screen.fill("darkkhaki")
    pygame.draw.line(screen, "black", (window_width / 2, window_height), (window_width / 2, 0))

#left main score
    leftrect_xcord = 0
    leftrect_ycord = window_height/2- 95/2
    leftrect = pygame.draw.rect(screen, "burlywood4", (leftrect_xcord, leftrect_ycord, 95, 95))
    if leftscore >= 1:
        pygame.draw.rect(screen, "gold2", (leftrect_xcord+5, leftrect_ycord + 5, 40, 40))
        screen.blit(tian,(leftrect_xcord+5, leftrect_ycord + 5))
    if leftscore >= 2:
        pygame.draw.rect(screen, "gold2", (leftrect_xcord+50, leftrect_ycord + 5, 40, 40))
        screen.blit(xia,(leftrect_xcord+50, leftrect_ycord + 5))
    if leftscore >= 3:
        pygame.draw.rect(screen, "gold2", (leftrect_xcord+5, leftrect_ycord + 50, 40, 40))
        screen.blit(tai,(leftrect_xcord+5, leftrect_ycord + 50))
    if leftscore >= 4:
        pygame.draw.rect(screen, "gold2", (leftrect_xcord+50, leftrect_ycord + 50, 40, 40)) 
        screen.blit(ping,(leftrect_xcord+50, leftrect_ycord + 50))
#left defense
    if leftdefscore >=1:
        pygame.draw.polygon(screen, "crimson", [(leftrect_xcord+1, leftrect_ycord -5),(leftrect_xcord+1, leftrect_ycord -15),(leftrect_xcord+25, leftrect_ycord -10)])
        pygame.draw.line(screen, "brown", (leftrect_xcord+1, leftrect_ycord -15),(leftrect_xcord+1, leftrect_ycord), 2)
    if leftdefscore >=2:
        pygame.draw.polygon(screen, "crimson", [(leftrect_xcord+36, leftrect_ycord -5),(leftrect_xcord+36, leftrect_ycord -15),(leftrect_xcord+60, leftrect_ycord -10)])
        pygame.draw.line(screen, "brown", (leftrect_xcord+36, leftrect_ycord -15),(leftrect_xcord+36, leftrect_ycord), 2)
    if leftdefscore >=3:
        pygame.draw.polygon(screen, "crimson", [(leftrect_xcord+71, leftrect_ycord -5),(leftrect_xcord+71, leftrect_ycord -15),(leftrect_xcord+95, leftrect_ycord -10)])
        pygame.draw.line(screen, "brown", (leftrect_xcord+71, leftrect_ycord -15),(leftrect_xcord+71, leftrect_ycord), 2)
    if leftdefscore >=4:
        pygame.draw.rect(screen, "yellow", (leftrect_xcord - 3, leftrect_ycord - 20, 95+20, 95+40), 3)
    if leftdefscore >=5:
        pygame.draw.rect(screen, "yellow", (leftrect_xcord - 3, leftrect_ycord - 40, 95+40, 95+80), 3)
    if leftdefscore >=6:
        pygame.draw.rect(screen, "yellow", (leftrect_xcord - 3, leftrect_ycord - 60, 95+60, 95+120), 3)
    if leftdefscore >=7:
        pygame.draw.rect(screen, "yellow", (leftrect_xcord - 3, leftrect_ycord - 80, 95+80, 95+160), 3)
    if leftdefscore >=8:
        pygame.draw.rect(screen, "yellow", (leftrect_xcord - 3, leftrect_ycord - 100, 95+100, 95+200), 3)
    
     # draw left weapon
    for i in range(6):
        weaponx = window_width / 2 - 110
        weapony = (i+1)*35 + i*80
        #cannon
        if leftweapon[i] in [1, 2]:
            pygame.draw.rect(screen, 'brown', (weaponx - 85, weapony, 20, 80))
            pygame.draw.rect(screen, 'black', (weaponx - 90, weapony, 30, 10))
            pygame.draw.rect(screen, 'black', (weaponx - 90, weapony + 70, 30, 10))
            if leftweapon[i] == 2:
                pygame.draw.rect(screen, 'azure2', (weaponx - 85, weapony + 25, 85, 30))
                pygame.draw.rect(screen, 'azure3', (weaponx - 105, weapony + 30, 20, 20))
                pygame.draw.line(screen, 'azure3', (weaponx - 15, weapony + 25), (weaponx - 15, weapony + 54), 3)
        if leftweapon[i] == 5:
            pygame.draw.rect(screen, 'brown3', (weaponx - 100, weapony + 10, 40, 5))
            pygame.draw.rect(screen, 'black', (weaponx - 100, weapony + 10, 40, 5), 1)
            pygame.draw.rect(screen, 'brown3', (weaponx - 100, weapony + 65, 40, 5))
            pygame.draw.rect(screen, 'black', (weaponx - 100, weapony + 65, 40, 5), 1)
        if leftweapon[i] >=3:
            pygame.draw.polygon(screen,'azure3',[(weaponx - 60, weapony + 40), (weaponx - 90, weapony), (weaponx - 100, weapony),(weaponx- 100, weapony+ 80), (weaponx- 90, weapony+ 80)])
            pygame.draw.polygon(screen,'azure3',[(weaponx - 90, weapony + 40), (weaponx - 120, weapony + 20),(weaponx- 120, weapony+ 60)])
            pygame.draw.line(screen,'azure4', (weaponx - 90, weapony),(weaponx- 90, weapony+ 80),2)
            if leftweapon[i] >=4:
                pygame.draw.polygon(screen,'azure2',[(weaponx, weapony + 40), (weaponx - 30, weapony + 35), (weaponx - 80, weapony + 30), (weaponx - 120, weapony + 35),(weaponx- 120, weapony+ 45),(weaponx- 80, weapony+ 50), (weaponx- 30, weapony+ 45)])
                pygame.draw.polygon(screen,'azure4',[(weaponx - 25, weapony + 38),(weaponx - 50, weapony +36), (weaponx - 50, weapony+ 44), (weaponx - 25, weapony + 42)])

# right main score
    rightrect_xcord = window_width-95
    rightrect_ycord = window_height/2- 95/2
    rightrect = pygame.draw.rect(screen, "burlywood4", (rightrect_xcord, rightrect_ycord, 95, 95))
    if rightscore >= 1:
        pygame.draw.rect(screen, "gold2", (rightrect_xcord+5, rightrect_ycord + 5, 40, 40))
        screen.blit(tian,(rightrect_xcord+5, rightrect_ycord + 5))
    if rightscore >= 2:
        pygame.draw.rect(screen, "gold2", (rightrect_xcord+50, rightrect_ycord + 5, 40, 40))
        screen.blit(xia,(rightrect_xcord+50,rightrect_ycord + 5))
    if rightscore >= 3:
        pygame.draw.rect(screen, "gold2", (rightrect_xcord+5, rightrect_ycord + 50, 40, 40))
        screen.blit(tai,(rightrect_xcord+5, rightrect_ycord + 50))
    if rightscore >= 4:
        pygame.draw.rect(screen, "gold2", (rightrect_xcord+50, rightrect_ycord + 50, 40, 40))
        screen.blit(ping,(rightrect_xcord+50,rightrect_ycord + 50))
# right defense
    if rightdefscore >=1:
        pygame.draw.polygon(screen, "blue", [(rightrect_xcord+1, rightrect_ycord -5),(rightrect_xcord+1, rightrect_ycord -15),(rightrect_xcord+25, rightrect_ycord -10)])
        pygame.draw.line(screen, "brown", (rightrect_xcord+1, rightrect_ycord -15),(rightrect_xcord+1, rightrect_ycord), 2)
    if rightdefscore >=2:
        pygame.draw.polygon(screen, "blue", [(rightrect_xcord+36, rightrect_ycord -5),(rightrect_xcord+36, rightrect_ycord -15),(rightrect_xcord+60, rightrect_ycord -10)])
        pygame.draw.line(screen, "brown", (rightrect_xcord+36, rightrect_ycord -15),(rightrect_xcord+36, rightrect_ycord), 2)
    if rightdefscore >=3:
        pygame.draw.polygon(screen, "blue", [(rightrect_xcord+71, rightrect_ycord -5),(rightrect_xcord+71, rightrect_ycord -15),(rightrect_xcord+95, rightrect_ycord -10)])
        pygame.draw.line(screen, "brown", (rightrect_xcord+71, rightrect_ycord -15),(rightrect_xcord+71, rightrect_ycord), 2)
    if rightdefscore >=4:
        pygame.draw.rect(screen, "yellow", (rightrect_xcord -20 +3, rightrect_ycord - 20, 95+20, 95+40), 3)
    if rightdefscore >=5:
        pygame.draw.rect(screen, "yellow", (rightrect_xcord -40 +3, rightrect_ycord - 40, 95+40, 95+80), 3)
    if rightdefscore >=6:
        pygame.draw.rect(screen, "yellow", (rightrect_xcord -60 +3, rightrect_ycord - 60, 95+60, 95+120), 3)
    if rightdefscore >=7:
        pygame.draw.rect(screen, "yellow", (rightrect_xcord -80 +3, rightrect_ycord - 80, 95+80, 95+160), 3)
    if rightdefscore >=8:
        pygame.draw.rect(screen, "yellow", (rightrect_xcord -100 +3, rightrect_ycord - 100, 95+100, 95+200), 3)
    
    # draw right weapon
    for i in range(6):
        weaponx = window_width / 2 + 110
        weapony = (i+1)*35 + i*80
        #cannon
        if rightweapon[i] in [1, 2]:#cannon
            pygame.draw.rect(screen, 'brown', (weaponx + 65, weapony, 20, 80))
            pygame.draw.rect(screen, 'black', (weaponx + 60, weapony, 30, 10))
            pygame.draw.rect(screen, 'black', (weaponx + 60, weapony + 70, 30, 10))
            if rightweapon[i] == 2:
                pygame.draw.rect(screen, 'azure2', (weaponx, weapony + 25, 85, 30))
                pygame.draw.rect(screen, 'azure3', (weaponx + 85, weapony + 30, 20, 20))
                pygame.draw.line(screen, 'azure3', (weaponx + 15, weapony + 25), (weaponx + 15, weapony + 54), 3)
        if rightweapon[i] == 5:
            pygame.draw.rect(screen, 'brown3', (weaponx + 60, weapony + 10, 40, 5))
            pygame.draw.rect(screen, 'black', (weaponx + 60, weapony + 10, 40, 5), 1)
            pygame.draw.rect(screen, 'brown3', (weaponx + 60, weapony + 65, 40, 5))
            pygame.draw.rect(screen, 'black', (weaponx + 60, weapony + 65, 40, 5), 1)
        if rightweapon[i] >=3: #plane
            pygame.draw.polygon(screen,'azure3',[(weaponx + 60, weapony + 40), (weaponx + 90, weapony), (weaponx + 100, weapony),(weaponx+ 100, weapony+ 80), (weaponx+ 90, weapony+ 80)])
            pygame.draw.polygon(screen,'azure3',[(weaponx + 90, weapony + 40), (weaponx + 120, weapony + 20),(weaponx+ 120, weapony+ 60)])
            pygame.draw.line(screen,'azure4', (weaponx + 90, weapony),(weaponx+ 90, weapony+ 80),2)
            if rightweapon[i] >=4:
                pygame.draw.polygon(screen,'azure2',[(weaponx, weapony + 40), (weaponx + 30, weapony + 35), (weaponx + 80, weapony + 30), (weaponx + 120, weapony + 35),(weaponx+ 120, weapony+ 45),(weaponx+ 80, weapony+ 50), (weaponx+ 30, weapony+ 45)])
                pygame.draw.polygon(screen,'azure4',[(weaponx + 25, weapony + 38),(weaponx + 50, weapony +36), (weaponx + 50, weapony+ 44), (weaponx + 25, weapony + 42)])

    # Show dice results for 1 second
    if pygame.time.get_ticks() - dice_display_time < 1000 and rolled_dice:
        draw_dice(window_width / 2 - 40 - dicewidth, window_height / 2 - 40 - dicewidth, rolled_dice[0])
        draw_dice(window_width / 2 - 40 - dicewidth, window_height / 2 + 40, rolled_dice[1])
        draw_dice(window_width / 2 + 40, window_height / 2 - 40 - dicewidth, rolled_dice[2])
        draw_dice(window_width / 2 + 40, window_height / 2 + 40, rolled_dice[3])

        # Display battle result text
        text_surface = font.render(battle_result, True, (255, 255, 255))
        screen.blit(text_surface, (window_width // 2 - len(battle_result)*7, window_height - 150))
# display attack option buttons
    if battle_result == 'Your Turn':
        if leftdefscore < 8:
            battleoption[0] = 1
        else:
            battleoption[0] = 0
        if 0 in leftweapon or 1 in leftweapon:
            battleoption[1] = 1
        else:
            battleoption[1] = 0
        if 0 in leftweapon or 3 in leftweapon:
            battleoption[2] = 1
        else:
            battleoption[2] = 0
        if 4 in leftweapon:
            battleoption[3] = 1
        else:
            battleoption[3] = 0
        if (2 in leftweapon or 5 in leftweapon) and (2 in rightweapon or 1 in rightweapon):
            battleoption[4] = 1
        else:
            battleoption[4] = 0
        if 5 in leftweapon and (5 in rightweapon or 4 in rightweapon or 3 in rightweapon):
            battleoption[5] = 1
        else:
            battleoption[5] = 0
        if 2 in leftweapon and rightdefscore>0:
            battleoption[6] = 1
        else:
            battleoption[6] = 0
        if (5 in leftweapon or (rightdefscore == 0 and 2 in leftweapon)) and rightscore>0:
            battleoption[7] = 1
        else:
            battleoption[7] = 0

        for i in range(8):
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

    # left attack
    if attackweapon:
        targetx = window_width/2 + 140
        speed = 300
    else:
        targetx = window_width -110
        speed = 600
    if playerattack and attackx <= targetx:
        if pygame.time.get_ticks() - playerattacktime < 100:
            attacky = (attackindex+1)*35 + attackindex*80 + 40
        else:
            attackx += speed * dt
            if plane:
                pygame.draw.line(screen, 'crimson', (attackx-45, attacky-30), (attackx-15, attacky-30), 4)
                pygame.draw.line(screen, 'crimson', (attackx-45, attacky+26), (attackx-15, attacky+26), 4)
            else:
                pygame.draw.circle(screen, 'black', (attackx, attacky), 15)
            r = 5
    else:
        if playerattack and r < 60:
            if r <= 15:
                boomcolour='yellow2'
            elif r <= 25:
                boomcolour='tan1'
            elif r <= 40:
                boomcolour='salmon4'
            elif r <= 60:
                boomcolour='grey20'
            pygame.draw.circle(screen, boomcolour, (attackx+10, attacky), r)
            r+=1
        else:
            playerattack = False
            plane = False
            attackx = window_width/2 - 110

    mouse = pygame.mouse.get_pos()     
    # if mouse is hovered on a button it 
    # changes to lighter shade  
    if not playerattack:
        if 20 <= mouse[0] <= 20+140 and 20 <= mouse[1] <= 20+40: 
            pygame.draw.rect(screen,'grey40',[20,20,140,40])
        else: 
            pygame.draw.rect(screen,'grey10',[20,20,140,40]) 
      
        # superimposing the text onto our button 
        text = font.render('Roll Dice' , True , 'white') 
        screen.blit(text , (20+10,20+7)) 
    if (leftscore ==0 or rightscore==0) and endtime == 0:
        endtime= pygame.time.get_ticks()
    if leftscore == 0:
        text = bigfont.render('You lose' , True , 'white') 
        screen.blit(text , (window_width/2 - (len('You lose')/2)*22,window_height/2)) 
    if rightscore ==0:
        text = bigfont.render('You win' , True , 'white') 
        screen.blit(text , (window_width/2 - (len('You win')/2)*22,window_height/2)) 
    if pygame.time.get_ticks()-endtime>2000 and endtime!=0:
        running = False
    # Update the screen
    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()
