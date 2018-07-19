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
from random import randint

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUOISE = (70, 142, 151)
DARK_TEAL = (46, 104, 111)
LIGHT_TEAL = (100, 201, 213)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.image.load("pixel_character.png").convert_alpha()
        self.game_over = False
        self.you_win = False
        self.can_change_image = True


        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
    
        self.score = 0
    
 
    def update(self):
        """ Move the player. """
        if self.rect.x > 10 and self.rect.y == (SCREEN_HEIGHT - self.rect.height - 50) and self.score != 8:
            self.game_over = True
            self.can_change_image = False
            if self.can_change_image == False:
                self.image = pygame.image.load("dead_character.png").convert_alpha()
        if self.score == 8:
            self.you_win = True
       

        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        # for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            # if self.change_x > 0:
            #     self.rect.right = block.rect.left
            # elif self.change_x < 0:
            #     # Otherwise if we are moving left, do the opposite.
            #     self.rect.left = block.rect.right
            
        coin_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, True)
        for coin in coin_hit_list:
            self.score = self.score + 1
 
        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)


        if self.change_y > 0:
            if self.can_change_image == True:
                self.image = pygame.image.load("falling_character.png").convert_alpha()

        for block in block_hit_list:
            # if self.change_x > 0:
            #     self.rect.right = block.rect.left
            # elif self.change_x < 0:
            #     # Otherwise if we are moving left, do the opposite.
            #     self.rect.left = block.rect.right
            # # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top

            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
            if self.can_change_image == True:
                self.image = pygame.image.load("pixel_character.png").convert_alpha()
        
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 2
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= (SCREEN_HEIGHT - self.rect.height - 50) and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = (SCREEN_HEIGHT - self.rect.height - 50)

    def jump(self):
        """ Called when user hits 'jump' button. """
        if self.can_change_image == True:
            self.image = pygame.image.load("pixel_jump.png").convert_alpha()

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        if self.can_change_image == True:
            self.image = pygame.image.load("pixel_character.png").convert_alpha()

 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        # self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("block.png").convert_alpha()
 
        self.rect = self.image.get_rect()

class Coin(pygame.sprite.Sprite):
    def __init__(self, width, height):
        
        super().__init__()

        self.image = pygame.image.load("dollar_bill.png").convert_alpha()
        
        self.rect = self.image.get_rect()

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
        self.world_shift = 0
 

    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        
        # # Draw all the sprite lists that we have
        if self.player.game_over == False:
            self.platform_list.draw(screen)
            self.coin_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for coin in self.coin_list:
            coin.rect.x += shift_x



# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)       
 
        # Array with width, height, x, and y of platform
        level = [[100, 50, 400, 500],
                 [100, 50, 700, 400],
                 [100, 50, 1100, 400],
                 [100, 50, 1500, 300],
                 [100, 50, 1700, 200],
                 [100, 50, 2000, 175],
                 [100, 50, 2300, 400],
                 [100, 50, 2500, 300]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # if pygame.sprite.collide_rect(player, last_block):       
        coins = [[40, 20, 425, 450],
                 [40, 20, 725, 350],
                 [40, 20, 1125, 350],
                 [40, 20, 1525, 250],
                 [40, 20, 1725, 150],
                 [40, 20, 2025, 125],
                 [40, 20, 2325, 350],
                 [40, 20, 2525, 250],
                 ]
                 
        for currency in coins:
            block = Coin(currency[0], currency[1])
            block.rect.x = currency[2]
            block.rect.y = currency[3]
            block.player = self.player
            self.coin_list.add(block)