import pygame
import time
import random

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

    
game_display.fill(black)
draw_squares()

# print(GAME_FIELD[0][0])

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
				print(pygame.mouse.get_pos())
			
		#game_display.fill(white)
		
		pygame.display.update()
		clock.tick(60)

game_loop()

pygame.quit()
quit()