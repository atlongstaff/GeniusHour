
import os
import sys
import pygame
import random
from pygame import *
import numpy as np
gamecount = 0
state = []
statel = []
weightlist = []
pygame.init()
weights = [-6.045241219211721, 1.1039546954332096, 2.1507645948876233, -7.143781348878972, 4.687756908039491, -7.359203087871767, -0.5280483076334046, -3.7938639953391786, -2.822856884632414, -2.1299312696715096, -4.692862623539003, 1.1946908982497937, -5.915071090792334, -6.54023831926035, -6.604373493493526, 11.136821126974088, -0.5332899524914365, 9.208738118815365, 0.025091588936894116, -3.0489921287658177, 4.501045253145343, 9.086163298436551, 1.6973997310034339, -4.9568222693103365, -12.082398512147778, -1.918214160649974, -6.578295518804014, 5.769805029272703, 4.740812490071971, 2.188083257792566, -1.9721795086553306, -1.750855700841424, -1.980717142258628, -1]
scorel = []

print(weights)

scr_size = (width,height) = (600,150)
FPS = 60
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Run ")

jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

def disp_gameOver_msg(retbutton_image,gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)

def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

class Dino():
    def __init__(self,sizex=-1,sizey=-1):
        self.images,self.rect = load_sprite_sheet('dino.png',5,1,sizex,sizey,-1)
        self.images1,self.rect1 = load_sprite_sheet('dino_ducking.png',2,1,59,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5
        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width
    def draw(self):
        screen.blit(self.image,self.rect)
    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False
    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity
        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2
        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2
        if self.isDead:
           self.index = 4
        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width
        self.rect = self.rect.move(self.movement)
        self.checkbounds()
        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()
        self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('cacti-small.png',3,1,sizex,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.input_cactustype = random.randrange(0,3) ############################ Nural net inpt #2 ----cactus type ###########################
        self.image = self.images[self.input_cactustype]
        self.movement = [-1*speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        #print("dist?",self.rect.left)   ############################ Nural net inpt #4 ---- Cactus distance ###########################
        #print("dist????????????????",self.rect)   ############################ Nural net inpt #4 ---- Cactus distance ###########################

        self.rect.right
        if self.rect.right < 0:
            self.kill()

class Ptera( pygame.sprite.Sprite):
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60]
        self.input_birdheight = random.randrange(0,3) ############################ Nural net inpt #1 ----Bird height ###########################
        self.rect.centery = self.ptera_height[self.input_birdheight]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        self.rect.right ############################ Nural net inpt #3 ---- teradactle distance ###########################
        if self.rect.right < 0:
            self.kill()

class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('cloud.png',int(90*30/42),30,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Scoreboard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.tempimages,self.temprect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,score):
        score_digits = extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0

def introscreen():
    temp_dino = Dino(44,47)
    temp_dino.isBlinking = True
    gameStart = False

    temp_ground,temp_ground_rect = load_sprite_sheet('ground.png',15,1,-1,-1,-1)
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image('logo.png',300,140,-1)
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0],temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo,logo_rect)
            temp_dino.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True

