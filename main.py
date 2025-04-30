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


def get_GAME_FIELD()->list:
    return [[get_color() for _ in range(ROWS)] for _ in range(COLS)]


GAME_FIELD = {
    'grid': []
}
BTNs = {
    'replay': None
}


def start_game()->None:
    GAME_FIELD['grid'] = get_GAME_FIELD()
    draw_squares()

    
def draw_btns()->None:
    replay_btn_img = pygame.image.load('btn_arrow_replay.svg')
    game_display.blit(replay_btn_img, (display_width/2, 10))
    BTNs['replay'] = replay_btn_img.get_rect(topleft=(10, display_width/2))
    

def draw_background()->None:
    background = pygame.image.load(bg_img).convert()
    game_display.fill(black)
    game_display.blit(background, (100, 182))
    
    draw_btns()


def replay(coord:tuple)->bool:
    if BTNs['replay'].collidepoint(coord[::-1]):
        start_game()
        return True
    
    return False


###################################################
def check_GAME_FIELD()->None:
    GAME_FIELD['grid'] = [col for col in GAME_FIELD['grid'] if col]


def draw_squares()->None:
    draw_background()

    for i, col in enumerate(GAME_FIELD['grid']):
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
    
    if col != len(GAME_FIELD['grid'])-1:
        if len(GAME_FIELD['grid'][col+1])-1>=row:
            nb.append((col+1, row))
        
    if col != 0:
        if len(GAME_FIELD['grid'][col-1])-1>=row:
            nb.append((col-1, row))
        
    if row != len(GAME_FIELD['grid'][col])-1:
        nb.append((col, row+1))
    if row != 0:
        nb.append((col, row-1))
    
    return check_clrs(root_clr, nb)


def check_clrs(clr:str, coords:list)->list:
    return [(col, row) for col, row in coords if clr==GAME_FIELD['grid'][col][row]]


def check_neighbours(coord:tuple)->list:
    figure = []
    col, row = coord
    try:
        clr = GAME_FIELD['grid'][col][row]
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


def delete_figure(figure:list)->None:
    for col, row in figure:
        GAME_FIELD['grid'][col][row] = 'black'

    for col, row in enumerate(GAME_FIELD['grid']):
        GAME_FIELD['grid'][col] = [elm for elm in row if elm != 'black']
    
    check_GAME_FIELD()
    
    draw_squares()
    
    am_I_win()

    
def am_I_win()->bool:
    if count_squares():
        return False
    print('Yes')
    return True
    

def count_squares()->int:
    return sum(len(row) for row in GAME_FIELD['grid'])
    
    
def game_loop(testing: bool=False)->None:
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not replay(event.pos):
                    figure = get_figure(event.pos)
                    if len(figure)>1:
                        delete_figure(figure)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('CLICKOMANIA')
    clock = pygame.time.Clock()
    
    start_game()
    
    game_loop()
    
    pygame.quit()
    quit()
