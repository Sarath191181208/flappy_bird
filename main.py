import os
import pygame
bird_img = pygame.image.load(os.path.join("assets","bird1.png"))

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

# Grav = Gravity
Grav = 3

class Bird():
    def __init__(self) -> None:
        self.x, self.y = 30,400
        self.vel = 0
        self.img = bird_img
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

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()
        draw(WIN, bird)

    pygame.quit()

if __name__ == "__main__":
    main()