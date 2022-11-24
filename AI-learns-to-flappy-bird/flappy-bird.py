import pygame, random, sys, pickle
from AInetwork import *
from pygame import gfxdraw

pygame.init()

screen_size = 900
data_screen_size = 700
data_screen_margin = 100

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
        self.jump_force = -10
        self.acc = 0.5
        self.speed = -10
        self.width = 10
        self.height = 10

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
        gfxdraw.aaellipse(screen, int(bird.pos["x"]), int(bird.pos["y"]), bird.width, bird.height, (255, 255, 0))
        gfxdraw.filled_ellipse(screen, int(bird.pos["x"]), int(bird.pos["y"]), bird.width, bird.height, (255, 255, 0))
    for pipe in pipes:
        pygame.draw.rect(screen, (64,255,64), (pipe.x ,0 , pipe.width, pipe.top_y))
        pygame.draw.rect(screen, (64,255,64), (pipe.x ,pipe.bottom_y , pipe.width, screen_size))

bird = Bird(100, 500)
pipes = [Pipe(random.randint(200, screen_size - 200))]
frames = 0
frames_since_pipe = 0
game_speed = 4
while True:
    frames += 1
    frames_since_pipe += 1
    game_speed += 0.01
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    if frames_since_pipe >= 1000 / (game_speed + 5):
        pipes.append(Pipe(random.randint(200, screen_size - 200)))
        frames_since_pipe = 0
        
    for index, pipe in enumerate(pipes):
        if pipe.move(game_speed):
            pipes.pop(index)
        
    bird.move()

    if bird.dead(pipes):
        bird.pos["y"] = 0
        bird.speed = 0
        pipes = []
        frames = -1
        game_speed = 4

    draw(screen, [bird], pipes)
    score_display(screen, round(frames/10))
    pygame.display.update()
    clock.tick(60)