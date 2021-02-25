from pygame.locals import *
from random import randint
import pygame
import time
import os
import neat
import math
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
windowWidth = 800
windowHeight = 600
bestscore1 = 0

pygame.init()
_display_surf = pygame.display.set_mode((windowWidth,windowHeight), pygame.HWSURFACE)

font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("comicsansms", 20)
pygame.display.set_caption('Game by Taren P')
_running = True
_image_surf = pygame.image.load(os.path.join("Graphics", "gold2.png"))
_apple_surf = pygame.image.load(os.path.join("Graphics", "apple2.png"))
class Apple:
    x = 0
    y = 0
    step = 44
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 
 
 
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*44
       self.x[2] = 2*44
 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
 
    def moveRight(self):
        self.direction = 0
 
    def moveLeft(self):
        self.direction = 1
 
    def moveUp(self):
        self.direction = 2
 
    def moveDown(self):
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
game = Game()
apple = Apple(5,5)
def on_event(event):
    if event.type == QUIT:
        self._running = False


def on_render(player):
    _display_surf.fill((0,0,0))
    player.draw(_display_surf, _image_surf)
    apple.draw(_display_surf, _apple_surf)
    pygame.display.flip()
def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)
def on_cleanup():
    pygame.quit()
def remove(index):
    snakes.pop(index)
    ge.pop(index)
    nets.pop(index)
def Your_score(score):
    global bestscore1
    text_1 = font_style.render(f'Snakes Alive:  {str(len(snakes))}', True, white)
    _display_surf.blit(text_1, [100, 210])
    value = score_font.render("Your Score: " + str(score), True, yellow)
    _display_surf.blit(value, [0, 0])
    if bestscore1 < score:
        bestscore1 = score
    value3 = font_style.render(f'Generation:  {pop.generation+1}', True, white)
    _display_surf.blit(value3, [0, 190])
    value2 = font_style.render("Best Score: " + str(bestscore1), True, white)
    _display_surf.blit(value2, [0, 210])
def eval_genomes(genomes, config):
    global _running, snakes, ge, nets
    snakes = []
    ge = []
    nets = []
    for genome_id, genome in genomes:
        snakes.append(Player(3))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    for i, player in enumerate(snakes):
        escape = False
        while(_running ):
            Your_score(player.length - 3)
            pygame.event.pump()
            output = nets[i].activate((distance((player.x[0], player.y[0]), (apple.x, apple.y)), player.length, player.x, player.y, windowHeight, apple.x, apple.y))
            if output[0] > 0.5:
                player.moveRight()

            if output[1] > 0.5:
                player.moveLeft()

            if output[2] > 0.5:
                player.moveUp()

            if output[3] > 0.5:
                player.moveDown()

            player.update()

            # does snake eat apple?
            for i in range(0,player.length):
                if apple.x == player.x[i] and apple.y == player.y[i]:
                    apple.x = randint(2,9) * 44
                    apple.y = randint(2,9) * 44
                    player.length = player.length + 1
                    ge[i].fitness += 2


            # does snake collide with itself?
            for i in range(2, player.length):
                if game.isCollision(player.x[0],player.y[0],player.x[i], player.y[i],40):
                    ge[i].fitness -= 1
                    remove(i)
                    escape = True
            on_render(player)
            if escape == True:
                break

            time.sleep (50.0 / 1000.0)
    on_cleanup()

def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 10000000000)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)