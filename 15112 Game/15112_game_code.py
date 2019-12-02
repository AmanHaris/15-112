#code by: Aman Haris
#andrew ID: asharis

#Last Updated: 2-12-19, 23:00
#Please Refer to the Project Description for explanation of code's function

import random
from math import *
import pygame
pygame.init()

#######################################################################################################
#Classes###############################################################################################
#######################################################################################################

#some preliminary functions needed in the classes

#takes a list of filenames for sprites; loads, resizes, and stores in dict.
def loadSprites(filenames, extension, ratio, initialIndex):
        character1_idle = []
        for i in range(10):
                file = filenames[0]+str(i + initialIndex) + extension
                character1_idle += [pygame.image.load(file)]

        character1_run = []
        for i in range(10):
                file = filenames[1]+str(i + initialIndex) + extension
                character1_run += [pygame.image.load(file)]

        character1_side_melee = []
        for i in range(10):
                file = filenames[2]+str(i + initialIndex) + extension
                character1_side_melee += [pygame.image.load(file)]

        character1_n_melee = []
        for i in range(10):
                file = filenames[3]+str(i + initialIndex) + extension
                character1_n_melee += [pygame.image.load(file)]

        #RESIZING CHARACTER1###
        for j in range(10):
                character1_run[j] = pygame.transform.rotozoom(character1_run[j], 0, ratio)
                character1_idle[j] = pygame.transform.rotozoom(character1_idle[j], 0, ratio)
                character1_side_melee[j] = pygame.transform.rotozoom(character1_side_melee[j], 0, ratio)
                character1_n_melee[j] = pygame.transform.rotozoom(character1_n_melee[j], 0, ratio)

        #Info is stored in this dictionary for use in other classes
        character1 = {}
        character1['run'] = character1_run
        character1['idle'] = character1_idle
        character1['side_melee'] = character1_side_melee
        character1['n_melee'] = character1_n_melee
        character1['jump'] = character1_run

        return character1

#resizes image in a desired ratio, expressed as a fraction of the window dimensions
def resizeImage(image, screen_width, screen_height):
        
        width_ratio = screen_width/image.get_width()
        height_ratio = screen_height/image.get_height()

        if width_ratio < height_ratio:
                image = pygame.transform.rotozoom(image, 0, width_ratio)
        else:
                image = pygame.transform.rotozoom(image, 0, height_ratio)
        return image

#class for changing between game states
class game_events():
        
        #event flags - toggles b/w screens
        loading = True
        main_screen = False
        gamemode_screen = False
        game_mode = ""
        char_screen = False
        stage_screen = False
        guide_screen = False        
        game = False
        result = False

        #stores selected players, stage by user
        player1 = ""
        player2 = ""
        stage = ""


        
        #helpers for loading
        loading_count = 0
        
        
        #helpers for result
        count = 0
        winner = ""



#class that loads and deals with the graphical assets
class graphics():

########BACKGROUNDS######################################################
        
        

        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h

        #bg screens for menus and game
        loading_bg = pygame.image.load("./sprites/loading_bg.jpg")
        loading_bg = resizeImage(loading_bg,screen_width, screen_height)
        
        main_bg = pygame.transform.rotozoom(pygame.image.load("./sprites/main_bg.jpg"), 0, 0.7)
        main_bg = resizeImage(main_bg,screen_width, screen_height)

        guide_bg = pygame.image.load("guide.png")
        guide_bg = resizeImage(guide_bg, screen_width, screen_height)

        ice_bg = pygame.image.load("./ice_bg.png")
        ice_bg = resizeImage(ice_bg,screen_width, screen_height)
        
##Loading assets for each stage#########################################
        
        #graphics for wormhole stage
        game_bg_wormholes = []
        game_bg_max = 10 #how many frames we have
        for i in range(0,game_bg_max,2):
                file = "./space/images-0"+"0"*(3 - len(str(i+1))) + str(i+1) + ".png"
                game_bg_wormholes.append(pygame.image.load(file))
        game_bg2 = game_bg_wormholes.copy()
        game_bg2.reverse() #appending reversed vision for back-and-forth animations seen in first stage
        game_bg_wormholes.extend(game_bg2)
        game_bg_count = 0 #will be updated to cycle through the frames

        #graphics for ice stage
        game_bg_ice = []
        game_bg_max = 10 #how many frames we have
        for i in range(0,30*game_bg_max,10):
                file = "./snow/image-0"+"0"*(3 - len(str(i+1))) + str(i+1) + ".jpeg"
                game_bg_ice.append(pygame.image.load(file))
        game_bg_count = 0 #will be updated to cycle through the frames

        game_bg = []

        #character screen assets
        char_bg = pygame.transform.rotozoom(pygame.image.load("./player_bg.png"),0,0.75)
        char_bg = resizeImage(char_bg,screen_width/2, screen_height/2)
        char_bg_rect = char_bg.get_rect()

        #this list will be sequentually blitted in stage selection screen
        stage_icons =  [pygame.image.load("wormholes.png"), 
                                pygame.image.load("ice.png"),
                                pygame.image.load("cloud.png"),
                                pygame.image.load("planet_icon.png")]

        for i in range(len(stage_icons)):
                stage_icons[i] = resizeImage(stage_icons[i], screen_height/3.2, screen_width/3.2)

###########PLATFORMS######################################################################
        platforms = []
            
       #wormhole stage platforms##########################################################
        platform_wh = pygame.image.load("./sprites/platform.png")
        platform_wh = resizeImage(platform_wh,screen_width, screen_height)

        platform_wh = pygame.transform.rotozoom(platform_wh, 0, 0.8)
        platform2_wh = pygame.transform.rotozoom(platform_wh, 0, 0.25)
        platform3_wh =  pygame.transform.rotozoom(platform_wh, 0, 0.25)

        #all platforms stored in a list for ease of use
        platforms_wh = [platform_wh, platform2_wh, platform3_wh]


        #ice stage platforms###############################################################

        platform_ice = pygame.image.load("ice_platform2.png")
        

        platform_ice = resizeImage(platform_ice,screen_width/3, screen_height/3)
        platform_ice = pygame.transform.rotozoom(platform_ice, 0, 2) 
        platform2_ice = pygame.transform.rotozoom(platform_ice, 0, 0.9)
        platform3_ice =  pygame.transform.rotozoom(platform_ice, 0, 0.7)
        platform4_ice =  pygame.transform.rotozoom(platform_ice, 0, 0.6)
        platform5_ice =  pygame.transform.rotozoom(platform_ice, 0, 0.5)

        #all platforms stored in a list for ease of use
        platforms_ice = [platform_ice, platform2_ice, platform3_ice, platform4_ice, platform5_ice]

        #clouds stage platforms###########################################################

        cloud1 = pygame.transform.rotozoom(pygame.image.load("./cloud1.png"),0,0.9)
        cloud2 = pygame.transform.rotozoom(pygame.image.load("./cloud2.png"),0,0.9)

        
        platform_cld = cloud1 
        platform2_cld = cloud2
        platform3_cld = cloud1
        platform4_cld = cloud2
        platform5_cld = cloud1
        platform6_cld = cloud2

        #all platforms stored in a list for ease of use
        platforms_cld = [platform_cld, platform2_cld, platform3_cld, platform4_cld, platform5_cld, platform6_cld]




        ############
        

        portal = pygame.image.load("./portal.png")
        portal = pygame.transform.rotate(portal, 30)
        portal = resizeImage(portal,screen_width/3, screen_height/3)




        #will be updated as per resolution of user's display
        

