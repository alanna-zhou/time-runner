"""
    This file contains classes that were inspired by Mr. Caven's tutorial.
    Sample Python/Pygame Programs
    Simpson College Computer Science
    http://programarcadegames.com/
    http://simpson.edu/computer-science/
    
    From:
    http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
    
    Explanation video: http://youtu.be/BCxWJgN4Nnc
    
    Part of a series:
    http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
    http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
    http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
    http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
    http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
    http://programarcadegames.com/python_examples/sprite_sheets/
    """

import pygame, sys
from pygame.locals import *
from player_obstacle_classes import Player
from player_obstacle_classes import Platform
from player_obstacle_classes import Level
from player_obstacle_classes import Level_01

pygame.init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
global play_game_button
global back_button


# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner Game")
SPEED = 4
myfont = pygame.font.Font(None, 15)


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUOISE = (70, 142, 151)
DARK_TEAL = (46, 104, 111)
LIGHT_TEAL = (100, 201, 213)


#global variable
play_pressed = False
back_pressed = False
menu_pressed = False
game_counter = 0

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

#this takes in the parameters from the main game loop and creates buttons. If "Play Game" button is pressed, it will set pressed to True
#which allows the game to start playing
class Button:
    global play_pressed
    global back_pressed
    global menu_pressed
    global mouse 
    def __init__(self, msg,x,y,width,height,u_color,s_color,text_size,center_x,center_y,action=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.u_color = u_color
        self.s_color = s_color
        self.text_size = text_size
        self.center_x = center_x
        self.center_y = center_y
        self.action = action
        mouse = pygame.mouse.get_pos()

        
        if play_pressed == False:
            click = pygame.mouse.get_pressed()

            if x+width > mouse[0] > x and y+height > mouse[1] > y:
                pygame.draw.rect(gameDisplay, u_color, [x, y, width, height])
                medText = pygame.font.Font(None, text_size)
                TextSurf, TextRect = text_objects(msg, medText)
                TextRect.center = (center_x, center_y)
                gameDisplay.blit(TextSurf, TextRect)
            else:
                pygame.draw.rect(gameDisplay, s_color, [x, y, width, height])
                medText = pygame.font.Font(None, text_size)
                TextSurf, TextRect = text_objects(msg, medText)
                TextRect.center = (center_x,center_y)
                gameDisplay.blit(TextSurf, TextRect) 



    def update(self):
        global play_pressed
        global back_pressed
        global menu_pressed
        global mouse 
        mouse = pygame.mouse.get_pos()
        if play_pressed == False:
            click = pygame.mouse.get_pressed()
            if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
                if click[0] == 1 and self.action!= None:
                    if self.action == "play":
                        play_pressed = True
                    elif self.action == "back":
                        back_pressed = True
                    elif self.action == 'menu':
                        menu_pressed = True


def level1():
    #Put the game code in here, but don't loop it. The game loop function is already in a loop down in the main game loop function
    #this function is just to display text. It's called in the button function     
    global play_pressed
    global game_counter 
    # Set background image
    scroller_x = SCREEN_WIDTH
    b1 = "pixel_background.jpg"
    back = pygame.image.load("pixel_background.jpg")
    back = pygame.transform.scale(back, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create the player
    player = Player()
    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
    # Create all coins
    coin_list = []
    # Create all sprites
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    # Place player
    player.rect.x = 0
    player.rect.y = (SCREEN_HEIGHT - player.rect.height - 50)
    active_sprite_list.add(player)
    while play_pressed == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if player.game_over == False:
                        player.go_right()
                if event.key == pygame.K_UP:
                    if player.game_over == False:
                        player.jump()  
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        gameDisplay.blit(back, (scroller_x, 0))
        gameDisplay.blit(back,(scroller_x - SCREEN_WIDTH, 0))
        if player.you_win == True:
            player.game_over = False
        elif player.game_over == True:
            player.you_win = False


        if player.you_win == True:
            game_counter = game_counter + 1
            gameDisplay.fill(BLACK)
            game_over_label = myfont.render("YOU WIN", 1, WHITE)
            gameDisplay.blit(game_over_label, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            score_label = myfont.render("Score: {0}".format(player.score), 1, WHITE)
            gameDisplay.blit(score_label, (665, 37))
            if game_counter > 100:
                game_counter = 0
                play_pressed = False
                main_game_loop()
        elif player.game_over == True:
            game_counter = game_counter + 1
            gameDisplay.fill(BLACK)
            game_over_label = myfont.render("GAME OVER", 1, WHITE)
            gameDisplay.blit(game_over_label, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            if game_counter > 100:
                game_counter = 0
                play_pressed = False
                main_game_loop()
        pygame.draw.rect(gameDisplay, WHITE, [650, 25, 125, 50])
        score_label = myfont.render("Score: {0}".format(player.score), 1, BLACK)
        gameDisplay.blit(score_label, (665, 37))

        scroller_x = scroller_x - SPEED
        if scroller_x == 0:
            scroller_x = SCREEN_WIDTH

        # Update the player.
        active_sprite_list.update()

        # Shift the world 
        if player.rect.right <= 1500:
            current_level.shift_world(- SPEED)
        else:
            current_level.shift_world(0)

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        if player.rect.left < 0:
            player.game_over = True


        current_level.draw(gameDisplay)
        active_sprite_list.draw(gameDisplay)

        pygame.display.flip()

        clock.tick(60)
    # Close the window and quit.
    pygame.quit()
    exit() # Needed when using IDLE


def menu():
    b1 = "menu_bg.jpg"   #these are the images I will use for the background
    back = pygame.image.load(b1).convert() #when used, this will load the images
    gameDisplay.blit(back, (0,0))      #this will blit the background image to a certain point on the screen

    pygame.draw.rect(gameDisplay, TURQUOISE, [200, 50, 400, 500])
    largeText = pygame.font.Font(None, 56)
    TextSurf, TextRect = text_objects("Time Runner", largeText)
    TextRect.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/4))
    gameDisplay.blit(TextSurf, TextRect)

    # calls the button function to display the buttons
    play_game_button = Button("Play Game", 220, 400, 355, 75, LIGHT_TEAL, DARK_TEAL, 46, 400, 440, "play")

    play_game_button.update()


def main_game_loop():
    intro = True
    pygame.mixer.music.load ("Crossroads.mid")
    pygame.mixer.music.play(-1,0.0)
    # pressed = False
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
       
        #updates screen
        pygame.display.update()

        if play_pressed == True:
            #game play starts
            level1()
        elif menu_pressed == True:
            menu()
        else:
            #general Menu BG and Title
            menu()


    # --- Limit to 60 frames per second
    clock.tick(60)
    pygame.display.flip()

main_game_loop()

# Close the window and quit.
pygame.quit()
exit() # Needed when using IDLE
