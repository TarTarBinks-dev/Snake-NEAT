import pygame
import time
import random
import neat
import os
import math
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 250
dis_height = 250
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Taren P')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 70
 
apple = pygame.image.load(os.path.join("Graphics", "apple.png"))
apple = pygame.transform.scale(apple, (20, 20))
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
 
def Your_score(score, y):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
    text_2 = font_style.render("Generation:" + str(y + 1), True, white)
    dis.blit(text_2, [0, 210])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
 
def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)



score = 0
def gameLoop(genomes, config, nets, i, ge, y):
    game_over = False
    game_close = False
    global score
 
    x1 = (dis_width / 2) + 5
    y1 = (dis_height / 2) + 5
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 3
    score = 0
    x1_change = -snake_block

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        output = nets[i].activate((distance((x1, y1), (foodx, foody)), score, foodx, foody, Length_of_snake, x1, y1, dis_height, dis_width))
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
            ge[i].fitness -= 1
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        widthForlines = []
        l = 0
        while l <= dis_width/10:
                pygame.draw.line(dis, black, (0, (dis_height / 25)*l), (dis_width, (dis_height / 25)*l))
                pygame.draw.line(dis, black, ((dis_width / 25)*l, 0), ((dis_width / 25)*l, dis_height))
                l+=1
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        dis.blit(apple, (foodx-5, foody -5.7))
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                ge[i].fitness -= 1
                game_close = True

 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 3, y)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        clock.tick(snake_speed)
        if game_close == True:
                score = Length_of_snake -3
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
        while y<= 10000000:
                for i, snake in enumerate(snakes):
                        gameLoop(genomes, config, nets, i, ge,y)
                        ge[i].fitness += score*5
                y += 1


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    global pop
    pop = neat.Population(config)
    pop.run(eval_genomes, 10000000000)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)