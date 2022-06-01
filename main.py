import os
import pygame
import random
import neat
import pickle

from timer import Timer

SCREEN_WIDTH, SCREEN_HEIGHT = 288, 512

BIRD_IMG = pygame.image.load(os.path.join("assets", "bird1.png"))
PIPE_IMG = pygame.image.load(os.path.join('assets', 'pipe.png'))
BACKGROUND = pygame.image.load(os.path.join('assets', "bg.png"))
GROUND_IMG = pygame.image.load(os.path.join('assets', "base.png"))

GEN = 1
HIGHEST_SO_FAR = 0


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def point_of_collision(mask, img, point):
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

        self.place_holder_timer = Timer(0.2)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def jump(self):
        if not self.place_holder_timer.start:
            self.place_holder_timer.start_timer()
            # think when jumped time resets to zero
            self.tick_seconds = 0
            # pygame coordinate system starts from top-left
            self.vel = -10

    def update(self):
        self.tick_seconds += 1
        self.place_holder_timer.update()
        # from s= ut +1/2 a t**2 := a = g
        global Grav
        y = (self.vel)*self.tick_seconds + Grav/2 * \
            (self.tick_seconds*self.tick_seconds)
        # terminal velocity
        y = 11 if y > 11 else y

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

        self.height = random.randint(50, self.top_img.get_height())
        self.y = self.height - self.top_img.get_height()
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
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False


class Text():
    def __init__(self, x, y, pre) -> None:
        self.val = 0
        self.x, self.y = x, y
        self.pre = pre

    def draw(self, win):
        txt = PYtxt(self.pre+str(self.val), 16)
        win.blit(txt, (self.x-txt.get_width()/2, self.y-txt.get_height()/2))


def draw(win, pipes, birds, *args):
    WHITE = pygame.Color('#ffffff')
    win.fill(WHITE)
    win.blit(BACKGROUND, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    for bird in birds:
        bird.draw(win)

    for arg in args:
        arg.draw(win)

    pygame.display.update()


class Ground():
    def __init__(self) -> None:
        self.WIDTH = GROUND_IMG.get_width()
        self.IMG = GROUND_IMG
        self.x1, self.x2 = 0, self.WIDTH
        self.y = SCREEN_HEIGHT-GROUND_IMG.get_height()+50
        self.vel = 5

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

    def update(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1+self.WIDTH < 0:
            self.x1 = self.x2+self.WIDTH
        if self.x2+self.WIDTH < 0:
            self.x2 = self.x1+self.WIDTH


def max_of_gens(gens):
    max_gene = gens[0]
    for gene in gens:
        if max_gene.fitness < gene.fitness:
            max_gene = gene
    return max_gene


def main(genomes, config):
    global GEN, HIGHEST_SO_FAR
    GEN += 1

    score = Text(SCREEN_WIDTH-40, 20, pre="Score : ")
    high_score = Text(SCREEN_WIDTH-70, 50, pre="High Score : ")
    alive = Text(50, 20, pre="Alive : ")
    generation = Text(70, 50, "Generation : ")
    generation.val = GEN

    gens = []
    nets = []
    birds = []

    # id, gene
    for _, gene in genomes:
        net = neat.nn.FeedForwardNetwork.create(gene, config)
        nets.append(net)
        birds.append(Bird())
        gene.fitness = 0
        gens.append(gene)

    pipes = [Pipe()]
    ground = Ground()
    run = True
    while run:
        alive.val = len(birds)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    max_player = max_of_gens(gens)
                    with open(f"./saves/{GEN}.pkl", "wb") as f:
                        pickle.dump(max_player, f)

        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].top_img.get_width():
                pipe_idx = 1

        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.update()
            gens[x].fitness += 0.1
            out = nets[x].activate((bird.y, abs(
                bird.y-pipes[pipe_idx].height), abs(bird.y-pipes[pipe_idx].bottom_y)))
            if out[0] > 0.5:
                bird.jump()

        rem_idxs = []
        add_pipe = False

        for idx, pipe in enumerate(pipes):
            pipe.update()
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    gens[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    gens.pop(x)
                    # score.val -= 1

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x+pipe.top_img.get_width() < 0:
                rem_idxs.append(idx)

        if add_pipe:
            for gene in gens:
                gene.fitness += 5
            score.val += 1
            pipes.append(Pipe())
        for gene in gens:
            gene.fitness += 5
        # you can't change an iterating array in python
        for idx in rem_idxs:
            pipes.pop(idx)

        for idx, bird in enumerate(birds):
            if bird.y >= ground.y + bird.img.get_height() or bird.y < 30:
                gens[idx].fitness -= 10
                birds.pop(idx)
                nets.pop(idx)
                gens.pop(idx)

        HIGHEST_SO_FAR = max(score.val, HIGHEST_SO_FAR)
        high_score.val = HIGHEST_SO_FAR
        ground.update()
        draw(WIN, pipes, birds, score, ground, alive, generation, high_score)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Create the population
    p = neat.Population(config)

    # Add a print to show progress
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(main, 10000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    print(HIGHEST_SO_FAR)


def replay_genome(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    local_dir = os.path.dirname(__file__)
    gen_path = os.path.join(local_dir, "two.pkl")
    with open(gen_path, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    main(genomes, config)


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    FPS = 30
    # main()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'feedforward.txt')
    # run(config_path)
    replay_genome(config_path)