def gameplay(state,statel,gamecount,weightlist,maxweight):

    state = []
    weights = [1.616797984770599e-08, -1.1797378113098196e-08, -8.79433831794616e-09, 1.0849769560821527e-09, -1.0981389289717385e-09, -1.3292259722625478e-09, 6.665210001821512e-10, 3.684057527281288e-10, 3.3060019264993626e-10, -3.3355332543417033e-10, 1.1882848741527957e-10, 5.802291701834183e-10, 3.445650102833289e-10, -2.2560444713257117e-10, 3.1001092407844664e-10, 9.909097391715416e-11, 1.4897043702633553e-10, 5.5544169706898127e-11, 9.380844501838645e-11, -4.0042137862479496e-12, 1.9373992103115066e-11, -4.2427204266688513e-11, -1.090047768198841e-11, 2.3423207443248083e-11, -2.2012066123475913e-12, 9.483492115893085e-12, -7.461264485464436e-12, 1.396186198799703e-12, 1.7852099082280966e-13, -1.3823681647990977e-12, -3.1358827075652696e-12, -1.2149096089163439e-12, 9.207732752101243e-13, -1]

    input_cactustype = 0
    input_cactusdistance = 0
    global high_score
    gamespeed = 4  ############################ Nural net inpt #5 ---- Game speed ###########################
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = Dino(44,47)
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0
    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    


    retbutton_image,retbutton_rect = load_image('replay_button.png',35,31,-1)
    gameover_image,gameover_rect = load_image('game_over.png',190,11,-1)

    temp_images,temp_rect = load_sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver and gamecount <11:

            for c in cacti:
                c.movement[0] = -1*gamespeed############################ Nural net inpt #5 ---- Game speed(change) ###########################
                if pygame.sprite.collide_mask(playerDino,c):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            for p in pteras:
                p.movement[0] = -1*gamespeed ############################ Nural net inpt #5 ---- Game speed(change) ###########################
                if pygame.sprite.collide_mask(playerDino,p):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    CactusV = Cactus(gamespeed,40,40)
                    last_obstacle.add(CactusV)
                    input_cactustype = CactusV.input_cactustype##########################sigmoid input definitions hidden layer   ##########################////////////////////////////////////error#////////////////////////////////////error#////////////////////////////////////error#////////////////////////////////////error
                    input_cactusdistance = input_cactusdistance##########################sigmoid input definitions hidden layer   ##########################//////////////////////////////////////////////////////////////////////////////////
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
                            last_obstacle.empty()
                            CactusV = Cactus(gamespeed,40,40)
                            last_obstacle.add(CactusV)
                            input_cactustype = CactusV.input_cactustype##########################sigmoid input definitions hidden layer   ##########################////////////////////////////////////error#////////////////////////////////////error#////////////////////////////////////error#////////////////////////////////////error
                            input_cactusdistance = input_cactusdistance  ##########################sigmoid input definitions hidden layer   ##########################//////////////////////////////////////////////////////////////////////////////////
                       

            if len(pteras) == 0 and random.randrange(0,200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        PteraV = Ptera(gamespeed,40,40)
                        last_obstacle.add(Ptera(Ptera, 46, 40))
                        input_birdheight = PteraV.input_birdheight##########################sigmoid input definitions hidden layer   ##########################
                        input_birddistance = PteraV.rect.right##########################sigmoid input definitions hidden layer   ##########################
            else:
                input_birdheight = 0
                input_birddistance = 0
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
            ##########################sigmoid hidden layer 1  ##########################
            #print(input_birdheight*weights[0]+input_cactustype*weights[4]+input_birddistance*weights[8]+input_cactusdistance*weights[12]+ gamespeed*weights[16]+1*weights[20])
                Hidden_layer1 = 1/(1+2.71828182**(input_birdheight*weights[0]+input_cactustype*weights[4]+input_birddistance*weights[8]+input_cactusdistance/10*weights[12]+ gamespeed*weights[16]+1*weights[20]))
               ##########################sigmoid hidden layer 2  ##########################
                Hidden_layer2 = 1/(1+2.71828182**(input_birdheight*weights[1]+input_cactustype*weights[5]+input_birddistance*weights[9]+input_cactusdistance/10*weights[13]+ gamespeed*weights[17]+1*weights[21]))
               ##########################sigmoid hidden layer 3  ##########################
                Hidden_layer3 = 1/(1+2.71828182**(input_birdheight*weights[2]+input_cactustype*weights[6]+input_birddistance*weights[10]+input_cactusdistance/10*weights[14]+ gamespeed*weights[18]+1*weights[22]))
                ##########################sigmoid hidden layer 4  ##########################
                Hidden_layer4 = 1/(1+2.71828182**(input_birdheight*weights[3]+input_cactustype*weights[7]+input_birddistance*weights[11]+input_cactusdistance/10*weights[15]+ gamespeed*weights[19]+1*weights[23]))
                
                #print("hiddenlayer1",Hidden_layer1)
                #print("hiddenlayer2",Hidden_layer2)
                #print("hiddenlayer3",Hidden_layer3)
                #print("hiddenlayer4",Hidden_layer4) 

                ##########################sigmoid output layer 1  ##########################
                output1 = 1/(1+2.71828182**(Hidden_layer1*weights[24]+Hidden_layer2*weights[26]+Hidden_layer3*weights[28]+Hidden_layer4*weights[30]+1*weights[32]))
             ##########################sigmoid output layer 2  ##########################
                output2 = 1/(1+2.71828182**(Hidden_layer1*weights[25]+Hidden_layer2*weights[27]+Hidden_layer3*weights[29]+Hidden_layer4*weights[31]+1*weights[33]))

                print("output1",Hidden_layer1)
                print("output2",Hidden_layer2) 
                print("input_birdheight",input_birdheight)
                print("input_cactustype",input_cactustype)
                print("input_birddistance",input_birddistance)
                print("input_cactusdistance",input_cactusdistance)
                print("gamespeed",gamespeed)
                print (gamecount,"gamecount")
                if output1 >= 0.5:#/##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/ Nural net output #1 ---- jumping #/#/#/#/#/#/#/#/#/#/#/#/##/#/#/#/
                    if playerDino.rect.bottom == int(0.98*height):
                        playerDino.isJumping = True
                        if pygame.mixer.get_init() != None:
                            jump_sound.play()
                        playerDino.movement[1] = -1*playerDino.jumpSpeed

                if output2 >= 0.9: #/##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/ Nural net output #2 ---- ducking #/#/#/#/#/#/#/#/#/#/#/#/##/#/#/#/
                    if not (playerDino.isJumping and playerDino.isDead):
                        playerDino.isDucking = True

            #if event.type == pygame.KEYUP:
             #   if event.key == pygame.K_DOWN:
             #       playerDino.isDucking = False
                if len(clouds) < 5 and random.randrange(0,300) == 10:
                    Cloud(width,random.randrange(height/5,height/2))
                CactusV.rect.left
                input_cactusdistance = CactusV.rect.left
                playerDino.update()
                cacti.update()
                pteras.update()
                clouds.update()
                new_ground.update()
                scb.update(playerDino.score)
                highsc.update(high_score)

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image,HI_rect)
                    cacti.draw(screen)
                    pteras.draw(screen)
                    playerDino.draw()

                    pygame.display.update()
                clock.tick(FPS)

                if playerDino.isDead:
                    gameOver = True
                    gamecount += 1
                    
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter%700 == 699:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

            if gameQuit:
                break

            while gameOver:
                if pygame.display.get_surface() == None:
                    print("Couldn't load display surface")
                    gameQuit = True
                    gameOver = False
                else:

                    gameOver = False
                    gameplay(state,statel,gamecount,weightlist,scorel)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameQuit = True
                        gameOver = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                gameQuit = True
                                gameOver = False
                        

                highsc.update(high_score)
                if pygame.display.get_surface() != None:
                    disp_gameOver_msg(retbutton_image,gameover_image)
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image,HI_rect)
                    pygame.display.update()
                clock.tick(FPS)


        pygame.quit()
        quit()

def main(state,statel,gamecount,weightlist,scorel):
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay(state,statel,gamecount,weightlist,scorel)

main(state,statel,gamecount,weightlist,scorel)

