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

# ВОТ ЭТУ ХУЙНЮ ПЕРЕПИСАТЬ!!!
def make_it_black():
    if len(full_n) > 1:
        for i in range(len(full_n)):
            pygame.draw.rect(game_display, black, pygame.Rect(full_n[i][1]*SQUARE_SIZE,
                                                              (14-full_n[i][0])*SQUARE_SIZE,
                                                              SQUARE_SIZE, SQUARE_SIZE))

def check_neighbours(row, col):
    test = { 'left': True, 'right': True, 'top': True, 'bottom': True }
    if row == 0:
        test['bottom'] = False
    
    if row == len(GAME_FIELD) - 1:
        test['top'] = False
    
    if col == 0:
        test['left'] = False
    
    if col == len(GAME_FIELD[0]) - 1:
        test['right'] = False
        
    return test

def is_destructible(mouse_coord):
    col, row = grid_coord(mouse_coord)
    clean()
    n.append((row, col))
    gather_squares(row, col)

    return {}

def clean():
    global n
    global full_n
    n = []
    full_n = []

full_n = []
n = []

def gather_squares(row, col):
    neighbours_test = check_neighbours(row, col)
    
    full_n.append((row, col))
    n.remove((row, col))
    
    GF_ROW = len(GAME_FIELD)
    GF_COL = len(GAME_FIELD[0])
    
    if neighbours_test['right'] and (GAME_FIELD[row][col] == GAME_FIELD[row][col+1]) and (row, col+1) not in full_n:
        n.append((row, col+1))
    
    if neighbours_test['left'] and (GAME_FIELD[row][col] == GAME_FIELD[row][col-1]) and (row, col-1) not in full_n:
        n.append((row, col-1))
    
    if neighbours_test['top'] and (GAME_FIELD[row][col] == GAME_FIELD[row+1][col]) and (row+1, col) not in full_n:
        n.append((row+1, col))
    
    if neighbours_test['bottom'] and (GAME_FIELD[row][col] == GAME_FIELD[row-1][col]) and (row-1, col) not in full_n:
        n.append((row-1, col))
    
    if len(n) >= 1:
        gather_squares(n[0][0], n[0][1])

    return ''

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
                is_destructible(pygame.mouse.get_pos())
#                print(full_n)
                make_it_black()


        pygame.display.update()
        

game_loop()

pygame.quit()
quit()