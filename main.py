import pygame
import time
import random
import math

bg_img = 'prison_mike.jpg'

pygame.init()

display_width = 400
display_height = 600

black = (36, 52, 53)
white = (232, 245, 240)

red    = (249, 102, 56)
blue   = (48, 96, 249)
green  = (52, 206, 147)
yellow = (255, 204, 95)
brown  = (127, 113, 97)

COLORS = [red, blue, green, yellow, brown]
SQUARE_SIZE = 40

GAME_FIELD = []

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('CLICKOMANIA')
clock = pygame.time.Clock()

background = pygame.image.load(bg_img).convert()

def get_color():
    return COLORS[random.randint(0, len(COLORS) - 1)]

def draw_squares():    
    for j in range(1, 14):
        y = display_height - SQUARE_SIZE*j
        row = []
        for i in range(10):
            color = get_color()
            row.append(color)
            pygame.draw.rect(game_display, color, pygame.Rect(i*SQUARE_SIZE, y, SQUARE_SIZE, SQUARE_SIZE))

        GAME_FIELD.append(row)
    #pygame.display.flip()

def grid_coord(xy):
    x, y = xy
    return (math.ceil(x / SQUARE_SIZE) - 1, 15 - math.ceil(y / SQUARE_SIZE))

def is_destructible(mouse_coord):
    col, row = grid_coord(mouse_coord)
    check_neighbours = { 'left': True, 'right': True, 'top': True, 'bottom': True }
    
    if row == 0:
        check_neighbours['bottom'] = False
    
    if row == len(GAME_FIELD) - 1:
        check_neighbours['top'] = False
    
    if col == 0:
        check_neighbours['left'] = False
    
    if col == len(GAME_FIELD[0]) - 1:
        check_neighbours['right'] = False
    
    if check_neighbours['left']:
        if GAME_FIELD[row][col] == GAME_FIELD[row][col-1]:
            return True
        
    if check_neighbours['right']:
        if GAME_FIELD[row][col] == GAME_FIELD[row][col+1]:
            return True
    
    if check_neighbours['top']:
        if GAME_FIELD[row][col] == GAME_FIELD[row+1][col]:
            return True
    
    if check_neighbours['bottom']:
        if GAME_FIELD[row][col] == GAME_FIELD[row-1][col]:
            return True

    return False

game_display.fill(black)

game_display.blit(background, (100, 182))
draw_squares()

# print(len(GAME_FIELD))

def game_loop():	
    x = display_width * 0.45
    y = display_height * 0.8

    x_change = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(is_destructible(pygame.mouse.get_pos()))


        pygame.display.update()
        

game_loop()

pygame.quit()
quit()