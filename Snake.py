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
 
dis_width = 230
dis_height = 230
 
bestscore1 = 0

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Taren P')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 150
 
apple = pygame.image.load(os.path.join("Graphics", "apple.png"))
apple = pygame.transform.scale(apple, (20, 20))
font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("comicsansms", 20)
 
def remove(index):
    snakes.pop(index)
    ge.pop(index)
    nets.pop(index)

def Your_score(score, y):
    global bestscore1
    text_1 = font_style.render(f'Snakes Alive:  {str(len(snakes))}', True, white)
    dis.blit(text_1, [100, 210])
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
    if bestscore1 < score:
        bestscore1 = score
    value3 = font_style.render(f'Generation:  {pop.generation+1}', True, white)
    dis.blit(value3, [0, 190])
    value2 = font_style.render("Best Score: " + str(bestscore1), True, white)
    dis.blit(value2, [0, 210])

def find(lst, r):
        return [i for i, x in enumerate(lst) if x == r]
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])
 
def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

score = 0
def gameLoop(genomes, config, i, y):
    game_over = False
    game_close = False
    global score
    x1 = (dis_width / 2) + 5
    y1 = (dis_height / 2) + 5
 
    x1_change = 0
    y1_change = 0
    location = []
    amount = []
    counter = 0

    snake_List = []
    Length_of_snake = 3
    score = 0
    #x1_change = -snake_block
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            ge[i].fitness -= 10
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        l = 0
        if foody == (dis_width/2) + 5:
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if foodx == (dis_height/2) + 5:
            foodx = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        while l <= dis_width/10:
                pygame.draw.line(dis, black, (0, (dis_height / 23)*l), (dis_width, (dis_height / 23)*l))
                pygame.draw.line(dis, black, ((dis_width / 23)*l, 0), ((dis_width / 23)*l, dis_height))
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
                ge[i].fitness -= 10
                game_close = True
        output = nets[i].activate((distance((x1, y1), (foodx, foody)), Length_of_snake, x1, y1, dis_width, foodx, foody))
        if output[0] > 0.5:
                    x1_change = -snake_block
                    y1_change = 0
        if output[1] > 0.5:
                    x1_change = snake_block
                    y1_change = 0
        if output[2] > 0.5:
                    y1_change = -snake_block
                    x1_change = 0
        if output[3] > 0.5:
                    y1_change = snake_block
                    x1_change = 0
        location.append(distance((x1, y1), (foodx, foody)))
        if len(location) > 100:
                del location[0]
        for r in location:
                amount = find(location, r)
                if len(amount) > 2:
                        ge[i].fitness -= 10
                        game_close = True
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 3, y)
        pygame.display.update()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        if counter > 12:
            ge[i] += 0.3
        clock.tick(snake_speed)
        if game_close == True:
                score = Length_of_snake -3
                ge[i].fitness += score*20
                # print(ge[i].fitness)
                remove(i)
                break
                
def eval_genomes(genomes, config):
        global snakes, ge, nets, i
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
                        gameLoop(genomes, config, i, y)
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