#########CHARACTER SPRITES#############################################

        filenames = ["./sprites/png/Idle__00",
                                "./sprites/png/Run__00",
                                "./sprites/png/Jump_Attack__00",
                                "./sprites/png/Attack__00"]

        character1 = loadSprites(filenames, ".png", 0.3, 0)

        filenames = ["./png2/Idle (",
                                "./png2/Run (",
                                "./png2/JumpAttack (",
                                "./png2/Attack ("]

        character2 = loadSprites(filenames, ").png", 0.2, 1)

        filenames = ["./Robo_png/Idle (",
                                "./Robo_png/Run (",
                                "./Robo_png/JumpMelee (",
                                "./Robo_png/Melee ("]

        character3 = loadSprites(filenames, ").png", 0.25, 1)

        filenames = ["./Kunoichi_png/Idle__00",
                                "./Kunoichi_png/Run__00",
                                "./Kunoichi_png/Jump_Attack__00",
                                "./Kunoichi_png/Attack__00"]

        character4 = loadSprites(filenames, ".png", 0.28, 0)

        characters = {}

        characters['Ninja']  = character1
        characters['Knight'] = character2
        characters['Rob'] = character3
        characters['Kunoichi'] = character4     

        
######################################PROJECTILE ATTACK##################

        p_attack = [pygame.image.load("./sprites/ki_blasts1.png"),
                  pygame.image.load("./sprites/ki_blasts2.png"),
                  pygame.image.load("./sprites/ki_blasts3.png"),
                  pygame.image.load("./sprites/ki_blasts4.png"),
                  pygame.image.load("./sprites/ki_blasts5.png")]
        for i in range(5):
                p_attack[i] = pygame.transform.rotozoom(p_attack[i], 0, 0.015)

###############################################HEALTH BAR###############

        healthbar_frame = pygame.image.load("./sprites/healthbar_frame.png")
        healthbar_body = pygame.image.load("./sprites/healthbar_body.png")



#designates a rect to a platform
class makePlatform():
        def __init__(self, x, y, width, height):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.hitbox = (self.x, self.y, self.width, self.height)
#portals in stage 1
class portal():
        def __init__(self, x, y):
                self.image = graphics.portal
                self.x = x
                self.y = y 
                self.width = graphics.portal.get_width()
                self.height = graphics.portal.get_height()
                self.hitbox = (self.x,self.y, self.width,self.height)
                self.rect = self.image.get_rect()
                self.rect.center = (x,y)

                portal.t1 = 0
                portal.t2 = 0

#planets in stage 4
class planet():
        def __init__(self, x = 1000, y = 500, r = 200, image = ""):
                self.x = x
                self.y = y
                self.image = pygame.image.load(image)
                self.image = resizeImage(self.image, graphics.screen_width/3, graphics.screen_height/3)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()

                self.radius = r
                self.rect.center = (x, y)
                self.center = (x,y)


#everything about a playable character, as well projectiles which move
class character():
        def __init__(self, x, y, name, velocity, sprites, vel_i = 0):
                
                #Basics######
                self.name = name
                
                #sprites
                self.sprites = sprites
                self.image = sprites['idle'][0]
                        #sprites is a dictionary with the keys 'idle', 'run', etc. and their list of sprites.


                #dimensions
                self.width = self.sprites['idle'][1].get_width()
                self.height = self.sprites['idle'][1].get_height()
                
                #velocity in x-axis
                self.vel = vel_i
                self.vel0 = velocity

                #velocity in y-axis
                self.vel_y = 0#default 0, when they are standing on a platform
                self.vel_y0 = 40 #jump velocity for character
                
                #positions: x and y are constantly updated in code, x0 and y0 are the starting positon
                self.y = y
                self.y0 = y
                self.x = x
                self.x0 = x

                #hitbox: borders of the sprite, for collisions
                self.hitbox = (self.x, self.y, self.width, self.height)
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y
                self.mask = pygame.mask.from_surface(self.image)
                        
                #Player states for sprite determination:
                        #It's all put in a dictionary for ease of manipulation,
                        # as each state is mutually exclusive (see changeState function)
                
                self.sprite_state = {}
                self.sprite_state['idle'] = True
                self.sprite_state['run'] = False
                self.sprite_state['side_melee'] = False
                self.sprite_state['n_melee'] = False
                self.sprite_state['jump'] = False

                #helpers:
                self.double_jumped = False #can double jump when false
                self.btn_pressed_once = False #used for determining if a btn is tapped twice
                self.jump_t1 = 0 #used to create a time interval for jumps
                self.jump_t2 = 0
                self.angle = 0 #for rotations
                self.portal_t1 = 0
                self.portal_t2 = 0
                self.invisible = False #for Knight's special ability

                

                #other player states:
                self.direction = 1 #1 means the player is facing right, and -1 for left.
                self.health = 100
                self.health_ratio = self.health/100 #The initial/full health
                self.costume_count = 0 #indexing for going through list of sprite animation
                self.projectiles = [] #all projectile attacks generated by self



        def changeState(self, state):
                if not ((self.sprite_state['n_melee'] or self.sprite_state['side_melee'])and self.costume_count%10 != 0):
                        for key in self.sprite_state:
                                #all keys except state is set to False
                                if key!=state:
                                        self.sprite_state[key] = False
                                #if the state was not already true, it's set to true and costume count is set to 0
                                elif not self.sprite_state[key]:
                                        self.sprite_state[key] = True
                                        #self.costume_count = 0

