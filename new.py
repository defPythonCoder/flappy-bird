#Librarys
import random
import pygame
import threading

#Initializing 
pygame.init()

#Images
bird_image = pygame.image.load('bird.png')
pipe_image = pygame.image.load('pipe.png')
background_image = pygame.image.load('background.png')

#Constants
ratio = background_image.get_width()/background_image.get_height()
window_height = 500
fps = 120
#flappyConst
flappy_height = 50
#pipeConst
pipe_width = 100

#Vars
speed = 1
bg1_x, bg2_x = 0, window_height*ratio
score = 0
change_score = False
name = ""
#buttonVars
clicked = {}
clicked["Play"] = False
#FlappyVars
flappy_dist = 20
#PipeVars
pipe_verticle = 150
pipes = {}
deletion = []

#Scaled
bg = pygame.transform.scale(pygame.image.load('background.png'), (window_height*ratio, window_height))
lower_pipe = pygame.transform.scale(pipe_image, (pipe_width, pipe_image.get_height()))
upper_pipe = pygame.transform.rotate(lower_pipe, 180)

#Text Fuctions----------------------------------------
def mouse():
    a = pygame.mouse.get_pos()
    return(a)

def pressed(x, y,width,height):
    a = mouse()
    if x<a[0]<(x+width) and y<a[1]<(y+height) and pygame.mouse.get_pressed()[0]:
        return True

def textrect(font,text1,color,size):
    font = pygame.font.SysFont(font, size)
    text = font.render(text1, True,color)
    rect = text.get_rect()
    return rect

def type(font,text1,color,centre_x,centre_y,size,surface):
    font = pygame.font.SysFont(font, size)
    text = font.render(text1, True,color)
    newX, newY = centre_x - (text.get_rect()[2]/2), centre_y - (text.get_rect()[3]/2)
    surface.blit(text,(newX,newY))

def button(win, center_x, center_y, text, textcolor, bgcolor, buttoncolor, font, size, tag):
    global clicked

    rect = textrect(font, text, textcolor, size)
    width = rect[2] + 10
    height = rect[3] + 10

    newX = center_x - (width/2)
    newY = center_y - (height/2)

    a = mouse()
    x1 = newX
    y1 = newY
    if newX<a[0]<(newX+width) and newY<a[1]<(newY+height):
        x1 = newX - 10
        y1 = newY + 10
        if pressed(newX, newY, width, height):
            clicked[tag] = True

    pygame.draw.rect(win, bgcolor,(x1,y1,width,height))
    pygame.draw.rect(win, buttoncolor,(newX,newY,width,height))
    type(font, text, textcolor, center_x, center_y,size,win)

def textBox(screen, x, y, width, height):
    global name

    text = ""
    active = False
    font = pygame.font.SysFont("Valorax", 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_box_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        name = text
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((255, 255, 255))
        text_box_rect = pygame.Rect(x, y, width, height)
        color = (255, 255, 255) if active else (200, 200, 200)
        pygame.draw.rect(screen, color, text_box_rect, 2)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (x + 5, y + 5))
        pygame.display.flip()


    pygame.draw.rect(surface, color, box, border_radius=border)



#Game Functions
def unique(list):
    key = ""
    chars = "abcdefghijklmnopqrstuvwxyz1234567890"
    for i in range(7):
        key += random.choice(chars)
    if key not in list:
        return key
    else:
        return unique(list)
    
def make_pipe(tag):
    global pipes

    y_pos = random.randint(0 + pipe_verticle, window_height-pipe_verticle)
    x_pos = window_height*ratio

    lower_rect = pygame.Rect(x_pos, y_pos, lower_pipe.get_width(), lower_pipe.get_height ())
    upper_rect = pygame.Rect(x_pos, (y_pos - (upper_pipe.get_height() + pipe_verticle)), upper_pipe.get_width(), upper_pipe.get_height())

    pipes[tag][0], pipes[tag][1] = lower_rect, upper_rect

def redraw_pipe(surface, tag):
    global pipes

    surface.blit(lower_pipe, pipes[tag][0])
    surface.blit(upper_pipe, pipes[tag][1])

    pipes[tag][0].x -= speed
    pipes[tag][1].x -= speed

    if pipes[tag][0].x <= 0-pipe_width:
        deletion.append(tag)

