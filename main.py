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


class GAME_FIELD():
    _ROWS = 13
    _COLS = 10
    def __init__(self):
        self.data = self.get_data()
    
    def _get_color(self)->list:
        return list(COLORS.keys())[random.randint(0, len(COLORS) - 1)]
    
    def get_data(self):
        return [[self._get_color() for _ in range(self._ROWS)] for _ in range(self._COLS)]


GAME_FIELD = GAME_FIELD().data

def check_GAME_FIELD()->None:
    global GAME_FIELD
    GAME_FIELD = [col for col in GAME_FIELD if col]


def draw_squares()->None:
    background = pygame.image.load(bg_img).convert()
    game_display.fill(black)
    game_display.blit(background, (100, 182))
    
    for i, col in enumerate(GAME_FIELD):
        for j, clr in enumerate(col):
            if clr == 'black': continue
            pygame.draw.rect(game_display,
                             COLORS[clr],
                             pygame.Rect(i*SQUARE_SIZE,
                                         abs(j-14)*SQUARE_SIZE,
                                         SQUARE_SIZE,
                                         SQUARE_SIZE))


def grid_coord(coord:tuple)->tuple:
    col, row = coord
    return (math.ceil(col / SQUARE_SIZE) - 1,
            15 - math.ceil(row / SQUARE_SIZE))


def get_all_neighbours(root_clr:str, coord:tuple)->list:
    col, row = coord
    nb = []
    
    if col != len(GAME_FIELD)-1:
        if len(GAME_FIELD[col+1])-1>=row:
            nb.append((col+1, row))
        
    if col != 0:
        if len(GAME_FIELD[col-1])-1>=row:
            nb.append((col-1, row))
        
    if row != len(GAME_FIELD[col])-1:
        nb.append((col, row+1))
    if row != 0:
        nb.append((col, row-1))
    
    return check_clrs(root_clr, nb)


def check_clrs(clr:str, coords:list)->list:
    return [(col, row) for col, row in coords if clr==GAME_FIELD[col][row]]


def check_neighbours(coord:tuple)->list:
    figure = []
    col, row = coord
    try:
        clr = GAME_FIELD[col][row]
    except:
        return []
    
    def search(coord:tuple)->list:
        if coord not in figure: figure.append(coord)
        nbs = get_all_neighbours(clr, coord)
        nbs = [coord for coord in nbs if coord not in figure]
        
        if not nbs:
            return figure
        else:
            for nb in nbs:
                search(nb)
    
        return figure
    
    return search(coord)
    

def get_figure(mouse_coord:tuple)->list:
    coord = grid_coord(mouse_coord)
    figure = check_neighbours(coord)
    
    return figure


def delete_figure(figure:list)->bool:
    for col, row in figure:
        GAME_FIELD[col][row] = 'black'

    for col, row in enumerate(GAME_FIELD):
        GAME_FIELD[col] = [elm for elm in row if elm != 'black']
    
    check_GAME_FIELD()
    
    draw_squares()
    
    return False


def game_loop(testing: bool=False)->None:
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                figure = get_figure(pygame.mouse.get_pos())
                if len(figure)>1:
                    delete_figure(figure)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('CLICKOMANIA')
    clock = pygame.time.Clock()

    draw_squares()
    
    game_loop()
    
    pygame.quit()
    quit()