class AI():
        #creates an instance for each game
        def __init__(self, player, opponent, platforms):
                self.player = player
                self.opponent = opponent
                self.platforms = platforms
                self.t1 = 0 #for timing actions
                self.t2 = 0
                self.detectedHitbox = False #true when colliding
                self.OldOppDir = opponent.direction 
                self.NewOppDir = opponent.direction #used to notice when player changes directions
                self.platformEdge = False #true if AI is at platform edge


        #This function makes the AI generally chase after the player, but with
        # randomness at different probabilities to make the AI's patterns
        # less predictable
        def goTo(self):
                #can crash when window is closed or game ends
                try: 
                        #update y-coordinate of closest platform below AI - 'y0',
                        # must be updated so jump can check if player is on solid groud before
                        #jumping
                        getPlatformBelow(self.player, self.platforms) 
                        delta = random.randint(-100,100) #a random variable
                        if self.opponent.y < self.player.y - 10: #if opponent is higher than AI
                                #if opp. is within range of a jump, horizontally
                                if abs(self.opponent.x - self.player.x) - 10*abs(self.player.vel) < 0:
                                        #Ai cannot detect player Knight if invisible
                                        if not self.opponent.invisible:
                                                if delta > 50:
                                                        jump(self.player) #jump towards the player with 25% prob.
                        if self.player.direction*self.opponent.direction < 0:
                                random_fluctuation = random.randint(-2,16) #another random variable,
                                                                           # defined when AI and Opp. face each other
                        else:
                                random_fluctuation = 1 

                        if delta < -90:
                                jump(self.player) #sometimes, randomly jump at 5% prob.                          

                        #if opp. is facing same direction it used to
                        if self.OldOppDir == self.NewOppDir:
                                if self.t2 - self.t1 > 100: #if a reaction time of 100ms has passed since last direction change
                                        if self.opponent.x + delta > self.player.x: #if opp. is likely to the right of AI
                                                if not self.opponent.invisible:
                                                        if random_fluctuation >= 0:
                                                                moveRight(self.player) #then probably move right
                                                        else:
                                                                moveLeft(self.player)
                                                                #move towards the player but sometimes random
                                                        self.NewOppDir = opponent.direction
                                        if self.opponent.x + delta< self.player.x: #same as above but mirrored
                                                if not self.opponent.invisible:
                                                        if random_fluctuation >= 0:
                                                                moveLeft(self.player)
                                                        else:
                                                                moveRight(self.player)
                                                        self.NewOppDir = opponent.direction
                        
                                
                                                                                      
                        else: #if opp. just fresh changed direction, reset reaction time timer
                                self.t1 = self.t2
                                self.OldOppDir = self.NewOppDir
                        
                        
                except:
                        pass
        #attacks when hitboxes collide, with a reaction time of 200ms
        def attack(self):
                self.t2 = pygame.time.get_ticks()
                hitbox = pygame.Rect(self.player.hitbox)
                if hitbox.colliderect(self.opponent.hitbox): #if hitboxes collide
                        if not self.detectedHitbox: #if first instance of deteced collision
                                self.t1 = self.t2 #measure reaction time
                                self.detectedHitbox = True
                        if self.t2 - self.t1 > 200 and self.detectedHitbox: #if reaction time > 200
                                self.player.changeState('n_melee') #attack
                                self.t1 = self.t2
                                self.detectedHitbox = False

        #predicts location in the future based on current variables,
        # to reduce probability of accidentally falling off a platform
        def predictFuture(self):

                #future x and y values of AI if current velocities are maintained for 10 frames
                future_x = self.player.x + 10*self.player.vel
                future_y = self.player.y + 10*self.player.vel_y           
               
                case_1 = True #an initial variable
                
                #creates a new instance of AI's sprite, but created at the future coordinates 
                future_me = character(future_x, future_y, "", self.player.vel0, self.player.sprites)
                #finds the y-coordinate of the closes platform below
                getPlatformBelow(future_me, self.platforms)
                #if there is no platform below, then the AI would lose in this future
                if future_me.y0 == graphics.screen_height:
                        case_1 = False #if case 1 were true then AI would proceed without course correction

                #coeff for adding/subtracting velocity based on direction of AI
                if not self.platformEdge:
                        coeff = 1
                else:
                        coeff = -1
                #if future AI loses without doing anything, checks if jumping onto another platform is possible
                # to prevent that by checking if a future where the AI jumped forward/backward loses
                #Note that this check is intentionally left with wide margins of error,
                # so that the AI is not perfect at these predictions, similar to humans
                future_me = character(future_x + coeff*20*self.player.vel, future_y + 5*self.player.vel_y0, "",
                                      self.player.vel0, self.player.sprites)
                getPlatformBelow(future_me, self.platforms)
                #if the AI doesn't lose in this future, we want our current AI to jump to the new platform
                if future_me.y0 != graphics.screen_height:
                        if not case_1:
                                if self.player.vel < 0:
                                        vel_i = self.player.vel_y
                                        jump(self.player)
                                        if self.player.vel_y > vel_i:
                                                #the AI's jump is given more initial velocity
                                                # since the AI can't long press the jump key to
                                                # jump higher like a human player
                                                self.player.vel_y += 40
                                        moveLeft(self.player)
                                else:
                                        #mirrored case of above for other edge of platform
                                        vel_i = self.player.vel_y
                                        jump(self.player)
                                        if self.player.vel_y > vel_i: #i.e, if successfully jumped
                                                self.player.vel_y += 40
                                        moveRight(self.player)
                                self.platformEdge = False
                #if trying to jump to another platform still leads to death, walk away from edge
                elif not case_1:
                        if self.player.vel < 0:
                                moveRight(self.player)
                                self.platformEdge = True
                        else:
                                moveLeft(self.player)
                                self.platformEdge = True
                else:
                        self.platformEdge = False
                
        #called in the main loop
        def updateAI(self):
                self.attack()
                self.goTo()
                self.predictFuture()


##################################################################################################
#####FUNCTIONS####################################################################################
##################################################################################################


#These functions work as would be expected

#They change according to the following conditions:
                #If the stage is Ice, friction is de-activated

                #If the stage is Planet, friction and gravity are de-activated and radial gravity
                # is active. All movement functions have if conditions to switch from normal coordinates
                # to vector manipulations (through trig.) They almost always work with some form of
                #the formula that if v is a required vector, then vx = vcosangle and vy = vsinangle
                                        
def friction(player):
        if not (player.y < player.y0):
                if player.vel != 0:
                        sign = player.vel/ abs(player.vel)
                        player.vel -= sign*abs(player.vel)/5
                        if player.vel < 2 and player.vel > -2:
                                player.vel = 0

def gravity(player, y0):
        if player.y<y0:
                player.vel_y -= 10
        else:
                player.y = y0
                if player.sprite_state['jump']:
                        player.changeState('idle')
                player.vel_y = 0

def update_coords(players):
        for player in players:
                if not game_events.stage == "Planet":
                        player.x += player.vel
                        #if player is not on the ground:
                        if player.y - player.vel_y < player.y0:
                                player.y -= player.vel_y
                        else:
                                player.y = player.y0
                else: #special case for stage4 - rotating coords
                        player.rect.centerx += player.vel
                        player.rect.centery -= player.vel_y
                        player.x = player.rect.x
                        player.y = player.rect.y


def moveRight(player):
        if not game_events.stage == "Planet":
                if player.vel < player.vel0:
                        player.vel += 10
                player.changeState('run')
                player.direction = 1
        else:   #special case for stage4 - rotating coords
                if player.angle == 0:
                        if player.vel < player.vel0:
                                player.vel = 5
                        player.changeState('run')
                        player.direction = 1
                else:
                        player.vel0 = 20
                        player.vel = 1*player.vel0*cos(radians(player.angle))
                        player.vel_y = 1*player.vel0*sin(radians(player.angle))
                        player.changeState('run')
                        player.direction = 1

def moveLeft(player):
        if not game_events.stage == "Planet":
                if player.vel > -1*player.vel0:
                        player.vel -= 10
                player.changeState('run')
                player.direction = -1
        else:   #special case for stage4 - rotating coords
                if player.angle == 0:
                        if player.vel > -1*player.vel0:
                                player.vel -= 5
                        player.changeState('run')
                        player.direction = -1
                else:
                        player.vel0 = 20
                        player.vel = -1*player.vel0*cos(radians(player.angle))
                        player.vel_y = -1*player.vel0*sin(radians(player.angle))
                        player.changeState('run')
                        player.direction = -1

def jump(player):
        #if player is on the ground, jump
        if player.y == player.y0:
                #time is tracked to check if ninja is allowed to double jump
                player.jump_t1 = pygame.time.get_ticks()
                player.double_jumped = False
                player.btn_pressed_once = False
                player.vel_y = 40
                player.changeState('jump')
        #else, double jump if ninja, or ascend higher as others
        else:
                #this code enables ninja to double jump
                if not player.double_jumped and player.btn_pressed_once:
                        player.jump_t2 = pygame.time.get_ticks()
                        if player.jump_t2-player.jump_t1 > 100:
                                player.vel_y = 40
                                player.double_jumped = True
                else:   #special case for stage4 - rotating coords
                        if not game_events.stage == "Planet":
                                player.vel_y += 2*player.vel_y/5
                                if player.vel_y > 60:
                                        player.vel_y = 30
                        else:
                                if player.vel_y**2 + player.vel**2 < 500:
                                        player.vel_y += 30*cos(radians(player.angle))
                                        player.vel -= 30*sin(radians(player.angle))


#updates hitboxes with new x and y coords
def updateHitbox(players):
        for player in players:
                player.hitbox = (player.x, player.y, player.width, player.height)

