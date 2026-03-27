import pygame, sys
from pygame.locals import *
from random import randint

winWidth = 900
winHeight = 700
FPS = 10


class Circ(pygame.sprite.Sprite):
    def __init__(self, screen, color, outer_color, x, y, radius, outer_radius):
        super().__init__()  # Circ inherits from pygame's Sprite class.
        self.screen = screen
        self.color = color
        self.outer_color = outer_color
        self.x = x
        self.y = y
        self.radius = radius
        self.outer_radius = outer_radius
        self.image = pygame.Surface(
            [2 * self.outer_radius, 2 * self.outer_radius], pygame.SRCALPHA, 32
        ).convert_alpha()
        self.image.fill((255, 255, 255, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(
            self.image,
            self.outer_color,
            (self.outer_radius, self.outer_radius),
            self.outer_radius,
        )
        pygame.draw.circle(
            self.image, self.color, (self.outer_radius, self.outer_radius), self.radius
        )

    def draw(self):
        self.screen.blit(
            self.image, (self.x - self.outer_radius, self.y - self.outer_radius)
        )
        self.rect.center = (self.x, self.y)


class Bubble(Circ):
    def __init__(
        self,
        screen,
        color=(70, 130, 180, 100),
        outer_color=(70, 130, 180, 150),
        x=2 * winWidth / 3,
        y=5 * winHeight / 8,
        radius=60,
        t=0.3,
        speed=50,
    ):
        self.t = t
        outer_radius = int(1.05 * radius)
        self.speed = speed
        super().__init__(screen, color, outer_color, x, y, radius, outer_radius)

    def update(self, bird, nest):
        # Move the Bubble toward the point determined by t lying on the line
        # connecting the bird and the nest.
        self.x += ((1 - self.t) * bird.x + self.t * nest.x - self.x) / self.speed
        self.y += ((1 - self.t) * bird.y + self.t * nest.y - self.y) / self.speed
        self.draw()


class Nest(Circ):
    def __init__(
        self,
        screen,
        color=(218, 165, 32),
        outer_color=(138, 69, 19, 200),
        x=7 * winWidth / 8,
        y=5 * winHeight / 6,
        radius=30,
    ):
        outer_radius = int(1.25 * radius)
        super().__init__(screen, color, outer_color, x, y, radius, outer_radius)
        self.move_to = randint(self.radius, winWidth - self.radius), randint(
            self.radius, winHeight - self.radius
        )

    def update(self):
        if randint(0, 100) < 1:
            self.move_to = randint(self.radius, winWidth - self.radius), randint(
                self.radius, winHeight - self.radius
            )

        # Move the nest toward a randomly chosen point.
        self.x += (self.move_to[0] - self.x) / 125
        self.y += (self.move_to[1] - self.y) / 125

        self.draw()


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen, x=winWidth / 8, y=winHeight / 6):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.images = []
        self.images.append(pygame.image.load("birdFlying1.png").convert_alpha())
        self.images.append(pygame.image.load("birdFlying2.png").convert_alpha())
        self.images.append(pygame.image.load("birdFlying3.png").convert_alpha())
        self.images.append(pygame.image.load("birdFlying4.png").convert_alpha())
        self.images.append(pygame.image.load("birdFlying5.png").convert_alpha())
        self.count = 0
        self.radius = 10  # for collision_circle

    def update(self, mouse):
        # Make the bird fly towards the mouse cursor.
        dx = mouse[0] - self.x
        self.x += dx / 10
        self.y += (mouse[1] - self.y) / 10

        # Cycle through the birdflying images.
        self.count += 1
        self.count = self.count % len(self.images)
        image = self.images[self.count]

        # If the bird is moving left reflect the image horizontally (but not vertically)
        if dx < 0:
            image = pygame.transform.flip(image, True, False)

        self.rect = image.get_rect()
        self.rect.center = (self.x, self.y)
        self.screen.blit(image, (self.x - self.rect[2] / 2, self.y - self.rect[3] / 2))


def captured(screen, wins, losses):
    smallFont = pygame.font.SysFont("Arial", 50)
    largeFont = pygame.font.SysFont("Arial", 80)
    largerFont = pygame.font.SysFont("Arial", 100)
    textSurface1 = largeFont.render("You let the bird get", True, (155, 0, 0))
    textSurface2 = largerFont.render("captured!", True, (155, 0, 0))
    textSurface3 = largeFont.render("Click to try again.", True, (0, 0, 0))
    textSurface4 = smallFont.render(
        "Wins: " + str(wins) + "  Losses: " + str(losses), True, (100, 100, 0)
    )
    textRect1 = textSurface1.get_rect()
    textRect2 = textSurface2.get_rect()
    textRect3 = textSurface3.get_rect()
    textRect4 = textSurface4.get_rect()
    textRect1.center = (winWidth / 2, winHeight / 3)
    textRect2.center = (winWidth / 2, winHeight / 2)
    textRect3.center = (int(winWidth / 2), int(2 * winHeight / 3))
    textRect4.center = (int(winWidth / 2), int(4 * winHeight / 5))
    screen.blit(textSurface1, textRect1)
    screen.blit(textSurface2, textRect2)
    screen.blit(textSurface3, textRect3)
    screen.blit(textSurface4, textRect4)

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                paused = False
                break

        pygame.display.update()
        fpsClock.tick(FPS)


def won(screen, wins, losses, applause):
    smallFont = pygame.font.SysFont("Arial", 40)
    largeFont = pygame.font.SysFont("Arial", 60)
    largerFont = pygame.font.SysFont("Arial", 80)
    textSurface1 = largeFont.render("The bird got to her nest", True, (200, 0, 200))
    textSurface2 = largerFont.render("YOU WIN!", True, (255, 0, 255))
    textSurface3 = largeFont.render("Click to play again.", True, (0, 100, 100))
    textSurface4 = smallFont.render(
        "Wins: " + str(wins) + "  Losses: " + str(losses), True, (100, 100, 0)
    )
    textRect1 = textSurface1.get_rect()
    textRect2 = textSurface2.get_rect()
    textRect3 = textSurface3.get_rect()
    textRect4 = textSurface4.get_rect()
    textRect1.center = (winWidth / 2, winHeight / 3)
    textRect2.center = (winWidth / 2, winHeight / 2)
    textRect3.center = (int(winWidth / 2), int(2 * winHeight / 3))
    textRect4.center = (int(winWidth / 2), int(4 * winHeight / 5))
    screen.blit(textSurface1, textRect1)
    screen.blit(textSurface2, textRect2)
    screen.blit(textSurface3, textRect3)
    screen.blit(textSurface4, textRect4)

    applause.play()

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                paused = False
                break

        pygame.display.update()
        fpsClock.tick(FPS)


def info(screen):
    unicode_font = pygame.font.Font("Cyberbit.ttf", 80)
    largeFont = pygame.font.SysFont("Arial", 35)
    textSurface1 = largeFont.render(
        "Move the mouse to guide the bird", True, (155, 0, 0)
    )
    textSurface2 = largeFont.render(
        "into the golden nest without getting", True, (155, 0, 0)
    )
    textSurface3 = largeFont.render("captured by the blue bubbles.", True, (155, 0, 0))
    textSurface4 = largeFont.render("Click to play.", True, (0, 0, 0))
    textSurface5 = unicode_font.render("一只鸟在飞", True, (0, 0, 0))
    textRect1 = textSurface1.get_rect()
    textRect2 = textSurface2.get_rect()
    textRect3 = textSurface3.get_rect()
    textRect4 = textSurface4.get_rect()
    textRect5 = textSurface5.get_rect()
    textRect1.center = (winWidth / 2, 2 * winHeight / 5)
    textRect2.center = (winWidth / 2, winHeight / 2)
    textRect3.center = (winWidth / 2, 3 * winHeight / 5)
    textRect4.center = (int(winWidth / 2), int(4 * winHeight / 5))
    textRect5.center = (int(winWidth / 2), int(winHeight / 7))
    screen.blit(textSurface1, textRect1)
    screen.blit(textSurface2, textRect2)
    screen.blit(textSurface3, textRect3)
    screen.blit(textSurface4, textRect4)
    screen.blit(textSurface5, textRect5)

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True

        pygame.display.update()
        fpsClock.tick(FPS)


def add_bubbles(screen, bubbles):
    for i in range(6, 20):
        bubbles.add(
            Bubble(
                screen,
                (70, 130, 180, 100),
                (70, 130, 180, 150),
                winWidth / 2,
                winHeight / 2,
                int((0.3 * i) ** 2 * 1.5),  # size
                (0.9 * i) ** 0.85 * 0.1 - 0.3,  # position
                1 + 0.2 * i**1.5,  # speed
            )
        )


def main():

    global fpsClock

    pygame.init()
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("Flying Bird")

    background_image = pygame.image.load("clouds.jpg").convert()
    applause = pygame.mixer.Sound("crowdapplause1.wav")
    pygame.mixer.music.load("bird-sound.mp3")
    pygame.mixer.music.play(-1)
    bubbles = pygame.sprite.Group()
    nest = Nest(screen)
    add_bubbles(screen, bubbles)
    bird = Bird(screen)
    mouse = 7 * winWidth / 8, 5 * winHeight / 6
    started_the_first_time = False
    wins = losses = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse = event.pos

        screen.blit(background_image, (0, 0))

        nest.update()
        bubbles.update(bird, nest)
        bird.update(mouse)

        if not started_the_first_time:
            started_the_first_time = info(screen)

        if pygame.sprite.spritecollideany(
            bird, bubbles, pygame.sprite.collide_circle_ratio(0.8)
        ):
            losses += 1
            captured(screen, wins, losses)

            # delete the old objects
            del bird, nest
            for bubble in bubbles:
                del bubble
            bubbles.empty()

            # create new ones
            nest = Nest(screen)
            bird = Bird(screen)
            add_bubbles(screen, bubbles)

        elif (
            abs(bird.rect.center[0] - nest.rect.center[0]) < 10
            and abs(bird.rect.center[1] - nest.rect.center[1]) < 10
        ):
            wins += 1
            won(screen, wins, losses, applause)

            # delete the old objects
            del bird, nest
            for bubble in bubbles:
                del bubble
            bubbles.empty()

            # create new ones
            nest = Nest(screen)
            bird = Bird(screen)
            add_bubbles(screen, bubbles)

        pygame.display.update()

        fpsClock.tick(FPS)


main()
