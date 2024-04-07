import random
import threading
import pygame
import time
pygame.init()

def unique(list):
    key = ""
    chars = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+~`[]|;:',./<>?"
    for i in range(7):
        key += random.choice(chars)
    if key not in list:
        return key
    else:
        return unique(list)

pipe_dist = 100
pipe_width = 50

height = 500

bird = pygame.image.load('bird.png')
pipe = pygame.image.load('pipe.png')
background = pygame.image.load('background.png')

ratio = background.get_width()/background.get_height()

win = pygame.display.set_mode((height*ratio, height))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(bird)


bg = pygame.transform.scale(pygame.image.load('background.png'), (height*ratio, height))


clock=pygame.time.Clock()

bg1_x = 0
bg2_x = height*ratio

def obstacle(surface, clock):

    y_pos = random.randint(0, height-pipe_dist)
    x_pos = height*ratio

    lower_pipe = pygame.transform.scale(pipe, (pipe_width, pipe.get_height()))
    upper_pipe = pygame.transform.rotate(lower_pipe, 180)

    while True:
        time.sleep(1)
        surface.blit(lower_pipe, (x_pos, y_pos))
        surface.blit(upper_pipe, (x_pos, (y_pos - (upper_pipe.get_height() + pipe_dist))))
        x_pos -= 1
        if x_pos <= 0:
            break
        pygame.display.update()

class flappy_bird():
    def __init__(self, height, x, y, surface):
        self.surface = surface
        self.x = x
        self.y = y
        self.ratio = bird.get_width()/bird.get_height()
        self.height = height
        self.width = self.ratio*self.height
        self.scaled = pygame.transform.scale(bird, (self.width, self.height))
        self.image = self.scaled
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
    
    def gravity(self):
        self.y += speed
        self.image = pygame.transform.rotate(self.scaled, -20)

    def up(self):
        self.y -= speed*2
        self.image = pygame.transform.rotate(self.scaled, 20)
    
    def draw(self):
        self.rect.update(self.x, self.y, self.width, self.height)
        self.surface.blit(self.image, self.rect)
        pygame.draw.rect(self.surface, (0,0,0), self.rect, width=1)

def backdrop(surfcae, speed):
    global bg1_x, bg2_x
    surfcae.blit(bg, (bg1_x,0))
    surfcae.blit(bg, (bg2_x, 0))

    if bg1_x <= -1*(height*ratio):
        bg1_x = height*ratio
    if bg2_x <= -1*(height*ratio):
        bg2_x = height*ratio

    bg1_x -= speed
    bg2_x -= speed

speed = 1

pipes = {}

run = True
count = 0
flappy = flappy_bird(50, 20, 225, win)
while run:

    clock.tick(60)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    key = pygame.key.get_pressed()

    backdrop(win, speed)
    flappy.draw()
    flappy.gravity()

    if key[pygame.K_SPACE] or key[pygame.K_UP]:
        flappy.up()
    
    if count >= 20:
        pipe_thread = threading.Thread(target=obstacle, args=(win, clock,))
        pipe_thread.start()
        count = 0


    bird_x = flappy.x
    bird_y = flappy.y

    pygame.display.update()
    '''if speed <= 10:
        speed += 0.005
    elif pipe_dist >= 60:
        pipe_dist -= 0.005'''
    count += 1

pygame.quit()