#blits player to screen. #blit variable is used to handle knight turning invisible
def updateScreen(player, blit = True):
 #determine player state to pick correct sprites
         state = ""
         for key in player.sprite_state:
                 if player.sprite_state[key]:
                         state = key

         player.image = player.sprites[state][player.costume_count%10]
         if player.direction == -1:
                 player.image = pygame.transform.flip(player.image, True, False)
         #for stage 4, rotates to be along the direction of gravity
         player.image = pygame.transform.rotate(player.image, player.angle) 
         player.mask = pygame.mask.from_surface(player.image) #updates mask and rect to latest image
         player.rect = player.image.get_rect()
         player.rect.x = player.x
         player.rect.y = player.y
         if blit: #Knight invisibility
                 win.blit(player.image, (player.x, player.y))
         player.costume_count += 1

#executes the inputes, similar to tokenize from past homework
def update_inputs(inputs, player, circle = ""):
        if inputs == ["left"]:
                if circle: #special case for stage4 - rotating coords
                        if onPlanet(player, circle):
                                moveLeft(player)
                else:
                        moveLeft(player)

        if inputs == ["right"]:
                if circle: #special case for stage4 - rotating coords
                        if onPlanet(player, circle):
                                moveRight(player)
                else:
                        moveRight(player)

        if inputs == ["up"] or inputs == ["left", "up"] or inputs == ["right", "up"] or inputs == ["left", "right", "up"]:
                if not (player.sprite_state['side_melee'] or player.sprite_state['n_melee']):
                        if circle:
                                if onPlanet(player, circle):
                                        jump(player)
                        else:
                                jump(player)

        if inputs == ["right", "p"]:
                player.direction = 1
                player.changeState('side_melee')

        if inputs == ["left", "p"]:
                player.direction = -1
                player.changeState('side_melee')

        if inputs == ["p"]:
                player.changeState('n_melee')

#deals with collisions and damage. Momentum changes per attack is proportional to damage taken.
def updateHits(player1, player2):
        hitbox = pygame.Rect(player1.hitbox)
        if hitbox.colliderect(player2.hitbox):
                #neutral attacks
                if player1.sprite_state['n_melee']:
                        if player1.costume_count%10 > 7:
                                player2.health -= 10
                                damage_multiplier = (150 - player2.health)/(4*2**(player2.health/100))
                                if player2.health < 0:
                                        player2.health = 0
                                        damage_multiplier = 2*damage_multiplier
                                        
                                player2.vel = 2*player1.direction*damage_multiplier
                                player2.vel_y = 2*damage_multiplier
                #side attacks
                elif player1.sprite_state['side_melee']:
                        if player1.costume_count%10 > 7:
                                player2.health -= 5
                                damage_multiplier = (150 - player2.health)/(4*2**(player2.health/100))
                                if player2.health < 0:
                                        player2.health = 0
                                        damage_multiplier = 2*damage_multiplier
                                
                                player2.vel = 3*player1.direction*damage_multiplier
                                player2.vel_y = 1*damage_multiplier

                #projectile attacks
                elif player1.name == 'projectile':
                        player2.health -= 2
                        if player2.health <= 0:
                                player2.health = 0
                        player2.vel += 2*player1.vel/abs(player1.vel)
                        return True
        #checks for projectiles recursively
        if player1.projectiles:
                removals = []
                for i in range(len(player1.projectiles)):
                        isHit = updateHits(player1.projectiles[i], player2)
                        if isHit:
                                removals += [i]
                        #also going to remove any projectiles off the screen
                        elif (player1.projectiles[i].x > graphics.screen_width 
                                or player1.projectiles[i].x < 0):
                                removals += [i]
                removals.reverse()
                for index in removals:
                        del player1.projectiles[index]



#determines y0 (where a player can stand)
def getPlatformBelow(player, platforms):
        hitbox = pygame.Rect(player.hitbox)
        player.y0 = graphics.screen_height
        true_platform = ()
        for platform in platforms:
                if hitbox.colliderect(platform.hitbox[0], 0, platform.hitbox[2], graphics.screen_height):
                        if player.y <= platform.hitbox[1] - player.height:
                                if (platform.hitbox[1] - player.height - player.y) <= (player.y0 - player.y):
                                        player.y0 = platform.hitbox[1] - player.height
                                        true_platform =  platform
        return true_platform

#loading screen
def loading(win):
        if game_events.loading:
                text = 'Loading'
                myfont = pygame.font.SysFont('Lato', 40)
                textsurface = myfont.render(text, False, (255, 255, 255))
                x0 = win.get_width()/2 - textsurface.get_width()/2
                if game_events.loading_count//15%5==1:
                        text = "Loading"
                if game_events.loading_count//15%5 == 2:
                        text = "Loading."
                if game_events.loading_count//15%5 == 3:
                        text = "Loading.."
                if game_events.loading_count//15%5 == 4:
                        text = "Loading..."
                textsurface = myfont.render(text, False, (255, 255, 255))
                win.blit(graphics.loading_bg, (0,0))
                if game_events.loading_count < (win.get_width()/5):
                        pygame.draw.rect(win, (255,255,255), (win.get_width()*2/5-2, win.get_height()*2/3-2, win.get_width()/5+2 , 17), 1)              
                        pygame.draw.rect(win, (0,255,0), (win.get_width()*2/5, win.get_height()*2/3, game_events.loading_count, 15))
                        win.blit(textsurface, (x0,win.get_height()*1.3/3-2))
                else:
                        game_events.loading = False
                        game_events.main_screen = True

                game_events.loading_count+=5

#deactivates and reactivates a button at time intervals to prevent multiple clicks 
def buttonActive(t1, t2):
        t2 = pygame.time.get_ticks()
        if t2 - t1 > 200 and pygame.mouse.get_pressed()[0]:
                t1 = t2
                return (t1, t2, True)
        return (t1, t2, False)