class flappy_bird():
    def __init__(self, height, x, y, surface):
        self.surface = surface
        self.x = x
        self.y = y
        self.ratio = bird_image.get_width()/bird_image.get_height()
        self.height = height
        self.width = self.ratio*self.height
        self.scaled = pygame.transform.scale(bird_image, (self.width, self.height))
        self.image = self.scaled
        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)
    
    def move(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or key[pygame.K_UP]):
            if (self.rect.y >= 0):
                self.y -= speed
                self.image = pygame.transform.rotate(self.scaled, 20)
        elif self.rect.y <= (window_height - flappy_height):
            self.y += speed
            self.image = pygame.transform.rotate(self.scaled, -20)
    
    def draw(self):
        self.rect.update(self.x, self.y, self.width, self.height)
        self.surface.blit(self.image, self.rect)
        self.rect.y += 10
        self.rect.x += 5

def backdrop(surfcae, speed):
    global bg1_x, bg2_x
    surfcae.blit(bg, (bg1_x,0))
    surfcae.blit(bg, (bg2_x, 0))

    if bg1_x <= -1*(window_height*ratio):
        bg1_x = window_height*ratio
    if bg2_x <= -1*(window_height*ratio):
        bg2_x = window_height*ratio

    bg1_x -= speed
    bg2_x -= speed

def display_score(surface):
    display_text = f"SCORE: {score}"
    score_rect = textrect('valorax', display_text, (255,255,255), 30)
    score_y = 10
    score_x = window_height*ratio - (score_rect[2] + 10)
    type('Valorax', display_text, (255,0,0         ), score_x, score_y, 30, surface)

def game():
    global speed, pipe_verticle, pipes, deletion, score, fps, change_score

    #pygame
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((window_height*ratio, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Flappy Bird")
    pygame.display.set_icon(bird_image)   

    bird = flappy_bird(flappy_height, flappy_dist, ((window_height-flappy_height)/2), window)
    pipe_count = 0

    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        backdrop(window, speed)
        bird.move()
        bird.draw()

        if pipe_count <= 0:
            tag = unique(pipes)
            pipes[tag] = [None, None]
            make_pipe(tag)
            pipe_count = 500 + 80
            if pipe_verticle >= 100:
                pipe_verticle -= 10
            elif fps <= 200:
                fps += 5

        for i in pipes:
            redraw_pipe(window, i)
            if pygame.Rect.colliderect(pipes[i][0], bird.rect) or pygame.Rect.colliderect(pipes[i][1], bird.rect):
                run = False

        for x in deletion:
            del pipes[x]

        deletion = []

        display_score(window)

        pipe_count -= 1
        score += 1
        pygame.display.update()
    pygame.quit()
    with open("score.txt", 'r') as f:
        f_score = []
        for i in f.readlines():
            f_score.append(i.rstrip())
        if int(f_score[0]) < score:
            change_score = True
    if change_score:
        with open("score.txt", 'w') as f:
            pass
        with open("score.txt", 'w') as f:
            f.write(str(score))
        print("New Highscore: ")

    print(score)

def main():
    global clicked, speed, bg1_x, bg2_x, score, change_score, flappy_dist, pipe_verticle, pipes, deletion                                              

    menuwin = pygame.display.set_mode((500, 500))
    run = True
    while run:
        with open("score.txt", "r") as f:
            f_score = []
            for i in f.readlines():
                f_score.append(i.rstrip())
            currentHighscore = int(f_score[0])

        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or clicked['Play']:
                run = False
        
        menuwin.fill((255, 0, 255))

        type("valorax", f"Highscore: {currentHighscore}", (255,255,0), 250, 100, 30, menuwin)
        button(menuwin, 250, 300, 'PLAY', (255,0,255), (0,0,0), (255,255,0), 'valorax', 70, "Play")

        pygame.display.update()
    pygame.quit()

    if clicked['Play']:
        #RESET---------------------------------
        run = True
        speed = 1
        bg1_x, bg2_x = 0, window_height*ratio
        score = 0
        change_score = False
        #buttonVars
        clicked = {}
        clicked["Play"] = False
        #FlappyVars
        flappy_dist = 20
        #PipeVars
        pipe_verticle = 150
        pipes = {}
        deletion = []
        #----------------------------------------

        pygame.init()
        game()
        pygame.init()
        main()

if __name__ == "__main__":
    main()
