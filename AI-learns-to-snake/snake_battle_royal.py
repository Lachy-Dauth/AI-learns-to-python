import pygame, random, sys, pickle
from AInetwork import *
from pygame import gfxdraw
import statistics as st

pygame.init()

screen_size = 4500
data_screen_size = 700
data_screen_margin = 100

ai_file = "./snake_highlights.pkl"

screen = pygame.display.set_mode((screen_size + data_screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake By Lachlan Dauth')
board_coordinates = starting_board_coordinates = (0,149)
pixel_size = screen_size/(board_coordinates[1]+1)
red = [255,0,0]
direction_list = [(1,0),(-1,0),(0,1),(0,-1)]

# for i in range(-1, 2):
#     for j in range(-1, 2):
#         direction_list.append((i,j))

font = pygame.font.SysFont('arial', 40)
ai_font = pygame.font.SysFont('arial', 20)
ai_font_2 = pygame.font.SysFont('arial', 50)

def is_snake_alive(snake):
    return not snake.am_i_dead()

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

def unpack(arr):
    new_array = []
    for small_arr in arr:
        for item in small_arr:
            new_array.append(item)
    return new_array

def check_apple_all(apple, snake_array):
    for snake in snake_array:
        apple = snake.check_apple(apple, snake_array)
    return apple

class Snake():
    def __init__(self, starting_x, starting_y, starting_length, starting_grow):
        self.color = (0, 255, 0)
        self.dead = False
        self.score = 0 # the score of the game
        self.grow = starting_grow # how many blocks the snake needs to grow
        self.array = [(starting_x - i, starting_y) for i in range(starting_length)] # the array conaining the snake body
        self.dir = {
            "x" : -1,
            "y" : 0
        }
        self.frame = 0
    
    def check_apple(self, apple, snake_array):
        if apple in self.array:
            self.score += 4
            self.grow += 4
            self.frame = 0
            apple = (random.randint(*board_coordinates), random.randint(*board_coordinates))
            apple = check_apple_all(apple, snake_array)
        return apple
    
    def move_snake(self, apple, snake_array):
        self.score += 0.001
        self.frame += 1
        new_point = (self.array[-1][0] + self.dir["x"], self.array[-1][1] + self.dir["y"])
        snake_array_no_current = [*snake_array]
        snake_array_no_current.remove(self)
        for snake in snake_array_no_current:
            if snake.point_in_body(new_point):
                self.dead = True
                break
        if len(self.array) > 1:
            if new_point == self.array[-2] or self.point_out_screen(new_point) or self.frame > 10000:
                self.dead = True
        self.array.append(new_point)
        apple = self.check_apple(apple, snake_array)
        if self.grow == 0:
            self.array.pop(0)
        else:
            self.grow -= 1
        return apple

    def am_i_dead(self):
        return self.dead

    def vision(self, apple, snake_array):
        output_array = []
        snake_array_no_current = [*snake_array]
        snake_array_no_current.remove(self)
        for direction in direction_list:
            point = (self.array[-1][0] + direction[0], self.array[-1][1] + direction[1])
            if len(self.array) > 1:
                if point == self.array[-2] or self.point_out_screen(point):
                    output_array.append(1)
                    continue
            for snake in snake_array_no_current:
                if snake.point_in_body(point):
                    output_array.append(1)
                    break
            else: 
                if point == apple:
                    output_array.append(0)
                else:
                    output_array.append(0.5)
        output_array.append(sigmoid(point[0] - apple[0]))
        output_array.append(sigmoid(point[1] - apple[1]))
        output_array.append(sigmoid(len(snake_array)-5))
        return output_array

    def point_in_body(self, point):
        return point[0] < board_coordinates[0] or point[0] > board_coordinates[1] or point[1] < board_coordinates[0] or point[1] > board_coordinates[1] or point in self.array

    def point_out_screen(self, point):
        return point[0] < board_coordinates[0] or point[0] > board_coordinates[1] or point[1] < board_coordinates[0] or point[1] > board_coordinates[1]

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
    
    def point_out_screen_in(self, head, direction, count):
        if self.point_out_screen(head):
            return count
        else:
            return self.point_out_screen_in((head[0] + direction[0], head[1] + direction[1]), direction, count + 1)

def score_display(frames, score):
    score_surface = font.render(str(frames) + "  " + str(score),True,(0,0,0))
    score_rect = score_surface.get_rect(center = (screen_size/2,100))
    screen.blit(score_surface, score_rect)

def draw(screen, snakes, apple):
    pygame.draw.rect(screen,(32,32,32),(0,0,screen_size,screen_size))
    for snake in snakes:
        for index, pixel in enumerate(snake.array):
            pygame.draw.rect(screen,(255*(len(snake.array)-index)/len(snake.array),255,255*(len(snake.array)-index)/len(snake.array)),((pixel[0]*pixel_size)+1, (pixel[1]*pixel_size)+1, pixel_size-2, pixel_size-2))
            if index +1 < len(snake.array):
                pygame.draw.rect(screen,(255*(len(snake.array)-index)/len(snake.array),255,255*(len(snake.array)-index)/len(snake.array)),(((pixel[0]+snake.array[index+1][0])/2*pixel_size)+1, ((pixel[1]+snake.array[index+1][1])/2*pixel_size)+1, pixel_size-2, pixel_size-2))
    pygame.draw.rect(screen,red,((apple[0]*pixel_size)+1, (apple[1]*pixel_size)+1, pixel_size-2, pixel_size-2))

def draw_stats(screen, past_averages, past_maxes, network, layers, layer_outs, dir_output):
    pygame.draw.rect(screen,(16,16,16),(screen_size,0,data_screen_size,screen_size))
    for index, average in enumerate(past_averages):
        gfxdraw.filled_circle(screen, int(screen_size + 10 + index*(data_screen_size-20)/max_value(len(past_averages) - 1, 1)), int(screen_size - 30 - (average*400)/max_value(max_value_in_list(past_maxes), 1)), 3, (0, 128, 255))
    for index, max in enumerate(past_maxes):
        gfxdraw.filled_circle(screen, int(screen_size + 10 + index*(data_screen_size-20)/max_value(len(past_maxes) - 1, 1)), int(screen_size - 30 - (max*400)/max_value(max_value_in_list(past_maxes), 1)), 3, (255, 128, 0))

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
    

def main(ais, snakes, past_averages, past_maxes, layers):
    global starting_board_coordinates
    global board_coordinates
    global pixel_size
    frames = 0
    frames_since_action = 0
    TFrames = 100000000000000
    boost = 1
    best_only = False
    death_punishment = 0
    no_display = False

    run = True

    apple = (25,25)
    board_coordinates = starting_board_coordinates
    pixel_size = screen_size/(board_coordinates[1]+1)

    while run:
        frames += 1
        frames_since_action += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    boost = max_value((boost+1)%11, 1) 
                if event.key == pygame.K_1:
                    best_only = not best_only
                if event.key == pygame.K_2:
                    frames = TFrames - 10
                if event.key == pygame.K_3:
                    no_display = not no_display
        
        if len(snakes) == 0:
            run = False
            board_coordinates = starting_board_coordinates
            pixel_size = screen_size/(board_coordinates[1]+1)
            return ais

        if frames%5 == -1:
            board_coordinates = (board_coordinates[0], board_coordinates[1]-1)
            pixel_size = screen_size/(board_coordinates[1]+1)
            if apple[0] < board_coordinates[0] or apple[0] > board_coordinates[1] or apple[1] < board_coordinates[0] or apple[1] > board_coordinates[1]:
                apple = (random.randint(*board_coordinates), random.randint(*board_coordinates))
        
        if frames == TFrames or frames_since_action > 3000:
            for x, snake in enumerate(snakes):
                snakes.pop(x)
            run = False
            board_coordinates = starting_board_coordinates
            pixel_size = screen_size/(board_coordinates[1]+1)
            return ais

        best_snake = None
        best_ai = None
        best_score = -100
        best_layer_outs = []
        best_output = 0
        snake_array = unpack([list(filter(is_snake_alive, snake_arr)) for [x, snake_arr] in snakes])
        for index, [x, snake_arr] in enumerate(snakes):
            if not(ais[x].fitness <= st.mean([snake.score for snake in snake_arr]) + 0.1 and ais[x].fitness >= st.mean([snake.score for snake in snake_arr]) - 0.1):
                frames_since_action = 0

            ais[x].fitness = st.mean([snake.score for snake in snake_arr])

            filtered_snake_arr = list(filter(is_snake_alive, snake_arr))
            for snake in filtered_snake_arr:
                output = max_in_list(ais[x].gen_outs(snake.vision(apple, snake_array)))
            
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

                apple = snake.move_snake(apple, snake_array)

            if len(filtered_snake_arr) == 0:
                frames_since_action = 0
                ais[x].fitness -= death_punishment
                snakes.pop(index)
                continue
                
            if ais[x].fitness >= best_score:
                best_score = ais[x].fitness
                best_snake = filtered_snake_arr[max_in_list([snake.score for snake in filtered_snake_arr])]
                best_ai = ais[x]
                best_layer_outs = best_ai.gen_layer_outs(best_snake.vision(apple, snake_array))
                best_output = max_in_list(ais[x].gen_outs(best_snake.vision(apple, snake_array)))
                
        if len(snakes) == 0:
            run = False
            board_coordinates = starting_board_coordinates
            pixel_size = screen_size/(board_coordinates[1]+1)
            return ais

        if len(snakes) == 1 and ais[snakes[0][0]].fitness > 50:
            ais[snakes[0][0]].fitness += 100
            board_coordinates = starting_board_coordinates
            pixel_size = screen_size/(board_coordinates[1]+1)
            return ais

        if not no_display:
            if frames%boost==0:
                if not best_only:
                    draw(screen, filter(is_snake_alive, unpack([snake[1] for snake in snakes])), apple)
                    score_display(frames, frames_since_action)
                elif best_snake != None:
                    draw(screen, [best_snake], apple)
                    score_display(best_score, frames_since_action)
                if best_snake != None:
                    draw_stats(screen, past_averages, past_maxes, best_ai.brain["network"], layers, best_layer_outs, best_output)
                pygame.display.update()

def run():
    num_of_ais = 100
    snakes_per_ai = 1
    elitism = 20
    mutation_chance = 0.1
    mutation_multiplier = 1
    random_ais_per_gen = 20
    num_of_inputs = 7
    hidden_nums = [6]
    num_of_outs = 4
    init_bais_range = [-1, 1]
    initial_ais = generate_initial_ais(num_of_ais, num_of_inputs, hidden_nums, num_of_outs, init_bais_range)
    ais = initial_ais
    past_averages = [0]
    past_maxes = [0]
    layers = [num_of_inputs, *hidden_nums, num_of_outs]
    highlights = {
        "brain_structure" : {
            "num_of_inputs" : num_of_inputs,
            "hidden_nums" : hidden_nums,
            "num_of_outs" : num_of_outs
        },
        "ais" : []
    }

    for i in range(10000):
        snakes = [[j, [Snake(random.randint(*board_coordinates), random.randint(*board_coordinates), 1, 2) for k in range(snakes_per_ai)]] for j in range(num_of_ais)]
        ais = main(ais, snakes, past_averages, past_maxes, layers)
        print("generation ", i+1)
        print([round(ai.fitness, 1) for ai in sorted(ais, key=get_fitness)])
        print()
        past_averages.append(average([ai.fitness for ai in sorted(ais, key=get_fitness)]))
        print(past_averages[-1])
        print()
        past_maxes.append([ai.fitness for ai in sorted(ais, key=get_fitness)][0])
        print(past_maxes[-1])
        if len(past_maxes) - 1 == max_in_list(past_maxes):
            highlights["ais"].append(AI(simular_network([ai for ai in sorted(ais, key=get_fitness)][0].brain, 0, 0)))
        print()
        ais = generate_next_ais(ais, mutation_chance, mutation_multiplier, elitism, random_ais_per_gen, num_of_inputs, hidden_nums, num_of_outs, init_bais_range)

    
    with open(ai_file, 'wb') as handle:
        pickle.dump(highlights, handle)

if __name__ == "__main__":
    run()