#makes the stage chosen by the user
def makeStage():
        #this looks big, but it's just an elaborate way of specifying where each platform should be in each stage
        if game_events.stage == "Wormholes": #For Stage 1
                platform1 = makePlatform(graphics.screen_width/10,
                     graphics.screen_height*4/5,
                     graphics.platform_wh.get_width(),
                     graphics.platform_wh.get_height())

                platform2 = makePlatform(graphics.screen_width/10 - graphics.platform2_wh.get_width()/2,
                     graphics.screen_height*2.5/5,
                     graphics.platform2_wh.get_width(),
                     graphics.platform2_wh.get_height())

                platform3 = makePlatform(graphics.screen_width*8/10,
                     graphics.screen_height*2.5/5,
                     graphics.platform3_wh.get_width(),
                     graphics.platform3_wh.get_height())


                platforms = [platform1, platform2, platform3]
                graphics.platforms = graphics.platforms_wh

                graphics.game_bg = graphics.game_bg_wormholes
 
        if game_events.stage == "Ice": #For Stage 2
                platform1 = makePlatform(graphics.screen_width/5,
                     graphics.screen_height*4/5,
                     graphics.platform_ice.get_width(),
                     graphics.platform_ice.get_height())

                platform2 = makePlatform(platform1.x + platform1.width/2 - graphics.platform2_ice.get_width()/2,
                                     platform1.y - graphics.platform2_ice.get_height()/1.5,
                                     graphics.platform2_ice.get_width(),
                                     graphics.platform2_ice.get_height())

                platform3 = makePlatform(platform1.x + platform1.width/2 - graphics.platform3_ice.get_width()/2,
                                     platform2.y - graphics.platform3_ice.get_height()/1.5,
                                     graphics.platform3_ice.get_width(),
                                     graphics.platform3_ice.get_height())

                platform4 = makePlatform(platform1.x + platform1.width/2 - graphics.platform4_ice.get_width()/2,
                                     platform3.y - graphics.platform4_ice.get_height()/1.5,
                                     graphics.platform4_ice.get_width(),
                                     graphics.platform4_ice.get_height()) 

                platform5 = makePlatform(platform1.x + platform1.width/2 - graphics.platform5_ice.get_width()/2,
                                     platform4.y - graphics.platform5_ice.get_height()/1.5,
                                     graphics.platform5_ice.get_width(),
                                     graphics.platform5_ice.get_height()) 

                graphics.platforms = graphics.platforms_ice
                graphics.game_bg = graphics.game_bg_ice

                platforms = [platform1, platform2, platform3, platform4, platform5]

        if game_events.stage == "Clouds": #For Stage 3
                y = random.randint(int(4*graphics.screen_height/6), graphics.screen_height - graphics.platform_cld.get_height())
                platform1 = makePlatform(graphics.screen_width/8,
                            y,
                            graphics.platform_cld.get_width(),
                            graphics.platform_cld.get_height())

                y = random.randint(int(4*graphics.screen_height/6), graphics.screen_height - graphics.platform_cld.get_height())
                platform2 = makePlatform(2*graphics.screen_width/8,
                            y,
                            graphics.platform2_cld.get_width(),
                            graphics.platform2_cld.get_height())

                y = random.randint(int(4*graphics.screen_height/6), graphics.screen_height - graphics.platform_cld.get_height())
                platform3 = makePlatform(3*graphics.screen_width/8,
                            y,
                            graphics.platform3_cld.get_width(),
                            graphics.platform3_cld.get_height())

                y = random.randint(int(4*graphics.screen_height/6), graphics.screen_height - graphics.platform_cld.get_height())
                platform4 = makePlatform(4*graphics.screen_width/8,
                            y,
                            graphics.platform4_cld.get_width(),
                            graphics.platform4_cld.get_height())

                y = random.randint(int(4*graphics.screen_height/6), graphics.screen_height - graphics.platform_cld.get_height())
                platform5 = makePlatform(5*graphics.screen_width/8,
                            y,
                            graphics.platform4_cld.get_width(),
                            graphics.platform4_cld.get_height())

                y = random.randint(int(4*graphics.screen_height/6), graphics.screen_height - graphics.platform_cld.get_height())
                platform6 = makePlatform(6*graphics.screen_width/8,
                            y,
                            graphics.platform4_cld.get_width(),
                            graphics.platform4_cld.get_height())
                
                platforms = [platform1, platform2, platform3, platform4, platform5, platform6]
                graphics.platforms = graphics.platforms_cld
                graphics.game_bg = graphics.game_bg_ice

        if game_events.stage == "Planet": #For Stage 4
                platforms = []
                graphics.platforms = []
                graphics.game_bg = graphics.game_bg_wormholes

        return platforms

#Moves the clouds in stage 4, and loops across the screen
def moveClouds(platforms):
        
        for i in range(len(platforms)):
                platforms[i].x -= 5
                if platforms[i].x + platforms[i].width/2 <= 0:
                        platforms[i].x = graphics.screen_width
                        if i - 1 >= 0:
                                platforms[i].y = random.randint(max(0,int(platforms[i-1].y/2)), int(graphics.screen_height*5/6))
                        else:
                                platforms[i].y = random.randint(max(0,int(platforms[len(platforms)-1].y/2)), int(graphics.screen_height*5/6))
#A boolean check for stage 4
def onPlanet(player, circle):
        circle.mask = pygame.mask.from_surface(circle.image)
        circle.rect = circle.image.get_rect()
        circle.rect.center = (circle.x, circle.y)
        offset_x = player.rect[0] - circle.rect[0]
        offset_y = player.rect[1] - circle.rect[1]
        # See if the two masks at the offset are overlapping.
        overlap = circle.mask.overlap(player.mask, (offset_x, offset_y))
        return overlap

#radial gravity for stage 4
def radialGravity(player, circle1, circle2):

        #uses slope of line joining circle and player to calculate angle

        (x, y) = player.rect.center


        c1x = circle1.center[0]
        c1y = circle1.center[1]

        c2x = circle2.center[0]
        c2y = circle2.center[1]

        if x - c1x!=0:
                slope1 = (y - c1y)/(x - c1x)
                angle1 = atan(slope1)
        else:
                angle1 = 90

        if x - c2x!=0:
                slope2 = (y - c2y)/(x - c2x)
                angle2 = atan(slope2)
        else:
                angle2 = 90

        distance1 = ((y - c1y)**2 + (x - c1x)**2)**0.5
        distance2 = ((y - c2y)**2 + (x - c2x)**2)**0.5

        #compares distances from each planet to determine which gravity is stronger
        if distance1<distance2:
                angle = angle1
        else:
                angle = angle2

        if (angle == angle1 and x - c1x > 0) or (angle == angle2 and x - c2x > 0):
                player.angle = 180 + 90 - degrees(angle)
        else:
                player.angle = 90 - degrees(angle)

        if angle == angle1:
                center = [c1x, c1y]
                circle = circle1
                distance = distance1
        else:
                center = [c2x, c2y]
                circle = circle2
                distance = distance2

        #set of actions if player is on a planet
        if onPlanet(player, circle1) or onPlanet(player, circle2):

                #a restoring force that makes the planet bouncy
                if player.vel > 5:
                        player.vel -= 5
                elif player.vel < -5:
                        player.vel += 5
                else: 
                        player.vel = 0

                if player.vel_y > 5:
                        player.vel_y -= 5
                elif player.vel_y < -5:
                        player.vel_y += 5
                else: 
                        player.vel_y = 0

                if x > center[0]:
                        player.vel += 10*cos(angle)*circle.radius/distance
                elif x < center[0]:
                        player.vel -= 10*cos(angle)*circle.radius/distance

                #if player is not on planet, vertically, accelerate vertically
                if y > center[1]:
                        player.vel_y -= 10*abs(sin(angle))*circle.radius/distance
                elif y < center[1]:
                        player.vel_y += 10*abs(sin(angle))*circle.radius/distance
        
        else:
                #if player is not on planet, horizontally, accelerate horizontally

                if x > center[0]:
                        player.vel -= 5*cos(angle)*circle.radius/distance
                elif x < center[0]:
                        player.vel += 5*cos(angle)*circle.radius/distance

                #if player is not on planet, vertically, accelerate vertically
                if y > center[1]:
                        player.vel_y += 5*abs(sin(angle))*circle.radius/distance
                elif y < center[1]:
                        player.vel_y -= 5*abs(sin(angle))*circle.radius/distance
                
                #arctan has range [-90,90] so this helps correct that

#used to resize image to background size of window
def resizeBackground():
        
        width_ratio = graphics.screen_width/graphics.game_bg[0].get_width()
        height_ratio = graphics.screen_height/graphics.game_bg[0].get_height()

        if width_ratio < height_ratio:
                for i in range(len(graphics.game_bg)):
                        graphics.game_bg[i] = pygame.transform.rotozoom(graphics.game_bg[i], 0, width_ratio)
                        graphics.game_bg[i] = graphics.game_bg[i].convert_alpha()
        else:
                for i in range(len(graphics.game_bg)):
                        graphics.game_bg[i] = pygame.transform.rotozoom(graphics.game_bg[i], 0, height_ratio)
                        graphics.game_bg[i] = graphics.game_bg[i].convert_alpha()




        


#################################################################################################
#Initialization##################################################################################

#load window
win = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  

