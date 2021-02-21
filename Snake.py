import pygame
import time
import random
import neat
import os
from math import trunc
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 300
dis_height = 300
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Taren P')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
score = 0
def gameLoop(genomes, config, nets, i, ge):
    game_over = False
    game_close = False
    global score
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
    score = 0
    x1_change = -snake_block

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        output = nets[i].activate((len(snake_List), int(score), int(foodx), int(foody), int(Length_of_snake), int(x1), int(y1), int(x1_change), int(y1_change)))
        if output[0] > 0.5:
                if x1_change != snake_block:
                        x1_change = -snake_block
                        y1_change = 0
        elif output[1] > 0.5:
                if x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
        elif output[2] > 0.5:
                if y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
        elif output[3] > 0.5:
                if y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            ge[i] -= 1
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                ge[i] -= 1
                game_close = True

 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        clock.tick(snake_speed)
        score = Length_of_snake -1
        if game_close == True:
                score = Length_of_snake -1
                break
 
def eval_genomes(genomes, config):
        snakes = []
        ge = []
        nets = []
        y = 0
        for genome_id, genome in genomes:
                snakes.append("snake")
                ge.append(genome)
                net = neat.nn.FeedForwardNetwork.create(genome, config)
                nets.append(net)
                genome.fitness = 0
        print(snakes)
        while y<= 10000000:
                for i, snake in enumerate(snakes):
                        gameLoop(genomes, config, nets, i, ge)
                        ge[i].fitness += score*2
                        y += 1


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