import pygame, sys
from pygame.locals import *
import random, time

#CONSTANTS
screen_width = 400
screen_height = 600

pygame.init()

inittime =pygame.time.get_ticks()
screen = pygame.display.set_mode((screen_width,screen_height))

while True:
    screen.fill('grey40')
    for event in pygame.event.get():    
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    timepass = pygame.time.get_ticks() - inittime
    inity = 10 * timepass /60
    for i in range(4):
        pygame.draw.line(screen, 'white', (screen_width/3, inity + i*210 - 210),(screen_width/3, inity+i*210-60), 10)
        pygame.draw.line(screen, 'white', (screen_width*2/3, inity + i*210 - 210),(screen_width*2/3, inity+i*210-60), 10)
        
    if inity + 390 > screen_height:
        inittime = pygame.time.get_ticks()
    pygame.display.update()