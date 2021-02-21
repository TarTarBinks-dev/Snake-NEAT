import pygame
import time
import random
import neat
import os

pygame.init()
            
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Taren P')

clock = pygame.time.Clock()

snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
class SNAKE():
        def __init__(self):
                self.snake_List = []
                self.snake_block = 10
                self.Length_of_snake = 1
                self.snake_Head = []
                self.x1 = dis_width / 2
                self.y1 = dis_height / 2
                self.x1_change = 0
                self.y1_change = 0
                self.foodx = round(random.randrange(0, dis_width - self.snake_block) / 10.0) * 10.0
                self.foody = round(random.randrange(0, dis_height - self.snake_block) / 10.0) * 10.0
        def draw_fruit(self):
                self.foodx = round(random.randrange(0, dis_width - self.snake_block) / 10.0) * 10.0
                self.foody = round(random.randrange(0, dis_height - self.snake_block) / 10.0) * 10.0
            
        def our_snake(self):
                for x in self.snake_List:
                        pygame.draw.rect(dis, black, [x[0], x[1], self.snake_block, self.snake_block])

        def Your_score(self, score):
            self.value = score_font.render("Your Score: " + str(score), True, yellow)
            dis.blit(self.value, [0, 0])

def gameLoop():
        game_over = False
        game_close = False
        
        snake = SNAKE()
        snake.draw_fruit()
        while not game_over:

                while game_close == True:
                        pygame.display.update()
                        gameLoop()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                game_over = True
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        snake.x1_change = -snake.snake_block
                                        snake.y1_change = 0
                                elif event.key == pygame.K_RIGHT:
                                        snake.x1_change = snake.snake_block
                                        snake.y1_change = 0
                                elif event.key == pygame.K_UP:
                                        snake.y1_change = -snake.snake_block
                                        snake.x1_change = 0
                                elif event.key == pygame.K_DOWN:
                                        snake.y1_change = snake.snake_block
                                        snake.x1_change = 0

                if snake.x1 >= dis_width or snake.x1 < 0 or snake.y1 >= dis_height or snake.y1 < 0:
                        game_close = True
                snake.x1 += snake.x1_change
                snake.y1 += snake.y1_change
                dis.fill(blue)
                pygame.draw.rect(dis, green, [snake.foodx, snake.foody, snake.snake_block, snake.snake_block])
                snake.snake_Head.append(snake.x1)
                snake.snake_Head.append(snake.y1)
                snake.snake_List.append(snake.snake_Head)
                if len(snake.snake_List) > snake.Length_of_snake:
                        del snake.snake_List[0]

                for x in snake.snake_List[:-1]:
                        if x == snake.snake_Head:
                                game_close = True

                snake.our_snake()
                pygame.display.update()

                if snake.x1 == snake.foodx and snake.y1 == snake.foody:
                        snake.draw_fruit()
                        snake.Length_of_snake += 1

                clock.tick(snake_speed)

        pygame.quit()
        quit()


gameLoop()