
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
spritey=[]
gamespeed_at_death=[]

dinonum = list(range(100))
for Dcounter in dinonum:
    spritey.append(750)
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





w1 = random.uniform(-1, 1)
##################### NEAT Inputs #######################
#Distance_to_obstical = cactus1x-spritex
#Gap_between_obsticals = cactus1x - cactus2x
#next_object_size = 
Game_Speed = cactusspeed
Bias = 1
network_state = []

##################### NEAT weights 23 #######################
for i in range(22):
  network_state.append(random.uniform(-1, 1))
  
print(network_state)
print(network_state[0])

##################### Game Play #######################
#Output_inputs = Distance_to_obstical*w1 +
#for Dcounter in dinonum:
  #Jump = 1/1+2.71828182**Output_inputs
  #o1 = 
#def sigmoid():
 # jump = 1/1+2.71828182**(Distance_to_obstical*w1 +Game_Speed*w2,Gap_between_obsticals*w3,next_object_size*w4, bias*w5)
  #return jump

  
##################### Game Play #######################
dir_from_key = {  
  pygame.K_UP: 'up'
}
Dcounter = [0]
while True:
    Game_Speed = cactusspeed
    DISPLAYSURF.blit(background,(0,0))
    for Dcounter in dinonum:
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
    for Dcounter in dinonum:
        print(Dcounter)
        jump = random.randint(0,1)

        if spritey[Dcounter] <= 200:
            spritey[Dcounter] += 10
            sprite = pygame.image.load('Dino..png')

        elif jump == 1:#inmutation == 1 and 1/(1+2.71828182**(Distance_to_obstical*w1)) >=0: #sigmoid function
            while spritey[Dcounter] >=100:
                DISPLAYSURF.blit(background,(0,0))
                DISPLAYSURF.blit(sprite,(spritex,spritey[Dcounter]))
                DISPLAYSURF.blit(cactus1,(cactus1x,cactus1y))
                DISPLAYSURF.blit(cactus2,(cactus2x,cactus2y))
                DISPLAYSURF.blit(cactus3,(cactus3x,cactus3y))
                pygame.display.update()
                fpsClock.tick(FPS)

            if cactus1x >-50:
                cactus1x -= cactusspeed
                cactus1 = pygame.image.load('cactus.png')
                Distance_to_obstical = cactus1x-spritex
                next_object_size = 2
                Gap_between_obsticals = cactus1x - cactus2x

            if cactus2x >-50:
              cactus2x -= cactusspeed
              cactus2 = pygame.image.load('cactusW.png')
              Distance_to_obstical = cactus2x-spritex
              next_object_size = 3
              Gap_between_obsticals = cactus2x - cactus3x

            if cactus3x >-50:
                cactus3x -= cactusspeed
                cactus3 = pygame.image.load('cactusS.png')
                Distance_to_obstical = cactus3x-spritex
                next_object_size = 1
                Gap_between_obsticals = cactus3x - cactus1x

            else:
                cactus1x = 800 + random.randint(-100,100)
                cactus2x = 1200 + random.randint(-100,100)
                cactus3x = 1600 + random.randint(-100,100)
                cactusspeed *= 1.1
            spritey[0] -= 10
            sprite = pygame.image.load('Dino..png')
    
        if  spritey[Dcounter] < 260 and spritey[Dcounter] > 180  and cactus1x < 90  and cactus1x > 50 : #gameovercheck
            print("game over")
            inmutation =  random.randint(0,4)

            cactusspeed = 8
            cactus1x = 800
            cactus2x = 1200
            cactus3x = 1600
            gamespeed_at_death.append(Game_Speed)
            print(gamespeed_at_death)

        if  spritey[Dcounter] < 230 and spritey[Dcounter] > 180 and cactus2x < 110 and  cactus2x > 20:
            print("game over")
            cactusspeed = 8
            cactus1x = 800
            actus2x = 1200
            cactus3x = 1600
            gamespeed_at_death.append(Game_Speed)
            print(gamespeed_at_death)

        if  spritey[Dcounter] < 230 and spritey[Dcounter] > 180 and cactus3x < 90 and  cactus3x > 50:
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