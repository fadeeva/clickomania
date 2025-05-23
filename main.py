import pygame
import random
import math


black  = (36, 52, 53)
white  = (232, 245, 240)


SCREEN = {
    'width' : 400,
    'height': 600,
}

SETTINGS = {
    'bg_clr'  : black,
    'caption' : 'CLICKOMANIA',
}

COLORS = {
    'red'   : (249, 102, 56),
    'blue'  : (48, 96, 249),
    'green' : (52, 206, 147),
    'yellow': (255, 204, 95),
    'brown' : (127, 113, 97),
}

SQUARE_SIZE = 40

ROWS = 13
COLS = 10

GAME_FIELD = {
    'grid': []
}

IMGs = {
    'replay_btn': pygame.image.load('btn_arrow_replay.svg'),
    'win_msg'   : pygame.image.load('win_message.svg'),
    'background': pygame.image.load('prison_mike.jpg'),
}

BTNs = {
    'replay': IMGs['replay_btn'].get_rect(topleft=(10, SCREEN['width']/2))
}


###################################################
def get_color()->list:
    return list(COLORS.keys())[random.randint(0, len(COLORS) - 1)]


def get_GAME_FIELD()->list:
    return [[get_color() for _ in range(ROWS)] for _ in range(COLS)]


def start_game()->None:
    GAME_FIELD['grid'] = get_GAME_FIELD()
    draw_squares()

    
def draw_btns()->None:
    game_display.blit(IMGs['replay_btn'], (SCREEN['width']/2, 10))
    

def draw_background()->None:
    game_display.fill(SETTINGS['bg_clr'])
    game_display.blit(IMGs['background'], (100, 182))
    
    draw_btns()


def replay(coord:tuple)->bool:
    if BTNs['replay'].collidepoint(coord[::-1]):
        start_game()
        return True
    
    return False


def show_win_message()->None:
    msg_width = SCREEN['width']/2-3*SQUARE_SIZE
    msg_height = 1.5*SQUARE_SIZE
    pygame.draw.rect(game_display, white,
                     pygame.Rect(msg_width, msg_height,
                                 6*SQUARE_SIZE, 3*SQUARE_SIZE))
    
    game_display.blit(IMGs['win_msg'], (msg_width+10, msg_height+10))


def am_I_win()->bool:
    squares_left = sum(len(row) for row in GAME_FIELD['grid'])
    
    return True if not squares_left else False

    
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
    if len(figure)<2:
        return
    
    for col, row in figure:
        GAME_FIELD['grid'][col][row] = 'black'

    for col, row in enumerate(GAME_FIELD['grid']):
        GAME_FIELD['grid'][col] = [elm for elm in row if elm != 'black']
    
    check_GAME_FIELD()
    draw_squares()


###################################################
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
                    delete_figure(figure)
                    if am_I_win(): show_win_message()

        pygame.display.update()
###################################################

if __name__ == '__main__':
    pygame.init()
    
    game_display = pygame.display.set_mode((SCREEN['width'],
                                            SCREEN['height']))
    pygame.display.set_caption(SETTINGS['caption'])
    clock = pygame.time.Clock()
    
    start_game()
    
    game_loop()
    
    pygame.quit()
    quit()
