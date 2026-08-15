#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
inittime =pygame.time.get_ticks()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
lane = 6
lane_height = 100
lane_space = 40
laneline = 2 * round(SCREEN_HEIGHT / (lane_height+lane_space))-1

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (round(SCREEN_WIDTH*(random.randint(1,lane-2))/lane)+SCREEN_WIDTH/lane/2, 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (round(SCREEN_WIDTH*(random.randint(1,lane-2))/lane)+SCREEN_WIDTH/lane/2, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 500)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if self.rect.top > self.rect.height:
        #      #if pressed_keys[K_SPACE]:
        #      #    self.rect.move_ip(0, -self.rect.height*2)
        #      if pressed_keys[K_UP]:
        #          self.rect.move_ip(0, -SPEED)
        #if self.rect.bottom < SCREEN_HEIGHT:        
        #      if pressed_keys[K_DOWN]:
        #          self.rect.move_ip(0, SPEED)
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
E2 = Enemy()

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
      
    #Creating Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    if SCORE > 20:
        enemies.add(E2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    if SCORE >20:
        all_sprites.add(E2)

    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    #DISPLAYSURF.blit(background, (0,0))
    DISPLAYSURF.fill('grey35')

    # road lanes
    timepass = pygame.time.get_ticks() - inittime
    #inity = 0
    inity = 10 * timepass / FPS
    
    for i in range(laneline):
        for j in range(lane):
            if lane-1 > j > 1:
                pygame.draw.line(DISPLAYSURF, 'white', (SCREEN_WIDTH*(j)/lane, inity + (i - 1) * (lane_height + lane_space)),(SCREEN_WIDTH*(j)/lane, inity + i * (lane_height + lane_space) - lane_space), 10)
            if j == 1 or j == lane-1:
                if j == 1:
                    pygame.draw.rect(DISPLAYSURF, 'yellowgreen', (0, 0, SCREEN_WIDTH/lane, SCREEN_HEIGHT))
                else:
                    pygame.draw.rect(DISPLAYSURF, 'yellowgreen', (SCREEN_WIDTH*(j)/lane, 0, SCREEN_WIDTH/lane, SCREEN_HEIGHT))
                if SCORE > 10:
                    bordercolor = 'crimson'
                else:
                    bordercolor = 'wheat'
                pygame.draw.line(DISPLAYSURF, bordercolor,(SCREEN_WIDTH*(j)/lane, 0), (SCREEN_WIDTH*(j)/lane, SCREEN_HEIGHT), 10)
        
    if inity + SCREEN_HEIGHT - (lane_height + lane_space) > SCREEN_HEIGHT:
        inittime = pygame.time.get_ticks()
    
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        
    leftside = pygame.Rect((0,0),(SCREEN_WIDTH/lane, SCREEN_HEIGHT))
    rightside = pygame.Rect((SCREEN_WIDTH*(lane-1)/lane,0),(SCREEN_WIDTH, SCREEN_HEIGHT))
    leftcrash = P1.rect.colliderect(leftside)
    rightcrash = P1.rect.colliderect(rightside)

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies) or (SCORE>10 and (leftcrash or rightcrash)):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
                 
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        scores = font.render(str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (SCREEN_WIDTH/2 -len(str(SCORE))*30/2, SCREEN_HEIGHT/2 + 50))
        
        pygame.display.update()
        for entity in all_sprites:
              entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        

    pygame.display.update()
    FramePerSec.tick(FPS)
