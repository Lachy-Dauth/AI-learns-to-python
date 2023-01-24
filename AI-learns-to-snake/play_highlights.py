import pygame, random, sys, pickle
from AInetwork import *
from pygame import gfxdraw

pygame.init()

screen_size = 900
data_screen_size = 700
data_screen_margin = 100

ai_file = "./snake_highlights.pkl"

screen = pygame.display.set_mode((screen_size + data_screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake By Lachlan Dauth')
board_coordinates = (0,49)
pixel_size = screen_size/(board_coordinates[1]+1)
red = [255,0,0]
direction_list = [(1,0),(-1,0),(0,1),(0,-1)]

font = pygame.font.SysFont('arial', 40)
ai_font = pygame.font.SysFont('arial', 20)
ai_font_2 = pygame.font.SysFont('arial', 50)

def average(arr):
    return sum(arr) / len(arr)

def max_in_list(input_list):
    max = input_list[0]
    index = 0
    for i in range(1,len(input_list)):
        if input_list[i] > max:
            max = input_list[i]
            index = i
    return index

def max_value_in_list(input_list):
    max = input_list[0]
    index = 0
    for i in range(1,len(input_list)):
        if input_list[i] > max:
            max = input_list[i]
            index = i
    return max

def max_value(a, b):
    if a > b:
        return a
    else:
        return b

class Snake():
    def __init__(self, starting_x, starting_y, starting_length, starting_grow):
        self.color = (0, 255, 0)
        self.dead = False
        self.score = 0 # the score of the game
        self.grow = starting_grow # how many blocks the snake needs to grow
        self.array = [(starting_x - i, starting_y) for i in range(starting_length)] # the array conaining the snake body
        self.apple = (random.randint(*board_coordinates), random.randint(*board_coordinates)) # the coordinates of the apple
        self.dir = {
            "x" : -1,
            "y" : 0
        }
        self.check_apple()
    
    def check_apple(self):
        if self.apple in self.array:
            self.score += 4
            self.grow += 4
            self.apple = (random.randint(*board_coordinates), random.randint(*board_coordinates))
            self.check_apple()
    
    def move_snake(self):
        new_point = (self.array[-1][0] + self.dir["x"], self.array[-1][1] + self.dir["y"])
        self.dead = self.point_in_body(new_point)
        self.array.append(new_point)
        self.check_apple()
        if self.grow <= 0:
            self.array.pop(0)
        else:
            self.grow -= 1

    def am_i_dead(self):
        return self.dead

    def vision(self):
        output_array = []
        for direction in direction_list:
            point = (self.array[-1][0] + direction[0], self.array[-1][1] + direction[1])
            if self.point_in_body(point):
                output_array.append(1)
            elif point == self.apple:
                output_array.append(0)
            else:
                output_array.append(0.5)
        output_array.append(sigmoid(point[0] - self.apple[0]))
        output_array.append(sigmoid(point[1] - self.apple[1]))
        return output_array

    def point_in_body(self, point):
        return point[0] < board_coordinates[0] or point[0] > board_coordinates[1] or point[1] < board_coordinates[0] or point[1] > board_coordinates[1] or point in self.array

    def pixels_reachable(self, head, visited_nodes, max):
        if self.point_in_body(head) or len(visited_nodes) >= max:
            return visited_nodes
        else:
            visited_nodes.append(head)
        for direction in direction_list:
            point = (head[0] + direction[0], head[1] + direction[1])
            if not (point in visited_nodes):
                visited_nodes = self.pixels_reachable(point, visited_nodes, max)
        return visited_nodes

def score_display(frames, score):
    score_surface = font.render(str(frames) + "  " + str(score),True,(255,255,255))
    score_rect = score_surface.get_rect(center = (screen_size/2,100))
    screen.blit(score_surface, score_rect)

def draw(screen, snakes):
    pygame.draw.rect(screen,(32,32,32),(0,0,screen_size,screen_size))
    for snake in snakes:
        for index, pixel in enumerate(snake.array):
            pygame.draw.rect(screen,snake.color,((pixel[0]*pixel_size)+1, (pixel[1]*pixel_size)+1, pixel_size-2, pixel_size-2))
            if index +1 < len(snake.array):
                pygame.draw.rect(screen,snake.color,(((pixel[0]+snake.array[index+1][0])/2*pixel_size)+1, ((pixel[1]+snake.array[index+1][1])/2*pixel_size)+1, pixel_size-2, pixel_size-2))
        pygame.draw.rect(screen,red,((snake.apple[0]*pixel_size)+1, (snake.apple[1]*pixel_size)+1, pixel_size-2, pixel_size-2))

def draw_stats(screen, past_scores, network, layers, layer_outs, dir_output):
    pygame.draw.rect(screen,(16,16,16),(screen_size,0,data_screen_size,screen_size))
    for index, score in enumerate(past_scores):
        gfxdraw.filled_circle(screen, int(screen_size + 10 + index*(data_screen_size-20)/max_value(len(past_scores) - 1, 1)), int(screen_size - 30 - (score*400)/max_value(max_value_in_list(past_scores), 1)), 3, (0, 128, 255))

    network_position = []
    for i in range(len(layers)):
        layer_position = []
        for j in range(layers[i]):
            layer_position.append((int(screen_size + data_screen_margin + (i)*(data_screen_size - 2*data_screen_margin)/(len(layers)-1)), int(200 + layers[i] * 20 - j * 40)))
        network_position.append(layer_position)

    for index, layer in enumerate(network):
        for i in range(len(layer)):
            for j in range(len(layer[i])):
                if layer[i][j] > 0:
                    pygame.draw.line(screen, (32, 32, 255), network_position[index][j], network_position[index+1][i], int(abs(layer[i][j])*3))
                else:
                    pygame.draw.line(screen, (255, 0, 0), network_position[index][j], network_position[index+1][i], int(abs(layer[i][j])*3))

    
    for i in range(len(layers)):
        layer_position = []
        for j in range(layers[i]):
            color = (layer_outs[i][j]*255, layer_outs[i][j]*255, layer_outs[i][j]*255)
            gfxdraw.filled_circle(screen, int(screen_size + data_screen_margin + (i)*(data_screen_size - 2*data_screen_margin)/(len(layers)-1)), int(200 + layers[i] * 20 - j * 40), 6, color)

    outputs = ["↑", "↓", "←", "→"]
    for index, output in enumerate(outputs):
        if index == dir_output:
            score_surface = ai_font_2.render(output,True,(255,255,255))
        else:
            score_surface = ai_font.render(output,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (network_position[-1][index][0] + data_screen_margin/2, network_position[-1][index][1]))
        screen.blit(score_surface, score_rect)

    inputs = ["→", "←", "↓", "↑", "apple Y", "apple X"]
    for index, input in enumerate(inputs):
        score_surface = ai_font.render(input,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (network_position[0][index][0] - data_screen_margin/2, network_position[0][index][1]))
        screen.blit(score_surface, score_rect)
    

def main(ai, snake, past_scores, layers):
    frames = 0
    frames_since_action = 0
    TFrames = 100000000000000
    max_boost = 3
    boost = max_boost + 1
    death_punishment = 0
    no_display = False

    run = True

    while run:
        frames += 1
        frames_since_action += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    boost = max_value((boost+1)%(max_boost+2), 1) 
                if event.key == pygame.K_2:
                    frames = TFrames - 10
                if event.key == pygame.K_3:
                    no_display = not no_display
        
        if frames == TFrames or frames_since_action > 3000:
            return ai.fitness

        if ai.fitness != snake.score:
            frames_since_action = 0

        ai.fitness = snake.score

        output = max_in_list(ai.gen_outs(snake.vision()))
    
        if output == 0:
            snake.dir = {
                "x" : 0,
                "y" : -1
            }
        if output == 1:
            snake.dir = {
                "x" : 0,
                "y" : 1
            }
        if output == 2:
            snake.dir = {
                "x" : -1,
                "y" : 0
            }
        if output ==  3:
            snake.dir = {
                "x" : 1,
                "y" : 0
            }

        snake.move_snake()

        if snake.am_i_dead():
            ai.fitness -= death_punishment
            return ai.fitness

        if not no_display:
            if frames%boost==0 or boost == max_boost + 1:
                draw(screen, [snake])
                score_display("Score: " + str(ai.fitness), "Generation: " + str(len(past_scores)))
                draw_stats(screen, past_scores, ai.brain["network"], layers, ai.gen_layer_outs(snake.vision()), output)
                pygame.display.update()
                if boost == max_boost + 1:
                    clock.tick(20)

def run():
    with open(ai_file, 'rb') as handle:
        highlights = pickle.load(handle)
    num_of_inputs = highlights["brain_structure"]["num_of_inputs"]
    hidden_nums = highlights["brain_structure"]["hidden_nums"]
    num_of_outs = highlights["brain_structure"]["num_of_outs"]
    ais = highlights["ais"]
    past_scores = [0]
    layers = [num_of_inputs, *hidden_nums, num_of_outs]
    for index, ai in enumerate(ais):
        snake = Snake(25, 25, 1, 2)
        ai_fitness = main(ai, snake, past_scores, layers)
        print("generation ", index+1)
        print(ai_fitness)
        print()
        past_scores.append(ai_fitness)
        print(past_scores[-1])
        print()

if __name__ == "__main__":
    run()