import sys, pygame, random, math, pickle
from AInetwork import *
from pygame import gfxdraw

pygame.init()

screen_size = 900
data_screen_size = 800
data_screen_margin = 100

ai_file = "./car_highlights.pkl"

screen = pygame.display.set_mode((screen_size + data_screen_size, screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Racing By Lachlan Dauth')

track = [(200, 200), (220, 220), (250, 250), (322, 349), (384, 356), (406, 351), (430, 336), (459, 305), (516, 274), (551, 254), (587, 244), (635, 242), (691, 245), (712, 257), (728, 271), (749, 303), (756, 350), (749, 369), (741, 387), (698, 424), (663, 443), (613, 468), (568, 497), (701, 525), (769, 532), (819, 534), (837, 550), (872, 583), (879, 591), (894, 636), (881, 690), (838, 742), (784, 778), (716, 792), (201, 809), (135, 780), (107, 745), (86, 703), (76, 648), (71, 604), (60, 517), (51, 440), (57, 373), (59, 278), (66, 230), (81, 203), (137, 181), (163, 184)]
itrack = [(124, 255), (146, 248), (162, 251), (178, 263), (188, 279), (196, 292), (202, 308), (212, 320), (226, 335), (237, 347), (252, 361), (287, 384), (327, 394), (372, 400), (433, 395), (480, 375), (511, 350), (551, 332), (594, 312), (630, 304), (663, 312), (670, 333), (667, 353), (643, 373), (617, 388), (578, 407), (543, 430), (514, 447), (495, 464), (489, 484), (482, 513), (494, 527), (525, 534), (546, 540), (594, 557), (640, 569), (685, 576), (730, 584), (750, 589), (757, 613), (752, 644), (744, 666), (724, 680), (693, 694), (657, 704), (630, 707), (614, 711), (501, 719), (424, 723), (372, 724), (315, 727), (264, 721), (210, 708), (170, 672), (154, 586), (141, 499), (129, 412), (117, 344), (117, 293)]

Goals = [[(663, 691), (687, 799)], [(613, 701), (630, 813)], [(554, 704), (554, 807)], [(493, 709), (486, 818)], [(438, 712), (436, 817)], [(382, 716), (380, 816)], [(327, 718), (321, 818)], [(277, 712), (271, 818)], [(245, 707), (218, 820)], [(206, 691), (152, 795)], [(184, 663), (104, 755)], [(172, 640), (62, 662)], [(171, 611), (62, 616)], [(159, 563), (58, 566)], [(154, 517), (51, 509)], [(145, 451), (38, 422)], [(129, 357), (50, 335)], [(125, 306), (44, 258)], [(131, 275), (71, 192)], [(145, 257), (117, 158)], [(163, 265), (175, 174)], [(180, 289), (243, 225)], [(206, 328), (271, 257)], [(232, 364), (315, 296)], [(263, 391), (332, 319)], [(321, 409), (358, 331)], [(388, 410), (377, 327)], [(446, 402), (404, 319)], [(486, 383), (439, 306)], [(517, 361), (473, 286)], [(547, 348), (506, 263)], [(578, 330), (533, 244)], [(609, 316), (590, 227)], [(633, 317), (642, 231)], [(655, 321), (738, 264)], [(656, 341), (771, 334)], [(638, 360), (741, 395)], [(624, 373), (699, 435)], [(597, 383), (661, 461)], [(566, 399), (623, 477)], [(519, 432), (602, 484)], [(480, 466), (584, 490)], [(466, 509), (587, 498)], [(509, 540), (603, 500)], [(567, 556), (624, 503)], [(613, 570), (652, 505)], [(646, 579), (688, 502)], [(691, 587), (714, 512)], [(737, 597), (768, 518)], [(750, 619), (851, 551)], [(741, 636), (905, 625)], [(735, 649), (884, 708)], [(706, 674), (834, 769)]]

Color_line=(60,255,60)

font = pygame.font.SysFont('arial', 40)
ai_font = pygame.font.SysFont('arial', 20)
ai_font_2 = pygame.font.SysFont('arial', 50)

def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

class Car:
    frame = 0
    x = 700.0
    y = 750.0
    x_speed = 0.0
    y_speed = 0.0
    p_point = 52
    score = 0.0
    lenght = 7
    width = 3
    angle = -130
    Acc = 3
    Turn = 15
    drift = 0.8

    points = [[0,0],[0,0],[0,0],[0,0]]
    points_rot = [[0,0],[0,0],[0,0],[0,0]]

    def __init__(self):
        self.colour = hsv_to_rgb(random.random(), random.uniform(0.5, 1), 1)
        self.Bat_rad = 1000
        self.Bat_count = 5
        self.Bat_range = 360/(self.Bat_count-1)
        self.fov = 1/2
        self.Bat_range = self.Bat_range * self.fov

        self.Bat = []

        for i in range(self.Bat_count):
            self.Bat.append(rot(0,self.Bat_rad,0,0,self.Bat_range*i))
        self.Bat_rot = self.Bat

    def box_build(self):

        self.points_rot = [[self.x-self.width,self.y-self.lenght],[self.x-self.width,self.y+self.lenght],[self.x+self.width,self.y+self.lenght],[self.x+self.width,self.y-self.lenght]]

        for i in range(len(self.points_rot)):
            self.points[i][0] = rot(self.points_rot[i][0],self.points_rot[i][1],self.x,self.y,self.angle)[0]
            self.points[i][1] = rot(self.points_rot[i][0],self.points_rot[i][1],self.x,self.y,self.angle)[1]


        for i in range(self.Bat_count):
            self.Bat[i] = (rot(0,self.Bat_rad,0,0,self.Bat_range*i)[0] + self.x, rot(0,self.Bat_rad,0,0,self.Bat_range*i)[1] + self.y)
        for i in range(self.Bat_count):
            self.Bat_rot[i] = rot(self.Bat[i][0],self.Bat[i][1],self.x,self.y,self.angle + 180 - (180*self.fov))

    def echo(self,i):
        dists = []
        pts = []
        for j in range(len(track)):
            dist = intersect(self.Bat_rot[i], (self.x,self.y), (track[j][0], track[j][1]), (track[(j+1)%(len(track))][0], track[(j+1)%(len(track))][1]))
            if dist != None:
                pts.append(dist)
                dists.append(abs(math.sqrt(((dist[0]-self.x) ** 2) + ((dist[1]-self.y) ** 2))))
        for j in range(len(itrack)):
            dist = intersect(self.Bat_rot[i], (self.x,self.y), (itrack[j][0], itrack[j][1]), (itrack[(j+1)%(len(itrack))][0], itrack[(j+1)%(len(itrack))][1]))
            if dist != None:
                pts.append(dist)
                dists.append(abs(math.sqrt(((dist[0]-self.x) ** 2) + ((dist[1]-self.y) ** 2))))
        if len(dists) > 0:
            #pygame.draw.circle(screen, self.colour, pts[dists.index(min(dists))],3)
            return((min(dists)/100)-1)
        else:
            return(200)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.points, 0)
        self.frame += 1

    def check_point(self, Goals):
        for i in range(len(self.points)):
            for j in range(len(Goals)):
                check = intersect((self.points[i][0], self.points[i][1]), (self.points[(i+1)%4][0], self.points[(i+1)%4][1]), (Goals[j][0][0], Goals[j][0][1]), (Goals[j][1][0], Goals[j][1][1]))
                if check != None and j == (self.p_point + 1)% len(Goals):
                    self.score += 2
                    self.frame = 0
                    self.p_point = j

    def check_if_dead(self):
        if self.frame >= 50:
            return True
        for i in range(len(self.points)):
            for j in range(len(track)):
                result = intersect((self.points[i][0], self.points[i][1]), (self.points[(i+1)%4][0], self.points[(i+1)%4][1]), (track[j][0], track[j][1]), (track[(j+1)%(len(track))][0], track[(j+1)%(len(track))][1]))
                if result != None:
                    return True
        for i in range(len(self.points)):
            for j in range(len(itrack)):
                result = intersect((self.points[i][0], self.points[i][1]), (self.points[(i+1)%4][0], self.points[(i+1)%4][1]), (itrack[j][0], itrack[j][1]), (itrack[(j+1)%(len(itrack))][0], itrack[(j+1)%(len(itrack))][1]))
                if result != None:
                    return True
        return False

    def move(self, f, a):
        self.x_speed = self.x_speed * self.drift
        self.y_speed = self.y_speed * self.drift
        
        self.x_speed += self.Acc *  math.sin(math.radians(self.angle)) * f * (1-(abs(a)/2))
        self.y_speed += self.Acc * -1 * math.cos(math.radians(self.angle)) * f * (1-(abs(a)/2))
        self.angle += self.Turn * a
            
        self.x += self.x_speed
        self.y += self.y_speed



def score_display(frames, score):
    score_surface = font.render(str(frames) + "  " + str(score),True,(0,0,0))
    score_rect = score_surface.get_rect(center = (screen_size/2,100))
    screen.blit(score_surface, score_rect)

def drawTrack(bool):
    if not bool:
        pygame.draw.rect(screen,(64,64,64),(0,0,screen_size ,screen_size))
        pygame.draw.polygon(screen, (128,128,128), track, 0)
        pygame.draw.polygon(screen, (64,64,64), itrack, 0)
    gfxdraw.rectangle(screen, (0,0,screen_size,screen_size), (64,64,64))
    gfxdraw.aapolygon(screen, track, (128,128,128))
    gfxdraw.aapolygon(screen, itrack, (64,64,64))

def intersect(p1, p2, p3, p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return None
    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return (x,y)

def rot(x1,y1,x2,y2,a):
    n_x = ((x1-x2) * math.cos(math.radians(a)))-((y1-y2) * math.sin(math.radians(a)))+x2
    n_y = ((y1-y2) * math.cos(math.radians(a)))+((x1-x2) * math.sin(math.radians(a)))+y2
    return (n_x,n_y)

def draw_stats(screen, past_scores, network, layers, layer_outs, first_pass):
    if first_pass:
        pygame.draw.rect(screen,(16,16,16),(screen_size,0,data_screen_size,screen_size))
        for index, score in enumerate(past_scores):
            gfxdraw.filled_circle(screen, int(screen_size + 10 + index*(data_screen_size-20)/max_value(len(past_scores) - 1, 1)), int(screen_size - 30 - (score*400)/max_value(max_value_in_list(past_scores), 1)), 3, (0, 128, 255))
    else:
        pygame.draw.rect(screen,(16,16,16),(screen_size,0,data_screen_size,screen_size/2))

    network_position = []
    for i in range(len(layers)):
        layer_position = []
        for j in range(layers[i]):
            layer_position.append((int(screen_size + data_screen_margin + (i)*(data_screen_size - 2*data_screen_margin)/(len(layers)-1)), int(200 + layers[i] * 30 - j * 60)))
        network_position.append(layer_position)

    for index, layer in enumerate(network):
        for i in range(len(layer)):
            for j in range(len(layer[i])):
                if layer[i][j] > 0:
                    pygame.draw.line(screen, (32, 32, 255), network_position[index][j], network_position[index+1][i], int(abs(layer[i][j])))
                else:
                    pygame.draw.line(screen, (255, 0, 0), network_position[index][j], network_position[index+1][i], int(abs(layer[i][j])))

    
    for i in range(len(layers)):
        layer_position = []
        for j in range(layers[i]):
            color = (layer_outs[i][j]*255, layer_outs[i][j]*255, layer_outs[i][j]*255)
            gfxdraw.filled_circle(screen, int(screen_size + data_screen_margin + (i)*(data_screen_size - 2*data_screen_margin)/(len(layers)-1)), int(200 + layers[i] * 30 - j * 60), 6, color)

    outputs = ["speed", "turns"]
    for index, output in enumerate(outputs):
        score_surface = ai_font.render(output,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (network_position[-1][index][0] + data_screen_margin/2, network_position[-1][index][1]))
        screen.blit(score_surface, score_rect)

    inputs = ["←", "↖", "↑", "↗", "→", "speed"]
    for index, input in enumerate(inputs):
        score_surface = ai_font.render(input,True,(255,255,255))
        score_rect = score_surface.get_rect(center = (network_position[0][index][0] - data_screen_margin/2, network_position[0][index][1]))
        screen.blit(score_surface, score_rect)

def main(ai, car, past_scores, layers):
    frames = 0
    Tframes = 1800
    boost = False
    no_display = False

    run = True

    while run:
        frames += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    boost = not boost
                if event.key == pygame.K_3:
                    no_display = not no_display

        drawTrack(False)
        
        if frames == Tframes:
            return ai.fitness

        car.box_build()

        car.check_point(Goals)
        ai.fitness = car.score

        output = ai.gen_outs([car.echo(0), car.echo(1), car.echo(2), car.echo(3), car.echo(4), (car.x_speed**2 + car.y_speed**2)**0.5/5])

        car.colour = hsv_to_rgb((output[1]+1)/2, output[0], 1)
        
        if (output[0] < 0):
            car.colour = hsv_to_rgb(0.2, output[0], 1)

        car.move(output[0], 2*(output[1]-0.5))

        if car.check_if_dead() == True:
            return ai.fitness

        if not no_display:
            car.draw(screen)
            score_display(ai.fitness, frames)
            draw_stats(screen, past_scores, ai.brain["network"], layers, ai.gen_layer_outs([car.echo(0), car.echo(1), car.echo(2), car.echo(3), car.echo(4), (car.x_speed**2 + car.y_speed**2)**0.5/5]), frames == 1)
            pygame.display.update()
            if boost:
                clock.tick(10)

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
        car = Car()
        ai_fitness = main(ai, car, past_scores, layers)
        print("generation ", index+1)
        print(ai_fitness)
        past_scores.append(ai_fitness)
        print()

if __name__ == "__main__":
    run()
