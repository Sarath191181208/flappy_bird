import os
import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 288, 512

BIRD_IMG = pygame.image.load(os.path.join("assets","bird1.png"))
PIPE_IMG = pygame.image.load(os.path.join('assets','pipe.png'))
BACKGROUND = pygame.image.load(os.path.join('assets',"bg.png"))
GROUND_IMG = pygame.image.load(os.path.join('assets',"base.png"))

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)
def point_of_collision(mask , img, point):
    img_mask = pygame.mask.from_surface(img)
    return mask.overlap(img_mask, point)
# Grav = Gravity
Grav = 3

class Bird():
    def __init__(self) -> None:
        self.x, self.y = 50, SCREEN_HEIGHT*0.7
        self.vel = 0
        self.img = BIRD_IMG
        self.tick_seconds = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def jump(self):
        # think when jumped time resets to zero
        self.tick_seconds = 0
        # pygame coordinate system starts from top-left 
        self.vel = -11
    
    def update(self):
        self.tick_seconds += 1

        # from s= ut +1/2 a t**2 := a = g
        global Grav
        y = (self.vel)*self.tick_seconds + Grav/2 * (self.tick_seconds*self.tick_seconds)
        # terminal velocity 
        y = 11 if y>11 else y

        self.y += y
        self.y = self.y if self.y < SCREEN_HEIGHT else SCREEN_HEIGHT
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe():
    def __init__(self) -> None:
        self.vel = 5
        self.x = SCREEN_WIDTH+50
        self.gap = 150

        # placeholder variable to stop scoring multiple times
        self.passed = False

        self.top_img = pygame.transform.rotate(PIPE_IMG, 180)
        self.bottom_img = PIPE_IMG

        self.y = random.randint(50, self.top_img.get_height())- self.top_img.get_height()
        self.top_y, self.bottom_y = self.y, self.y+self.gap+self.top_img.get_height()
    
    def draw(self, win):
        win.blit(self.top_img, (self.x, self.top_y))
        win.blit(self.bottom_img, (self.x, self.bottom_y))
    
    def update(self):
        self.x -= self.vel
    
    def collide(self, bird):
        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(self.top_img)
        bottom_mask = pygame.mask.from_surface(self.bottom_img)

        top_offset = (self.x - bird.x, self.top_y - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_y - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

class Text():
    def __init__(self, x, y) -> None:
        self.val = 0
        self.x, self.y = x, y
    def draw(self,win):
        txt = PYtxt("Score : "+str(self.val),13)
        win.blit(txt, (self.x-txt.get_width()/2, self.y-txt.get_height()/2) )


def draw(win, pipes, *args):
    WHITE = pygame.Color('#ffffff')
    win.fill(WHITE)
    win.blit(BACKGROUND, (0,0))
    for pipe in pipes:
        pipe.draw(win)

    for arg in args:
        arg.draw(win)

    pygame.display.update()

class Ground():
    def __init__(self) -> None:
        self.WIDTH =  GROUND_IMG.get_width()
        self.IMG = GROUND_IMG
        self.x1, self.x2 = 0, self.WIDTH
        self.y = SCREEN_HEIGHT-GROUND_IMG.get_height()+50
        self.vel = 5
    
    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

    def update(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1+self.WIDTH < 0:
            self.x1 = self.x2+self.WIDTH
        if self.x2+self.WIDTH < 0:
            self.x2 = self.x1+self.WIDTH

def main():
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    FPS = 30

    score = Text(SCREEN_WIDTH-30,20)

    bird = Bird()
    pipes = [Pipe()]
    ground = Ground()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        rem_idxs = []
        for idx, pipe in enumerate(pipes):
            pipe.update()
            if pipe.collide(bird):
                score.val -= 1

            if not pipe.passed and pipe.x < bird.x:
                score.val += 1
                pipe.passed = True

            if pipe.x+pipe.top_img.get_width() < 0:
                rem_idxs.append(idx)
                pipes.append(Pipe())

        # you can't change an iterating array in python
        for idx in rem_idxs:
            pipes.pop(idx)

        bird.update()
        ground.update()
        draw(WIN, pipes, bird, score, ground)

    pygame.quit()

if __name__ == "__main__":
    main()