import pygame, sys
from pygame.locals import *
from player_obstacle_classes import Player
from player_obstacle_classes import Platform
from player_obstacle_classes import Level
from player_obstacle_classes import Level_01

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 4
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
x = SCREEN_WIDTH
myfont = pygame.font.SysFont(None, 15)


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUOISE = (70, 142, 151)
DARK_TEAL = (46, 104, 111)
LIGHT_TEAL = (100, 201, 213)
 
# Set background image
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

while True:
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

    screen.blit(back, (x, 0))
    screen.blit(back,(x - SCREEN_WIDTH, 0))

    if player.you_win == True:
        player.game_over = False
    elif player.game_over == True:
        player.you_win = False

    if player.you_win == True:
        screen.fill(BLACK)
        game_over_label = myfont.render("YOU WIN", 1, WHITE)
        screen.blit(game_over_label, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        score_label = myfont.render("Score: {0}".format(player.score), 1, WHITE)
        screen.blit(score_label, (665, 37))
    elif player.game_over == True:
        screen.fill(BLACK)
        game_over_label = myfont.render("GAME OVER", 1, WHITE)
        screen.blit(game_over_label, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    

    pygame.draw.rect(screen, WHITE, [650, 25, 125, 50])
    score_label = myfont.render("Score: {0}".format(player.score), 1, BLACK)
    screen.blit(score_label, (665, 37))

    x = x - SPEED
    if x == 0:
        x = SCREEN_WIDTH

    # Update the player.
    active_sprite_list.update()

    # Shift the world 
    if player.rect.right <= 800:
        current_level.shift_world(- SPEED)
    else:
        current_level.shift_world(0)

    # If the player gets near the right side, shift the world left (-x)
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    if player.rect.left < 0:
        player.game_over = True


    current_level.draw(screen)
    active_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)
# Close the window and quit.
pygame.quit()
exit() # Needed when using IDLE
