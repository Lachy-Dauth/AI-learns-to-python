import pygame, random, math, sys, neat, os

pygame.init()

screen_size = 800

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake By Lachlan Dauth')
board_coordinates = (0,49)
pixel_size = screen_size/(board_coordinates[1]+1)
red = [255,0,0]
direction_list = [(1,0),(-1,0),(0,1),(0,-1)]

font = pygame.font.SysFont('arial', 40)

def max_in_list(input_list):
    max = input_list[0]
    index = 0
    for i in range(1,len(input_list)):
        if input_list[i] > max:
            max = input_list[i]
            index = i
    return index

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
            self.score += 1
            self.grow += 1
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
                output_array.append(10)
            elif point == self.apple:
                output_array.append(-10)
            else:
                output_array.append(0)
            output_array.append(len(self.array) - len(self.pixels_reachable(point, [], len(self.array) + 10)))
        output_array.append(point[0] - self.apple[0])
        output_array.append(point[1] - self.apple[1])
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
    score_surface = font.render(str(frames) + "  " + str(score),True,(0,0,0))
    score_rect = score_surface.get_rect(center = (screen_size/2,100))
    screen.blit(score_surface, score_rect)

def draw(screen, snakes):
    pygame.draw.rect(screen,(32,32,32),(0,0,1000,1000))
    for snake in snakes:
        for pixel in snake.array:
            pygame.draw.rect(screen,snake.color,((pixel[0]*pixel_size)+1, (pixel[1]*pixel_size)+1, pixel_size-2, pixel_size-2))
        pygame.draw.rect(screen,red,((snake.apple[0]*pixel_size)+1, (snake.apple[1]*pixel_size)+1, pixel_size-2, pixel_size-2))

def main(genomes, config):
    nets = []
    ge = []
    snakes = []

    frames = 0
    frames_since_action = 0
    TFrames = 100000000000000
    boost = False
    best_only = True
    death_punishment = 0
    no_display = False

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake(25, 25, 1, 2))
        g.fitness = 0
        ge.append(g)

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
                    boost = not boost
                if event.key == pygame.K_1:
                    best_only = not best_only
                if event.key == pygame.K_2:
                    frames = TFrames - 10
                if event.key == pygame.K_3:
                    no_display = not no_display
                if event.key == pygame.K_5:
                    TFrames = 3000
                if event.key == pygame.K_6:
                    TFrames = 100000000000000
        
        if len(snakes) == 0:
            run = False
            break
        
        if frames == TFrames or frames_since_action > 3000:
            for x, car in enumerate(snakes):
                snakes.pop(x)
                nets.pop(x)
                ge.pop(x)
            run = False
            break

        best_snake = snakes[0]
        best_score = -100
        for x, snake in enumerate(snakes):
            if ge[x].fitness != snake.score:
                frames_since_action = 0

            ge[x].fitness = snake.score

            output = max_in_list(nets[x].activate(snake.vision()))
        
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

            if ge[x].fitness > best_score:
                best_score = ge[x].fitness
                best_snake = snake

            if snake.am_i_dead():
                frames_since_action = 0
                ge[x].fitness -= death_punishment
                snakes.pop(x)
                nets.pop(x)
                ge.pop(x)

        if not no_display:
            if not best_only:
                draw(screen, snakes)
                score_display(frames, frames_since_action)
            else:
                draw(screen, [best_snake])
                score_display(best_score, frames_since_action)
            pygame.display.update()
            if boost:
                clock.tick(20)

def run(configPath):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            configPath)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,5000)

    print(winner)

if __name__ == "__main__":
    localDir = os.path.dirname(__file__)
    configPath = os.path.join(localDir, "config-feedforward.txt")
    run(configPath)