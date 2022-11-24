import pygame, sys, random, math

pygame.init()

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
pygame.display.set_caption('Racing By Lachlan Dauth')

track = [(200, 200), (220, 220), (250, 250), (322, 349), (384, 356), (406, 351), (430, 336), (459, 305), (516, 274), (551, 254), (587, 244), (635, 242), (691, 245), (712, 257), (728, 271), (749, 303), (756, 350), (749, 369), (741, 387), (698, 424), (663, 443), (613, 468), (568, 497), (701, 525), (769, 532), (819, 534), (837, 550), (872, 583), (879, 591), (894, 636), (881, 690), (838, 742), (784, 778), (716, 792), (201, 809), (135, 780), (107, 745), (86, 703), (76, 648), (71, 604), (60, 517), (51, 440), (57, 373), (59, 278), (66, 230), (81, 203), (137, 181), (163, 184)]
itrack = [(124, 255), (146, 248), (162, 251), (178, 263), (188, 279), (196, 292), (202, 308), (212, 320), (226, 335), (237, 347), (252, 361), (287, 384), (327, 394), (372, 400), (433, 395), (480, 375), (511, 350), (551, 332), (594, 312), (630, 304), (663, 312), (670, 333), (667, 353), (643, 373), (617, 388), (578, 407), (543, 430), (514, 447), (495, 464), (489, 484), (482, 513), (494, 527), (525, 534), (546, 540), (594, 557), (640, 569), (685, 576), (730, 584), (750, 589), (757, 613), (752, 644), (744, 666), (724, 680), (693, 694), (657, 704), (630, 707), (614, 711), (501, 719), (424, 723), (372, 724), (315, 727), (264, 721), (210, 708), (170, 672), (154, 586), (141, 499), (129, 412), (117, 344), (117, 293)]

Goals = [[(663, 691), (687, 799)], [(613, 701), (630, 813)], [(554, 704), (554, 807)], [(493, 709), (486, 818)], [(438, 712), (436, 817)], [(382, 716), (380, 816)], [(327, 718), (321, 818)], [(277, 712), (271, 818)], [(245, 707), (218, 820)], [(206, 691), (152, 795)], [(184, 663), (104, 755)], [(172, 640), (62, 662)], [(171, 611), (62, 616)], [(159, 563), (58, 566)], [(154, 517), (51, 509)], [(145, 451), (38, 422)], [(129, 357), (50, 335)], [(125, 306), (44, 258)], [(131, 275), (71, 192)], [(145, 257), (117, 158)], [(163, 265), (175, 174)], [(180, 289), (243, 225)], [(206, 328), (271, 257)], [(232, 364), (315, 296)], [(263, 391), (332, 319)], [(321, 409), (358, 331)], [(388, 410), (377, 327)], [(446, 402), (404, 319)], [(486, 383), (439, 306)], [(517, 361), (473, 286)], [(547, 348), (506, 263)], [(578, 330), (533, 244)], [(609, 316), (590, 227)], [(633, 317), (642, 231)], [(655, 321), (738, 264)], [(656, 341), (771, 334)], [(638, 360), (741, 395)], [(624, 373), (699, 435)], [(597, 383), (661, 461)], [(566, 399), (623, 477)], [(519, 432), (602, 484)], [(480, 466), (584, 490)], [(466, 509), (587, 498)], [(509, 540), (603, 500)], [(567, 556), (624, 503)], [(613, 570), (652, 505)], [(646, 579), (688, 502)], [(691, 587), (714, 512)], [(737, 597), (768, 518)], [(750, 619), (851, 551)], [(741, 636), (905, 625)], [(735, 649), (884, 708)], [(706, 674), (834, 769)]]

font = pygame.font.SysFont('arial', 40)
sfont = pygame.font.SysFont('arial', 10)
Color_line=(60,255,60)

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
    x = 700.0
    y = 750.0
    x_speed = 0.0
    y_speed = 0.0
    Speed = 0.0
    p_point = 52
    score = 0.0
    lenght = 7
    width = 3
    angle = -80
    Slip = 10
    SlipTurn = 20
    Acc = 2
    Turn = 3

    points = [[0,0],[0,0],[0,0],[0,0]]
    points_rot = [[0,0],[0,0],[0,0],[0,0]]

    def __init__(self):
        self.colour = hsv_to_rgb(random.random(), random.uniform(0.5, 1), 1)
        self.Bat_rad = 2000
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
            pygame.draw.circle(screen, self.colour, pts[dists.index(min(dists))],3)
            hit_surface = sfont.render(str(round(min(dists))),True,(0,0,0))
            hit_rect = hit_surface.get_rect(center = (pts[dists.index(min(dists))][0] + 20, pts[dists.index(min(dists))][1]))
            screen.blit(hit_surface, hit_rect)
            return(self.Bat_rad - (min(dists)))
        else:
            return(0)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.points, 0)

    def check_point(self, Goals):
        for i in range(len(self.points)):
            for j in range(len(Goals)):
                check = intersect((self.points[i][0], self.points[i][1]), (self.points[(i+1)%4][0], self.points[(i+1)%4][1]), (Goals[j][0][0], Goals[j][0][1]), (Goals[j][1][0], Goals[j][1][1]))
                if check != None and j == (self.p_point + 1)% len(Goals):
                    self.score += 2
                    self.p_point = j

    def check_if_dead(self):
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

    def move(self, f, b, l, r):
        self.Speed -= (self.Speed * (self.Slip/60))
        
        if f:
            self.Speed += self.Acc
        if b:
            self.Speed -= self.Acc
        if l:
            self.angle -= self.Speed * self.Turn
            self.Speed -= (self.Speed * (self.SlipTurn/60))
        if r:
            self.angle += self.Speed * self.Turn
            self.Speed -= (self.Speed * (self.SlipTurn/60))
            
        self.x_speed = self.Speed *  math.sin(math.radians(self.angle))
        self.y_speed = self.Speed * -1 * math.cos(math.radians(self.angle))
        self.x += self.x_speed
        self.y += self.y_speed


def score_display(frames):
    score_surface = font.render(str(frames),True,(0,0,0))
    score_rect = score_surface.get_rect(center = (500,100))
    screen.blit(score_surface, score_rect)

def drawTrack(ml):
    pygame.draw.rect(screen,(64,64,64),(0,0,1000,1000))
    if ml:
        pygame.draw.polygon(screen, (128,128,128), track, 0)
        pygame.draw.polygon(screen, (64,64,64), itrack, 0)

        for i in range(len(Goals)):
            pygame.draw.line(screen,Color_line,Goals[i][0],Goals[i][1])

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

def main():
    car = Car()

    ml = True

    frames = 0

    run = True

    forward = False
    back = False
    left = False
    right = False

    while run:
        frames += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_w:
                    forward = True
                if event.key ==  pygame.K_s:
                    back = True
                if event.key ==  pygame.K_a:
                    left = True
                if event.key ==  pygame.K_d:
                    right = True
                if event.key ==  pygame.K_SPACE:
                    ml = not ml


            if event.type == pygame.KEYUP:
                if event.key ==  pygame.K_w:
                    forward = False
                if event.key ==  pygame.K_s:
                    back = False
                if event.key ==  pygame.K_a:
                    left = False
                if event.key ==  pygame.K_d:
                    right = False
        
        drawTrack(ml)

        car.box_build()

        for i in range(car.Bat_count):
            car.echo(i)

        car.check_point(Goals)

        car.move(forward, back, left, right)

        car.draw(screen)

        if car.check_if_dead() == True:
            car = Car()
        score_display(car.score)
        
        pygame.display.update()
        clock.tick(20)

main()