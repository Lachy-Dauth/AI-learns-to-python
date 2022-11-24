import pygame, random, math, sys

pygame.init()

screen_size = 800

screen = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake By Lachlan Dauth')
board_coordinates = (0,49)
pixel_size = screen_size/(board_coordinates[1]+1)
red = [255,0,0]

class Snake():
    def __init__(self, starting_x, starting_y, starting_length):
        self.color = (0, 255, 0)
        self.dead = False
        self.score = 0 # the score of the game
        self.grow = 0 # how many blocks the snake needs to grow
        self.array = [(starting_x - i, starting_y) for i in range(starting_length)] # the array conaining the snake body
        self.apple = (random.randint(*board_coordinates), random.randint(*board_coordinates)) # the coordinates of the apple
        self.dir = {
            "x" : -1,
            "y" : 0
        }
        self.check_apple()
        print(self.array, self.apple)
    
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
        if self.grow == 0:
            self.array.pop(0)
        else:
            self.grow -= 1

    def am_i_dead(self):
        return self.dead

    def point_in_body(self, point):
        return point[0] < board_coordinates[0] or point[0] > board_coordinates[1] or point[1] < board_coordinates[0] or point[1] > board_coordinates[1] or point in self.array

def draw(screen, snakes):
    pygame.draw.rect(screen,(32,32,32),(0,0,1000,1000))
    for snake in snakes:
        for pixel in snake.array:
            pygame.draw.rect(screen,snake.color,((pixel[0]*pixel_size)+1, (pixel[1]*pixel_size)+1, pixel_size-2, pixel_size-2))
        pygame.draw.rect(screen,red,((snake.apple[0]*pixel_size)+1, (snake.apple[1]*pixel_size)+1, pixel_size-2, pixel_size-2))

def main():
    snakes = [Snake(25,10,3)]
    while True:
        pygame.draw.rect(screen,(32,32,32),(0,0,1000,1000))
        draw(screen, snakes)
        snakes[0].move_snake()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_w:
                    snakes[0].dir = {
                        "x" : 0,
                        "y" : -1
                    }
                if event.key ==  pygame.K_s:
                    snakes[0].dir = {
                        "x" : 0,
                        "y" : 1
                    }
                if event.key ==  pygame.K_a:
                    snakes[0].dir = {
                        "x" : -1,
                        "y" : 0
                    }
                if event.key ==  pygame.K_d:
                    snakes[0].dir = {
                        "x" : 1,
                        "y" : 0
                    }
                if event.key ==  pygame.K_SPACE:
                    snakes.append(Snake(25, 10, 3))
        pygame.display.update()
        if snakes[0].am_i_dead():
            snakes = [Snake(25,10,3)]

        clock.tick(20)

if __name__ == "__main__":
    main()