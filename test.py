
"""
http://pastebin.com/VW9maqHf
"""

import pygame
import time

pygame.init()

display_width = 800
display_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

player_1_start_location = (display_width-100, display_height-100)
player_1_current_location = player_1_start_location

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('title')
clock = pygame.time.Clock()

backgroundImg = pygame.image.load('board-800.jpg')
player1_img = pygame.image.load('man1.png')

backgroundImg = pygame.transform.scale(backgroundImg, (display_width, display_height))
player1_img = pygame.transform.scale(player1_img, (int(display_width*0.1), int(display_height*0.1)))

game_display.fill(white)
game_display.blit(backgroundImg, (0, 0))
game_display.blit(player1_img, player_1_start_location)

crashed = False
x_change = 0

def repaint_background():
    game_display.fill(white)
    game_display.blit(backgroundImg, (0, 0))

def display_player(x, y):
    global player_1_current_location
    repaint_background()
    temp = (player_1_current_location[0]-x, player_1_current_location[1]-y)
    if temp[0] < 15 or temp[0] > display_width-50 or temp[1] < 100 or temp[1] > display_height-50:
        return

    player_1_current_location = temp
    game_display.blit(player1_img, player_1_current_location)

def draw_vertical_line(x):
    pygame.draw.line(game_display, black, (x,0), (x,1000))

def draw_horizontal_line(y):
    pygame.draw.line(game_display, black, (0,y), (1000,y))

def text_objects(msg, fontobj, color=black):
    text_surf = fontobj.render(msg, True, color)
    return text_surf, text_surf.get_rect()

def message_display(msg):
    large_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surf, text_rect = text_objects(msg, large_text)
    text_rect.center = (display_width/2, display_height/2)
    game_display.blit(text_surf, text_rect)

for i in range(0, 1000, 100):
    draw_vertical_line(i)
    draw_horizontal_line(i)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # print event

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_change = -70
            elif event.key == pygame.K_LEFT:
                x_change = 70
            display_player(x_change, 0)
            message_display("wheeeeee")

    pygame.display.update() #only changed
    #pygame.display.flip() #entire

    clock.tick(30) # 30 fps

pygame.quit()
quit()
