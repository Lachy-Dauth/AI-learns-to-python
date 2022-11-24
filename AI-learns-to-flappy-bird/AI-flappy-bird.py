import pygame, random, sys, pickle
from AInetwork import *
from pygame import gfxdraw

pygame.init()

screen_size = 900
data_screen_size = 700
data_screen_margin = 100

ai_file = "./snake_highlights.pkl"

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird By Lachlan Dauth')

font = pygame.font.SysFont('arial', 40)

class Bird:
    
    def __init__(self, x, y):
        self.pos = {
            "x" : x,
            "y" : y
        }
        self.jump_force = -20
        self.acc = 2
        self.speed = -10
        self.width = 10
        self.height = 10
        self.color = (255,255, 0)

    def jump(self):
        self.speed = self.jump_force

    def move(self):
        self.speed += self.acc
        self.pos["y"] += self.speed
        
    def dead(self, pipes):
        for pipe in pipes:
            if pipe.x < self.pos["x"] + self.width and pipe.x + pipe.width > self.pos["x"] - self.width:
                if pipe.top_y > self.pos["y"] - self.height or pipe.bottom_y < self.pos["y"] + self.height:
                    return True
        if self.pos["y"] < 0 or self.pos["y"] > screen_size:
            return True
        return False
    
    def vision(self, pipes, speed):
        array = []
        array.append(sigmoid((self.pos["y"] - pipes[0].bottom_y)/10))
        array.append(sigmoid((self.pos["y"] - pipes[0].top_y)/10))
        array.append(sigmoid((self.pos["x"] - pipes[0].x)/10))
        array.append(sigmoid(self.speed))
        array.append(sigmoid(speed))
        return array

class Pipe:
    def __init__(self, y):
        self.top_y = y - 80
        self.bottom_y = y + 80
        self.width = 100
        self.x = screen_size

    def move(self, speed):
        self.x -= speed
        return self.x + self.width < 0

def score_display(screen, score):
    score_surface = font.render(str(score),True,(0,0,0))
    score_rect = score_surface.get_rect(center = (screen_size/2,100))
    screen.blit(score_surface, score_rect)

def draw(screen, birds, pipes):
    pygame.draw.rect(screen, (128,128,255), (0,0,screen_size, screen_size))
    for bird in birds:
        gfxdraw.filled_ellipse(screen, int(bird.pos["x"]), int(bird.pos["y"]), bird.width, bird.height, (0,0,0))
        gfxdraw.filled_ellipse(screen, int(bird.pos["x"]), int(bird.pos["y"]), bird.width-1, bird.height-1, bird.color)
    for pipe in pipes:
        pygame.draw.rect(screen, (64,255,64), (pipe.x ,0 , pipe.width, pipe.top_y))
        pygame.draw.rect(screen, (64,255,64), (pipe.x ,pipe.bottom_y , pipe.width, screen_size))

bird = Bird(100, 500)
game_speed = 4
def main(ais, birds, past_averages, past_maxes, layers):
    frames = 0
    game_speed = 5
    TFrames = 100000000000000
    frames_since_pipe = 0
    boost = 1
    no_display = False

    pipes = [Pipe(random.randint(200, screen_size - 200))]
    run = True

    while run:
        frames += 1
        frames_since_pipe += 1
        game_speed += 0.001

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    boost = max_value((boost+1)%11, 1) 
                if event.key == pygame.K_2:
                    frames = TFrames - 10
                if event.key == pygame.K_3:
                    no_display = not no_display
        
        for index, pipe in enumerate(pipes):
            if pipe.move(game_speed):
                pipes.pop(index)

        if frames_since_pipe >= 1000 / (game_speed + 5) or len(pipes) == 0:
            pipes.append(Pipe(random.randint(200, screen_size - 200)))
            frames_since_pipe = 0
            
        if len(birds) == 0:
            return ais

        for index, [x, bird] in enumerate(birds):
            ais[x].fitness = frames

            [output] = ais[x].gen_outs(bird.vision(pipes, game_speed)) 

            if output < 0.5:
                bird.jump()

            bird.color = (255, output*255, 0)

            bird.move()

            if bird.dead(pipes):
                birds.pop(index)

        if not no_display:
            if frames%boost==0:
                draw(screen, [bird[1] for bird in birds], pipes)
                score_display(screen, round(frames/10))
                pygame.display.update()
                clock.tick(60)

def run():
    num_of_ais = 300
    elitism = 20
    mutation_chance = 0.1
    mutation_multiplier = 1
    random_ais_per_gen = 80
    num_of_inputs = 5
    hidden_nums = []
    num_of_outs = 1
    init_bais_range = [-3, 3]
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
        birds = [[j, Bird(100, 500)] for j in range(num_of_ais)]
        ais = main(ais, birds, past_averages, past_maxes, layers)
        print("generation ", i+1)
        print([round(ai.fitness, 1) for ai in sorted(ais, key=get_fitness)])
        print()
        past_averages.append(average([ai.fitness for ai in sorted(ais, key=get_fitness)]))
        print(past_averages[-1])
        print()
        past_maxes.append([ai.fitness for ai in sorted(ais, key=get_fitness)][0])
        print(past_maxes[-1])
        highlights["ais"].append(AI(simular_network([ai for ai in sorted(ais, key=get_fitness)][0].brain, 0, 0)))
        print()
        if i%10 == 0:
            with open(ai_file, 'wb') as handle:
                pickle.dump(highlights, handle)
        ais = generate_next_ais(ais, mutation_chance, mutation_multiplier, elitism, random_ais_per_gen, num_of_inputs, hidden_nums, num_of_outs, init_bais_range)

    
    with open(ai_file, 'wb') as handle:
        pickle.dump(highlights, handle)

if __name__ == "__main__":
    run()