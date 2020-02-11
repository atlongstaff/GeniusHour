
import pygame, sys, time
from pygame.locals import *
import random
import math
pygame.init()
##################### Basic Inputs #######################

FPS=30
fpsClock=pygame.time.Clock()
width=800
height=300
DISPLAYSURF=pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption('Animation')
background=pygame.image.load('Dino.png.png')
sprite=pygame.image.load('Dino..png')
spritex=70
spritey=[150]
direction= 0 
cactus1=pygame.image.load('cactus.png')
cactus1x=800
cactus1y=220
cactus2=pygame.image.load('cactusW.png')
cactus2x=1000
cactus2y=220
cactus3=pygame.image.load('cactusS.png')
cactus3x=1600
cactus3y=220
cactusspeed = 8
dinonum = list(range(100))


next_obstical = 1
w1 = random.uniform(-1, 1)
##################### NEAT Inputs #######################
#Distance_to_obstical = cactus1x-spritex
#Gap_between_obsticals = cactus1x - cactus2x
Game_Speed = cactusspeed
Bias = 1
##################### NEAT weights #######################

inmutation =  random.randint(0,4)
outmutation = random.randint(0,2)
gamespeed_at_death = []
Nuralweights = []
##################### sigmoid function weights #######################

#if inmutation == 1:
  #o1 = 1/1+2.71828182**Distance_to_obstical*w1
##################### Game Play #######################
dir_from_key = {  
  pygame.K_UP: 'up'
}
Dcounter = [0]
while True:
    Game_Speed = cactusspeed
    DISPLAYSURF.blit(background,(0,0))
    for Dcounter in range(100):
      DISPLAYSURF.blit(sprite,(spritex,spritey[0]))
      #fitness = gamespeed_at_death[Dcounter]


    DISPLAYSURF.blit(cactus1,(cactus1x,cactus1y))
    DISPLAYSURF.blit(cactus2,(cactus2x,cactus2y))
    DISPLAYSURF.blit(cactus3,(cactus3x,cactus3y))

    # Get all the events for this tick into a list
    events = list(pygame.event.get()) 
    quit_events = [e for e in events if e.type == QUIT]
    keydown_events = [e for e in events if e.type == pygame.KEYDOWN and e.key in dir_from_key]
    keyup_events = [e for e in events if e.type == pygame.KEYUP and e.key in dir_from_key]

    # If there's no quit event, then the empty list acts like false
    if quit_events:
        pygame.quit()
        sys.exit()

    # Non-last key down events will be overridden anyway
    if keydown_events:
      direction = dir_from_key[keydown_events[-1].key]

    if cactus1x >-50:
      cactus1x -= cactusspeed
      cactus1 = pygame.image.load('cactus.png')
      next_obstical = 2
      Distance_to_obstical = cactus1x-spritex
      Gap_between_obsticals = cactus1x - cactus2x
    if cactus2x >-50:
      cactus2x -= cactusspeed
      cactus2 = pygame.image.load('cactusW.png')
      next_obstical = 3
      Distance_to_obstical = cactus2x-spritex
      Gap_between_obsticals = cactus2x - cactus3x
    if cactus3x >-50:
      cactus3x -= cactusspeed
      cactus3 = pygame.image.load('cactusS.png')
      next_obstical = 4
      Distance_to_obstical = cactus3x-spritex
      Gap_between_obsticals = cactus3x - cactus1x

    else:
      cactus1x = 800 + random.randint(-100,100)
      cactus2x = 1200 + random.randint(-100,100)
      cactus3x = 1600 + random.randint(-100,100)
      cactusspeed *= 1.1

    # Change location and image based on direction
    if spritey[0] <= 200:
      spritey[0] += 10
      sprite = pygame.image.load('Dino..png')
    elif direction == 'up':#inmutation == 1 and 1/(1+2.71828182**(Distance_to_obstical*w1)) >=0: #sigmoid function
      while spritey[0] >=100:
        DISPLAYSURF.blit(background,(0,0))
        DISPLAYSURF.blit(sprite,(spritex,spritey[0]))
        DISPLAYSURF.blit(cactus1,(cactus1x,cactus1y))
        DISPLAYSURF.blit(cactus2,(cactus2x,cactus2y))
        DISPLAYSURF.blit(cactus3,(cactus3x,cactus3y))
        pygame.display.update()
        fpsClock.tick(FPS)

        if cactus1x >-50:
          cactus1x -= cactusspeed
          cactus1 = pygame.image.load('cactus.png')
          Distance_to_obstical = cactus1x-spritex
          Gap_between_obsticals = cactus1x - cactus2x

        if cactus2x >-50:
          cactus2x -= cactusspeed
          cactus2 = pygame.image.load('cactusW.png')
          Distance_to_obstical = cactus2x-spritex
          Gap_between_obsticals = cactus2x - cactus3x

        if cactus3x >-50:
          cactus3x -= cactusspeed
          cactus3 = pygame.image.load('cactusS.png')
          Distance_to_obstical = cactus3x-spritex
          Gap_between_obsticals = cactus3x - cactus1x

        else:
          cactus1x = 800 + random.randint(-100,100)
          cactus2x = 1200 + random.randint(-100,100)
          cactus3x = 1600 + random.randint(-100,100)
          cactusspeed *= 1.1
        spritey[0] -= 10
        sprite = pygame.image.load('Dino..png')
    
    if  spritey[0] < 260 and spritey[0] > 180  and cactus1x < 90  and cactus1x > 50 : #gameovercheck
      print("game over")
      inmutation =  random.randint(0,4)

      cactusspeed = 8
      cactus1x = 800
      cactus2x = 1200
      cactus3x = 1600
      gamespeed_at_death.append(Game_Speed)
      print(gamespeed_at_death)

    if  spritey[0] < 230 and spritey[0] > 180 and cactus2x < 110 and  cactus2x > 20:
      print("game over")
      cactusspeed = 8
      cactus1x = 800
      cactus2x = 1200
      cactus3x = 1600
      gamespeed_at_death.append(Game_Speed)
      print(gamespeed_at_death)

    if  spritey[0] < 230 and spritey[0] > 180 and cactus3x < 90 and  cactus3x > 50:
      print("game over")
      cactusspeed = 8
      cactus1x = 800
      cactus2x = 1200
      cactus3x = 1600
      gamespeed_at_death.append(Game_Speed)
      print(gamespeed_at_death)
    # If there's a keyup event for the current direction.
    if [e for e in keyup_events if dir_from_key[e.key] == direction]:
      direction = None

    pygame.display.update()
    fpsClock.tick(FPS)