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


def get_color()->list:
    return list(COLORS.keys())[random.randint(0, len(COLORS) - 1)]


GAME_FIELD = [[get_color() for _ in range(ROWS)] for _ in range(COLS)]


def draw_squares()->None:
    for i, col in enumerate(GAME_FIELD):
        for j, clr in enumerate(col):
            pygame.draw.rect(game_display,
                             COLORS[clr],
                             pygame.Rect(i*SQUARE_SIZE,
                                         abs(j-14)*SQUARE_SIZE,
                                         SQUARE_SIZE,
                                         SQUARE_SIZE))


def grid_coord(xy:tuple)->tuple:
    x, y = xy
    return (math.ceil(x / SQUARE_SIZE) - 1,
            15 - math.ceil(y / SQUARE_SIZE))


def get_all_neighbours(col:int, row:int)->list:
    return [(0, 0)]


def check_neighbours(col:int, row:int)->list:
    nb = []
    nb.append((col, row))
    current_clr = GAME_FIELD[col][row]
    
    for col, row in nb:
        nbs_coords = get_all_neighbours(col, row)
        
        for col_nb, row_nb in nbs_coords:
            if GAME_FIELD[col_nb][row_nb] == current_clr and (col_nb, row_nb) not in nb:
                nb.append((col_nb, row_nb))
    
    return nb


def is_destructible(mouse_coord:tuple)->bool:
    col, row = grid_coord(mouse_coord)
    print(check_neighbours(col, row))
    
    return False


def game_loop(testing: bool=False)->None:
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_destructible(pygame.mouse.get_pos())

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
