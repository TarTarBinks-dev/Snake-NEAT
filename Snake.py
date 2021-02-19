import pygame
import sys

class FRUIT:
    def __init__(self):
        #create an x and y position, draw a square
        self.x = 5
        self.y = 4



pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
    screen.fill((175, 215, 70))
    pygame.display.update()
    clock.tick(70)