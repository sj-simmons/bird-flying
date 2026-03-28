import pygame, sys
from pygame.locals import *
from random import randint

winWidth = 900
winHeight = 700
FPS = 10
AI = None


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

        # Keep the bird on screen.
        self.x = max(0, min(winWidth, self.x))
        self.y = max(0, min(winHeight, self.y))

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

    global AI

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
    textSurface6 = largeFont.render("Type m for minimax or e for expectimax.", True, (0, 0, 0))
    textRect1 = textSurface1.get_rect()
    textRect2 = textSurface2.get_rect()
    textRect3 = textSurface3.get_rect()
    textRect4 = textSurface4.get_rect()
    textRect5 = textSurface5.get_rect()
    textRect6 = textSurface6.get_rect()
    textRect1.center = (winWidth / 2, 2 * winHeight / 5)
    textRect2.center = (winWidth / 2, winHeight / 2)
    textRect3.center = (winWidth / 2, 3 * winHeight / 5)
    textRect4.center = (int(winWidth / 2), int(4 * winHeight / 5))
    textRect5.center = (int(winWidth / 2), int(winHeight / 7))
    textRect6.center = (int(winWidth / 2), int(9 * winHeight / 10))
    screen.blit(textSurface1, textRect1)
    screen.blit(textSurface2, textRect2)
    screen.blit(textSurface3, textRect3)
    screen.blit(textSurface4, textRect4)
    screen.blit(textSurface5, textRect5)
    screen.blit(textSurface6, textRect6)

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
            elif event.type == KEYUP and event.key == K_m:
                AI = "minimax"
                return True
            elif event.type == KEYUP and event.key == K_e:
                AI = "expectimax"
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


def minimax(bird, nest, bubbles, depth=4):
    bx, by = bird.x, bird.y
    nx, ny = nest.x, nest.y
    nest_mt = nest.move_to
    bird_radius = bird.radius
    bub_states = [(b.x, b.y, b.t, b.speed, b.outer_radius) for b in bubbles]

    def evaluate(bx, by, nx, ny, bubs):
        dist_to_nest = ((bx - nx) ** 2 + (by - ny) ** 2) ** 0.5
        if dist_to_nest < 10:
            return 10000
        min_margin = float("inf")
        for bbx, bby, _, _, b_or in bubs:
            dist = ((bx - bbx) ** 2 + (by - bby) ** 2) ** 0.5
            collision_dist = (b_or + bird_radius) * 0.8
            margin = dist - collision_dist
            if margin < min_margin:
                min_margin = margin
        if min_margin < 0:
            return -10000
        score = -dist_to_nest + 3.0 * min(min_margin, 150)
        if min_margin < 40:
            score -= 500 * (40 - min_margin) / 40
        return score

    def clamp(x, y):
        return max(0, min(winWidth, x)), max(0, min(winHeight, y))

    def gen_moves(bx, by, nx, ny):
        step = 120
        moves = [
            (nx, ny),  # straight to nest
            (bx + step, by),
            (bx - step, by),
            (bx, by + step),
            (bx, by - step),
            (bx + step, by + step),
            (bx + step, by - step),
            (bx - step, by + step),
            (bx - step, by - step),
        ]
        return [clamp(mx, my) for mx, my in moves]

    def sim_step(bx, by, nx, ny, n_mt, bubs, move):
        nbx = bx + (move[0] - bx) / 10
        nby = by + (move[1] - by) / 10
        nbx, nby = clamp(nbx, nby)
        nnx = nx + (n_mt[0] - nx) / 125
        nny = ny + (n_mt[1] - ny) / 125
        new_bubs = []
        for bbx, bby, t, spd, b_or in bubs:
            nbbx = bbx + ((1 - t) * nbx + t * nnx - bbx) / spd
            nbby = bby + ((1 - t) * nby + t * nny - bby) / spd
            new_bubs.append((nbbx, nbby, t, spd, b_or))
        return nbx, nby, nnx, nny, new_bubs

    def search(bx, by, nx, ny, n_mt, bubs, d):
        if d == 0:
            return evaluate(bx, by, nx, ny, bubs), None
        best_score = float("-inf")
        best_move = (nx, ny)
        for move in gen_moves(bx, by, nx, ny):
            nbx, nby, nnx, nny, new_bubs = sim_step(
                bx, by, nx, ny, n_mt, bubs, move
            )
            score, _ = search(nbx, nby, nnx, nny, n_mt, new_bubs, d - 1)
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    _, best_move = search(bx, by, nx, ny, nest_mt, bub_states, depth)
    return best_move


