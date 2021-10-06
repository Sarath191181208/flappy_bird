import os
import pygame
import random

BIRD_IMG = pygame.image.load(os.path.join("assets","bird1.png"))
PIPE_IMG = pygame.image.load(os.path.join('assets','pipe.png'))

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

# Grav = Gravity
Grav = 3

class Bird():
    def __init__(self) -> None:
        self.x, self.y = 30,400
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
        self.y = self.y if self.y < 550 else 550

class Pipe():
    def __init__(self) -> None:
        self.vel = 5
        self.x = 400
        self.gap = 200
        self.top_img = pygame.transform.rotate(PIPE_IMG, 180)
        self.bottom_img = PIPE_IMG
        self.y = random.randint(50,400)- self.top_img.get_height()
        print(self.y)
    
    def draw(self, win):
        win.blit(self.top_img, (self.x,self.y))
        win.blit(self.bottom_img, (self.x, self.y+self.gap+self.top_img.get_height()))
    
    def update(self):
        self.x -= self.vel


def draw(win, *args):
    WHITE = pygame.Color('#ffffff')
    win.fill(WHITE)

    for arg in args:
        arg.draw(win)
    
    pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((500,600))
    pygame.display.set_caption('Flappy Bird')
    FPS = 30

    bird = Bird()
    pipe = Pipe()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        pipe.update()
        bird.update()
        draw(WIN, bird,pipe)

    pygame.quit()

if __name__ == "__main__":
    main()