(graphics.screen_width, graphics.screen_height) = (win.get_width(), win.get_height())           



#####LOAD MUSIC########
music = "./sprites/spider_dance.mp3"
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)




graphics.ice_bg = graphics.ice_bg.convert_alpha()

portal1 = portal(500,500)
portal2 =  portal(1000,400)
portal_angle = 0

spriteUpdater = 0 #for character screen animation
time_stamp1 = 0 #used to keep track of time intervals
time_stamp2 = 0


#Game loop###################################################################################
#############################################################################################



run = True
while run:
        pygame.time.delay(35)

        for event in pygame.event.get():
                
                #loop exit
                if event.type == pygame.QUIT:
                        run = False
                        break
#############################################################################################

#Lots of Menu screens code that are big to look at but only because of precision requirements for
# layouts. There is no major logic to analyse.

        #make loading screen
        loading(win)

        #switch to menu after loading
        if game_events.main_screen:
                win.blit(graphics.main_bg, (0,0))
                myfont = pygame.font.SysFont('Lato', 40)
                textsurface1 = myfont.render('Start Game', False, (255, 255, 255))
                textsurface2 = myfont.render('Guide', False, (255, 255, 255))
                textsurface3 = myfont.render('Quit Game', False, (255, 255, 255))

                texts = [textsurface1, textsurface2, textsurface3]
                commands = ["game", "guide", "quit"]

                #making buttons
                (time_stamp1, time_stamp2, activeButton) = buttonActive(time_stamp1, time_stamp2)
                for i in range(len(texts)):
                
                        x0 = win.get_width()*3//4
                        y0 = win.get_height()//5
                        y = y0*(i+1)

                        textborder = (x0-10, y-10, texts[i].get_width()+20, texts[i].get_height()+20)

                        (mx, my) = pygame.mouse.get_pos()
                        if mx > x0 and mx < x0+texts[i].get_width() and my > y and my < y+texts[i].get_height():
                                pygame.draw.rect(win, (255, 255, 255), textborder, 2)
                                if pygame.mouse.get_pressed()[0] and activeButton:
                                        if commands[i] == "quit":
                                                run = False
                                                break
                                        if commands[i] == "game":
                                                game_events.gamemode_screen = True
                                                game_events.main_screen = False
                                        if commands[i] == "guide":
                                                game_events.guide_screen = True
                                                game_events.main_screen = False

                        win.blit(texts[i], (x0, (i+1)*y0))

        #switch between menu and guide screen
        if game_events.guide_screen:
                win.blit(graphics.guide_bg, (0,0))

                myfont = pygame.font.SysFont('Lato', 40)
                text = myfont.render('Okay', False, (255, 255, 255))
                text_rect = text.get_rect()
                (text_rect.x, text_rect.y) = (graphics.screen_width*7/10, graphics.screen_height*8/10)
                win.blit(text, (text_rect.x, text_rect.y))
                
                (mx, my) = pygame.mouse.get_pos()
                if text_rect.collidepoint((mx, my)):
                        pygame.draw.rect(win, (255, 255, 255), (text_rect[0] - 50, text_rect[1] - 30, text_rect[2] + 100, text_rect[3] + 60), 2)
                        if pygame.mouse.get_pressed()[0]:
                                game_events.main_screen = True
                                game_events.guide_screen = False

########################################################################################################################################################
        #AI or Player v Player
        if game_events.gamemode_screen:
                win.blit(graphics.main_bg, (0,0))
                myfont = pygame.font.SysFont('Lato', 40)
                textsurface1 = myfont.render('vs AI', False, (255, 255, 255))
                textsurface2 = myfont.render('vs Player', False, (255, 255, 255))

                texts = [textsurface1, textsurface2]
                commands = ["AI", "Player"]

                #making buttons
                (time_stamp1, time_stamp2, activeButton) = buttonActive(time_stamp1, time_stamp2)
                for i in range(len(texts)):
                
                        x0 = win.get_width()*3//4
                        y0 = win.get_height()//5
                        y = y0*(i+1)

                        textborder = (x0-10, y-10, texts[i].get_width()+20, texts[i].get_height()+20)

                        (mx, my) = pygame.mouse.get_pos()
                        
                        if mx > x0 and mx < x0+texts[i].get_width() and my > y and my < y+texts[i].get_height():
                                pygame.draw.rect(win, (255, 255, 255), textborder, 2)
                                if pygame.mouse.get_pressed()[0] and activeButton:
                                        if commands[i] == "AI":
                                                game_events.game_mode = "AI"
                                                game_events.char_screen = True
                                                game_events.gamemode_screen = False
                                        if commands[i] == "Player":
                                                game_events.game_mode = "Offline"
                                                game_events.char_screen = True
                                                game_events.gamemode_screen = False


                        win.blit(texts[i], (x0, (i+1)*y0))
########################################################################################################################################################
        #Chooses Characters here
        if game_events.char_screen:
                win.blit(graphics.loading_bg, (0,0))
                graphics.char_bg_rect.center = (graphics.screen_width/4, 3*graphics.screen_height/5)

                win.blit(graphics.char_bg, (graphics.char_bg_rect.x, graphics.char_bg_rect.y))
                win.blit(graphics.char_bg, (graphics.char_bg_rect.x + graphics.screen_width/6, graphics.char_bg_rect.y))
                win.blit(graphics.char_bg, (graphics.char_bg_rect.x +  2*graphics.screen_width/6, graphics.char_bg_rect.y))
                win.blit(graphics.char_bg, (graphics.char_bg_rect.x + 3*graphics.screen_width/6, graphics.char_bg_rect.y))

                char_initialx = graphics.char_bg_rect.centerx - graphics.character1['idle'][0].get_width()/2
                char_initialy = graphics.char_bg_rect.centery
                win.blit(graphics.character1['idle'][spriteUpdater%10], (char_initialx, char_initialy))
                win.blit(graphics.character2['idle'][spriteUpdater%10], (char_initialx + graphics.screen_width/6, char_initialy))
                win.blit(graphics.character3['idle'][spriteUpdater%10], (char_initialx + 2*graphics.screen_width/6, char_initialy))
                win.blit(graphics.character4['idle'][spriteUpdater%10], (char_initialx + 3*graphics.screen_width/6, char_initialy))
                spriteUpdater += 1

                myfont = pygame.font.SysFont('Lato', 40)
                text1 = myfont.render('Ninja', False, (255, 255, 255))
                text2 = myfont.render('Knight', False, (255, 255, 255))
                text3 = myfont.render('Rob', False, (255, 255, 255))
                text4 = myfont.render('Kunoichi', False, (255, 255, 255))

                textCommand1 = myfont.render('Choose Player 1!', False, (255, 255, 255))
                textCommand2 = myfont.render('Choose Player 2!', False, (255, 255, 255))

                text_y = char_initialy - graphics.char_bg.get_height()/3
                win.blit(text1, (char_initialx, text_y))
                win.blit(text2, (char_initialx + graphics.screen_width/6, text_y))
                win.blit(text3, (char_initialx + 2*graphics.screen_width/6, text_y))
                win.blit(text4, (char_initialx + 2.9*graphics.screen_width/6, text_y))

                character_rects = ['a','b','c','d']
                for i in range(4):
                        character_rects[i] = pygame.Rect(graphics.char_bg_rect[0] + i*graphics.screen_width/6,
                                                                         graphics.char_bg_rect[1],
                                                                         graphics.char_bg_rect[2],
                                                                         graphics.char_bg_rect[3])

                (mx, my) = pygame.mouse.get_pos()
                names = ["Ninja", "Knight", "Rob", "Kunoichi"]
                (time_stamp1, time_stamp2, activeButton) = buttonActive(time_stamp1, time_stamp2)
                for i in range(len(character_rects)):
                        if character_rects[i].collidepoint((mx, my)):
                                pygame.draw.rect(win, (255,255,255), character_rects[i], 5)
                                if pygame.mouse.get_pressed()[0] and activeButton:
                                        if not game_events.player1:
                                                game_events.player1 = names[i]
                                        elif not game_events.player2:
                                                game_events.player2 = names[i]

                if not game_events.player1:
                        win.blit(textCommand1, (graphics.screen_width/5, graphics.screen_height/5))
                elif not game_events.player2:
                        win.blit(textCommand2, (graphics.screen_width/5, graphics.screen_height/5))
                else:   #initializes players for the game
                        player1 = character(graphics.screen_width*3.5/5, graphics.screen_height*2/5, "Player 1", 30, graphics.characters[game_events.player1])
                        player2 = character(graphics.screen_width*2.5/5, graphics.screen_height*2/5, "Player 2", 30, graphics.characters[game_events.player2])

                        players = [player1,player2]

                        player1.direction = -1
                        if game_events.player1 == "Kunoichi":
                                player1.vel0 = 2*player1.vel0
                        if game_events.player2 == "Kunoichi":
                                player2.vel0 = 2*player2.vel0

                        game_events.stage_screen = True
                        game_events.char_screen = False
