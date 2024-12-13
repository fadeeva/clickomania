import pygame
import random
import math


bg_img = 'prison_mike.jpg'

display_width  = 400
display_height = 600

black  = (36, 52, 53)
white  = (232, 245, 240)

red    = (249, 102, 56)
blue   = (48, 96, 249)
green  = (52, 206, 147)
yellow = (255, 204, 95)
brown  = (127, 113, 97)

COLORS = {
    'red': red,
    'blue': blue,
    'green': green,
    'yellow': yellow,
    'brown': brown
}

SQUARE_SIZE = 40

ROWS = 13
COLS = 10


def get_color():
    return list(COLORS.keys())[random.randint(0, len(COLORS) - 1)]


GAME_FIELD = [[get_color() for _ in range(ROWS)] for _ in range(COLS)]


def draw_squares():
    for i, col in enumerate(GAME_FIELD):
        for j, clr in enumerate(col):
            pygame.draw.rect(game_display,
                             COLORS[clr],
                             pygame.Rect(i*SQUARE_SIZE, abs(j-14)*SQUARE_SIZE,
                                         SQUARE_SIZE, SQUARE_SIZE))


def grid_coord(xy):
    x, y = xy
    return (math.ceil(x / SQUARE_SIZE) - 1, 15 - math.ceil(y / SQUARE_SIZE))


def redraw_squares():
    # print(GAME_FIELD[12][9])
    for j in range(len(GAME_FIELD)):
        y = display_height - SQUARE_SIZE*j
        for i in range(len(GAME_FIELD[0])):
            if GAME_FIELD[j-1][i]:
                color = GAME_FIELD[j-1][i]
                pygame.draw.rect(game_display,
                                 color,
                                 pygame.Rect(i*SQUARE_SIZE,
                                             y,
                                             SQUARE_SIZE,
                                             SQUARE_SIZE))


def check_neighbours(row, col):
    test = {'left': True, 'right': True, 'top': True, 'bottom': True}
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
#    gather_squares(row, col)
    print(col, row)
    return {}


def clean():
    n.clear()
    full_n.clear()


full_n = []
n = []


def gather_squares(row, col):
    neighbours_test = check_neighbours(row, col)

    full_n.append((row, col))
    n.remove((row, col))

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


def game_loop(testing: bool=False):    
    
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_destructible(pygame.mouse.get_pos())
#                make_it_black()

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('CLICKOMANIA')
    clock = pygame.time.Clock()

    background = pygame.image.load(bg_img).convert()
    
    game_display.fill(black)

    game_display.blit(background, (100, 182))
    draw_squares()
    
    game_loop()
    
    pygame.quit()
    quit()