def expectimax(bird, nest, bubbles, depth=4):
    bx, by = bird.x, bird.y
    nx, ny = nest.x, nest.y
    nest_mt = nest.move_to
    bird_radius = bird.radius
    bub_states = [(b.x, b.y, b.t, b.speed, b.outer_radius) for b in bubbles]

    frames_per_step = 4
    # Probability the nest picks a new random target during frames_per_step frames
    p_change = 1 - 0.99 ** frames_per_step  # ≈ 0.04
    # Representative targets that sample the screen for the chance node
    nr = nest.radius
    rand_targets = [
        (winWidth * 0.25, winHeight * 0.25),
        (winWidth * 0.75, winHeight * 0.25),
        (winWidth * 0.25, winHeight * 0.75),
        (winWidth * 0.75, winHeight * 0.75),
    ]

    def clamp(x, y):
        return max(0, min(winWidth, x)), max(0, min(winHeight, y))

    def evaluate(bx, by, nx, ny, bubs):
        dist_to_nest = ((bx - nx) ** 2 + (by - ny) ** 2) ** 0.5
        if dist_to_nest < 10:
            return 10000
        min_margin = float("inf")
        for bbx, bby, _, _, b_or in bubs:
            m = ((bx - bbx) ** 2 + (by - bby) ** 2) ** 0.5 - (b_or + bird_radius) * 0.8
            if m < min_margin:
                min_margin = m
        if min_margin < 0:
            return -10000
        path_min = float("inf")
        for step in range(1, 6):
            t = step / 6.0
            px, py = bx + t * (nx - bx), by + t * (ny - by)
            for bbx, bby, _, _, b_or in bubs:
                m = ((px - bbx) ** 2 + (py - bby) ** 2) ** 0.5 - (b_or + bird_radius) * 0.8
                if m < path_min:
                    path_min = m
        score = min(path_min, 100) * 5.0 + max(0.0, 300 - dist_to_nest)
        if dist_to_nest < 80:
            score += (80 - dist_to_nest) * 25.0
        safety_weight = min(dist_to_nest / 80.0, 1.0)
        if min_margin < 50:
            score -= 300 * (50 - min_margin) / 50 * safety_weight
        edge = 40
        if bx < edge:             score -= 200 * (edge - bx) / edge
        if bx > winWidth - edge:  score -= 200 * (bx - (winWidth - edge)) / edge
        if by < edge:             score -= 200 * (edge - by) / edge
        if by > winHeight - edge: score -= 200 * (by - (winHeight - edge)) / edge
        return score

    def gen_moves(bx, by, nx, ny, bubs):
        step = 200
        moves = [
            (bx, by),
            (nx, ny),
            (10 * nx - 9 * bx, 10 * ny - 9 * by),  # lands on nest in 1 frame
            (bx + step, by), (bx - step, by), (bx, by + step), (bx, by - step),
            (bx + step, by + step), (bx + step, by - step),
            (bx - step, by + step), (bx - step, by - step),
        ]
        nearest_dist = float("inf")
        nearest_bub = None
        for bbx, bby, _, _, _ in bubs:
            d = ((bx - bbx) ** 2 + (by - bby) ** 2) ** 0.5
            if d < nearest_dist:
                nearest_dist, nearest_bub = d, (bbx, bby)
        if nearest_bub is not None:
            dx, dy = bx - nearest_bub[0], by - nearest_bub[1]
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length > 0:
                dx, dy = dx / length, dy / length
                moves += [(bx + dy * step, by - dx * step),
                          (bx - dy * step, by + dx * step),
                          (bx + dx * step, by + dy * step)]
        return [clamp(mx, my) for mx, my in moves]

    def sim(bx, by, nx, ny, n_mt, bubs, move, frames):
        for _ in range(frames):
            bx = bx + (move[0] - bx) / 10
            by = by + (move[1] - by) / 10
            bx, by = clamp(bx, by)
            nx = nx + (n_mt[0] - nx) / 125
            ny = ny + (n_mt[1] - ny) / 125
            new_bubs, min_margin = [], float("inf")
            for bbx, bby, t, spd, b_or in bubs:
                nbbx = bbx + ((1 - t) * bx + t * nx - bbx) / spd
                nbby = bby + ((1 - t) * by + t * ny - bby) / spd
                new_bubs.append((nbbx, nbby, t, spd, b_or))
                m = ((bx - nbbx) ** 2 + (by - nbby) ** 2) ** 0.5 - (b_or + bird_radius) * 0.8
                if m < min_margin:
                    min_margin = m
            bubs = new_bubs
            if min_margin < 0:
                return bx, by, nx, ny, bubs, False, True
            if ((bx - nx) ** 2 + (by - ny) ** 2) ** 0.5 < 10:
                return bx, by, nx, ny, bubs, True, False
        return bx, by, nx, ny, bubs, False, False

    def search(bx, by, nx, ny, n_mt, bubs, d):
        if d == 0:
            return evaluate(bx, by, nx, ny, bubs), None

        # Order moves with a cheap 1-frame sim
        moves = gen_moves(bx, by, nx, ny, bubs)
        scored = []
        for move in moves:
            nbx, nby, nnx, nny, nb, won, died = sim(bx, by, nx, ny, n_mt, bubs, move, 1)
            s = 10000 if won else (-10000 if died else evaluate(nbx, nby, nnx, nny, nb))
            scored.append((s, move))
        scored.sort(reverse=True, key=lambda x: x[0])

        best_score, best_move = float("-inf"), (nx, ny)
        for move in [m for _, m in scored[:4]]:
            nbx, nby, nnx, nny, nb, won, died = sim(bx, by, nx, ny, n_mt, bubs, move, frames_per_step)
            if won:
                return 10000, move
            if died:
                score = -10000
            elif d == 1:
                # Chance node: expected value over nest target uncertainty.
                # Re-sim with each candidate target and take weighted average.
                score = (1 - p_change) * evaluate(nbx, nby, nnx, nny, nb)
                for t in rand_targets:
                    rb2x, rb2y, rn2x, rn2y, rb2, rw, rd = sim(
                        bx, by, nx, ny, t, bubs, move, frames_per_step
                    )
                    rs = 10000 if rw else (-10000 if rd else evaluate(rb2x, rb2y, rn2x, rn2y, rb2))
                    score += (p_change / len(rand_targets)) * rs
            else:
                score = search(nbx, nby, nnx, nny, n_mt, nb, d - 1)[0]

            if score > best_score:
                best_score, best_move = score, move
            if best_score >= 10000:
                break

        return best_score, best_move

    _, best_move = search(bx, by, nx, ny, nest_mt, bub_states, depth)
    return best_move


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
                if not AI:
                    mouse = event.pos

        if AI == "minimax":
            mouse = minimax(bird, nest, bubbles)
        elif AI == "expectimax":
            mouse = expectimax(bird, nest, bubbles)

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