########################################################################################################################################################

        #Player chooses a screen
        if game_events.stage_screen:
                win.blit(graphics.loading_bg, (0,0))

                myfont = pygame.font.SysFont('Lato', 40)
                text1 = myfont.render('Choose your stage!', False, (255, 255, 255))
                win.blit(text1, (graphics.screen_width/3, graphics.screen_height/5))

                (x, y) = (graphics.screen_width/2, graphics.screen_height/3)

                if not game_events.game_mode == "AI":
                        for i in range(len(graphics.stage_icons)):
                                win.blit(graphics.stage_icons[i], (x/4.5 + i*graphics.screen_width/5, y))

                        stage_rects = ['a','b','c','d']
                        for i in range(4):
                                stage_rects[i] = pygame.Rect(x/4.5 + i*graphics.screen_width/5,
                                                                                 y,
                                                                                 graphics.stage_icons[i].get_width(),
                                                                                 graphics.stage_icons[i].get_height())
                else:
                        for i in range(len(graphics.stage_icons) - 1):
                                win.blit(graphics.stage_icons[i], (x/4.5 + i*graphics.screen_width/5, y))

                        stage_rects = ['a','b','c']
                        for i in range(3):
                                stage_rects[i] = pygame.Rect(x/4.5 + i*graphics.screen_width/5,
                                                                                 y,
                                                                                 graphics.stage_icons[i].get_width(),
                                                                                 graphics.stage_icons[i].get_height())

                (mx, my) = pygame.mouse.get_pos()
                names = ["Wormholes", "Ice", "Clouds", "Planet"]
                (time_stamp1, time_stamp2, activeButton) = buttonActive(time_stamp1, time_stamp2)
                for i in range(len(stage_rects)):
                        if character_rects[i].collidepoint((mx, my)):
                                pygame.draw.rect(win, (255,255,255), stage_rects[i], 5)
                                if pygame.mouse.get_pressed()[0] and activeButton:
                                        if not game_events.stage:
                                                game_events.stage = names[i]
                #initializes the stage
                if game_events.stage:
                        platforms = makeStage()
                        if game_events.stage == "Planet":
                                planet1 = planet(x = 2*graphics.screen_width/5, y = 1.2*graphics.screen_height/3, image = "./planet.png")
                                planet2 = planet(x = 3.5*graphics.screen_width/5, y = 1.8*graphics.screen_height/3, image = "./planet2.png")
                        resizeBackground()
                        player2AI = AI(player2, player1, platforms)
                        game_events.game = True
                        game_events.stage_screen = False
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
        ######### MAIN GAME ##########################
                        
        
        if game_events.game:

                if not game_events.stage == "Planet":
                        
                        if game_events.stage == "Clouds":
                                moveClouds(platforms)
                
                        updateHitbox(platforms)

                        getPlatformBelow(player1, platforms)
                        getPlatformBelow(player2, platforms)

                        gravity(player1, player1.y0)
                        gravity(player2, player2.y0)

                        if not game_events.stage == "Ice":
                                friction(player1)
                                friction(player2)
                        

                keys = pygame.key.get_pressed()
                inputs1 = []
                inputs2 = []

        ###################################################PLAYER 1 CONTROL#####################


                if keys[pygame.K_LEFT]:
                        inputs1 += ["left"]

                if keys[pygame.K_RIGHT]:
                        inputs1 += ["right"]

                else:
                        if not player1.sprite_state['jump']:
                                player1.changeState('idle')

                if keys[pygame.K_UP]:
                        inputs1 += ["up"]

                else:
                        if game_events.player1 == "Ninja":
                                player1.btn_pressed_once = True

                if keys[pygame.K_l]:
                        #makes projectiles by initializing them as non-controllable objects of class character
                        if game_events.player1 == "Rob":
                                if len(player1.projectiles)<=5:
                                        player1.projectiles += [character(player1.x + player1.width/2 + player1.direction*player1.width/4,
                                                                player1.y + player1.height/2, "projectile", 50, {'idle': graphics.p_attack}, 
                                                                vel_i = player1.direction*50)]

                if keys[pygame.K_p]:
                        inputs1 += ["p"]




        ####################################################PLAYER 2 CONTROL####################

                if keys[pygame.K_a]:
                        inputs2 += ["left"]

                if keys[pygame.K_d]:
                        inputs2 += ["right"]

                else:
                        if not player2.sprite_state['jump']:
                                player2.changeState('idle')

                if keys[pygame.K_w]:
                        inputs2 += ["up"]
                else:
                        if game_events.player2 == "Ninja":
                                player2.btn_pressed_once = True

                if keys[pygame.K_SPACE] and game_events.game_mode != "AI":
                        #same as above
                        if game_events.player2 == "Rob":
                                if len(player2.projectiles)<=5:
                                        player2.projectiles += [character(player2.x + player2.width/2 + player2.direction*player2.width/4,
                                                                player2.y + player2.height/2, "projectile", 50, {'idle': graphics.p_attack}, 
                                                                vel_i = player2.direction*50)]

                if keys[pygame.K_c]:
                        inputs2 += ["p"]


        ####################################################################################################

                #for abrupt game quits
                if keys[pygame.K_ESCAPE]:
                        run = False
                        break
                                
        ####################################################################################################

                #updating events
                
                if not game_events.stage == "Planet":
                        update_inputs(inputs1, player1)

                        if game_events.game_mode == "AI":
                                inputs2 = []
                                player2AI.updateAI()
                        if game_events.game_mode == "Offline":
                                update_inputs(inputs2, player2)
                else:
                        if game_events.game_mode == "Offline":
                                update_inputs(inputs1, player1, planet1)
                                update_inputs(inputs2, player2, planet1)
                                update_inputs(inputs1, player1, planet2)
                                update_inputs(inputs2, player2, planet2)

                        elif game_events.game_mode == "AI":
                                update_inputs(inputs1, player1, planet1)
                                update_inputs(inputs1, player1, planet2)
                                inputs2 = []
                                player2AI = AI(player2, player1, platforms)
                                player2AI.updateAI()


                updateHitbox(platforms)
                updateHitbox(players)
                updateHitbox(player1.projectiles)
                updateHitbox(player2.projectiles)

                updateHits(player1, player2)
                updateHits(player2, player1)

                update_coords(players)
                update_coords(player1.projectiles)
                update_coords(player2.projectiles)


        #updating display
                
                win.blit(graphics.game_bg[graphics.game_bg_count%graphics.game_bg_max], (0,0))
                graphics.game_bg_count += 1

                if game_events.stage == "Ice" or game_events.stage == "Clouds":
                        win.blit(graphics.ice_bg, (0,0))


                #platforms
                for i in range(len(platforms)):
                        j = len(platforms) - 1 - i
                        win.blit(graphics.platforms[j], (platforms[j].hitbox[0], platforms[j].hitbox[1]))
                        
                if game_events.stage == "Wormholes":
                        for platform in platforms:
                                pygame.draw.rect(win, (255,0,255), platform.hitbox, 10)

                ##########Generation and management of wormholes###########################################
                        #time loops from 0 to 20000 ms.
                        #t = 0 to 10000, portals are alive
                        #t = 10000 to 20000, no portals
                        #t = 20000, new portals are made and time loops
                        
                        portal1.t2 = pygame.time.get_ticks()

                        if portal1.t2 - portal1.t1 > 20000:
                                portal1.t1 = portal1.t2
                                x = graphics.screen_width
                                y = graphics.screen_height
                                portal1.rect.center = (random.randint(int(x/4), int(3*x/4)), random.randint(int(y/4), int(3*y/4)))
                                portal2.rect.center = (random.randint(int(x/4), int(3*x/4)), random.randint(int(y/4), int(3*y/4)))

                        if portal1.t2 - portal1.t1 < 10000:

                                portal_image = pygame.transform.rotozoom(graphics.portal, portal_angle, 1.5)
                                #portal angle is a helper to make its sprite rotate
                                portal_angle = (portal_angle + 15)
                                portal1_rect = portal_image.get_rect()
                                portal1_rect.center = portal1.rect.center
                                win.blit(portal_image, (portal1_rect.x, portal1_rect.y))

                                portal_image = pygame.transform.rotozoom(graphics.portal, portal_angle, 1.5)
                                portal_angle = (portal_angle + 15)
                                portal2_rect = portal_image.get_rect()
                                portal2_rect.center = portal2.rect.center
                                win.blit(portal_image, (portal2_rect.x, portal2_rect.y))

                                #objects that collide with centre of wormhole get teleported:
                                for player in players:
                                        player.portal_t2 = pygame.time.get_ticks()
                                        if player.portal_t2 - player.portal_t1 > 500:
                                                if player.rect.collidepoint(portal1_rect.center):
                                                        player.rect.center = portal2_rect.center
                                                        (player.x, player.y) = (player.rect.x, player.rect.y)
                                                        player.portal_t1 = pygame.time.get_ticks() 
                                                elif player.rect.collidepoint(portal2_rect.center):
                                                        player.rect.center = portal1_rect.center
                                                        (player.x, player.y) = (player.rect.x, player.rect.y) 
                                                        player.portal_t1 = pygame.time.get_ticks()

                                        for projectile in player.projectiles:
                                                projectile.portal_t2 = pygame.time.get_ticks()
                                                if projectile.portal_t2 - projectile.portal_t1 > 500:
                                                        if projectile.rect.collidepoint(portal1_rect.center):
                                                                projectile.rect.center = portal2_rect.center
                                                                (projectile.x, projectile.y) = (projectile.rect.x, projectile.rect.y)
                                                                projectile.portal_t1 = pygame.time.get_ticks() 
                                                        elif projectile.rect.collidepoint(portal2_rect.center):
                                                                projectile.rect.center = portal1_rect.center
                                                                (projectile.x, projectile.y) = (projectile.rect.x, projectile.rect.y) 
                                                                projectile.portal_t1 = pygame.time.get_ticks()

        ######################################################################################################################


                #Checks if knight should be invisible
                if game_events.player1 == "Knight" and keys[pygame.K_l]:
                        updateScreen(player1, blit = False)
                        player1.invisible = True
                else:
                        updateScreen(player1)
                        player1.invisible = False
                if game_events.player2 == "Knight" and keys[pygame.K_SPACE]:
                        updateScreen(player2, blit = False)
                        player2.invisible = True
                else:
                        updateScreen(player2)
                        player2.invisible = False

                #more blittings...
                for projectile in player1.projectiles:
                        win.blit(graphics.p_attack[4], (projectile.x, projectile.y))

                for projectile in player2.projectiles:
                        win.blit(graphics.p_attack[4], (projectile.x, projectile.y))

                if game_events.stage == "Planet":
                        radialGravity(player1, planet1, planet2)
                        radialGravity(player2, planet1, planet2)
                        win.blit(planet1.image, (planet1.rect[0], planet1.rect[1]))
                        win.blit(planet2.image, (planet2.rect[0], planet2.rect[1]))

                #healthbars
                h_coeff = graphics.healthbar_body.get_width()
                win.blit(pygame.transform.flip(graphics.healthbar_frame, True, False), (graphics.screen_width/10,graphics.screen_height/10))
                win.blit(pygame.transform.flip(graphics.healthbar_body, True, False), (graphics.screen_width/10,graphics.screen_height/10), (0, 0, 355*player2.health/100, 200))
                win.blit(graphics.healthbar_frame, (9*graphics.screen_width/10 - graphics.healthbar_frame.get_width(), graphics.screen_height/10))
                win.blit(pygame.transform.flip(graphics.healthbar_body, True, False), (9*graphics.screen_width/10 - 0.88*graphics.healthbar_frame.get_width(), graphics.screen_height/10), (0, 0, 355*player1.health/100, 200))

        
        #Checking for win/loss                
                if (player1.y >= graphics.screen_height 
                        or player1.x < -1*graphics.screen_width 
                        or player1.x > 2*graphics.screen_width):
                        
                        game_events.game = False
                        game_events.result = True
                        game_events.winner = player2.name

                if (player2.y >= graphics.screen_height 
                        or player2.x < -1*graphics.screen_width 
                        or player2.x > 2*graphics.screen_width):
                        game_events.game = False
                        game_events.result = True
                        game_events.winner = player1.name
                        
########################################################################################################################################################
########################################################################################################################################################
        #RESULTS AND RE-INITIALIZATION
                        
        #End of game and displaying results
        if game_events.result:
                #continue blitting bg
                win.blit(graphics.game_bg[graphics.game_bg_count%graphics.game_bg_max], (0,0))
                graphics.game_bg_count += 1
                #display result
                myfont = pygame.font.SysFont('Lato', 50)
                textsurface = myfont.render(game_events.winner+" won!", False, (255, 255, 255))
                text_rect = textsurface.get_rect()
                text_rect.center = (graphics.screen_width/2, graphics.screen_height/2)
                win.blit(textsurface, (text_rect.x, text_rect.y))
                #track time
                game_events.count += 1
                if game_events.count == 50:
                        #re-initialize everything
                        game_events.result = False
                        game_events.game = False
                        game_events.main_screen = True
                        game_events.count = 0
                        player1.x = player1.x0
                        player2.x = player2.x0
                        player1.y = graphics.screen_height*4/5 - 250
                        player2.y = graphics.screen_height*4/5 - 250
                        player1.vel = 0
                        player1.vel_y = 0
                        player2.vel = 0
                        player2.vel_y = 0
                        player1.direction = -1
                        player2.direction = 1
                        player1.health = 100
                        player2.health = 100
                        game_events.player1 = ""
                        game_events.player2 = ""
                        game_events.stage = ""


        pygame.display.update()
pygame.quit()
