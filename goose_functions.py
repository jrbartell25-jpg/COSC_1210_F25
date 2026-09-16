import pygame, random, math
import config_goose as config


def draw_title_screen(screen):
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 28)
    title = font_big.render("not that goose game", True, (255, 255, 255))
    msg = font_small.render("Press SPACE to start", True, (230, 230, 230))
    instr = font_small.render("get that bread, don't get hit by a ball", True, (211, 150, 18))
    rect1 = title.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 40))
    rect2 = msg.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 20))
    rect3 = instr.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 60))
    screen.blit(title, rect1)
    screen.blit(msg, rect2)
    screen.blit(instr, rect3)

def draw_hud(screen, score, breads_left):
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Bread: {score}  Left: {breads_left}", True, (240,240,240))
    screen.blit(text, (10, 8))

def game_over(screen, won, score):
    font_big = pygame.font.SysFont(None, 56)
    font_small = pygame.font.SysFont(None, 28)

    # Draw dark overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    # Text
    msg = "You Win!" if won else "Game Over!"
    t1 = font_big.render(msg, True, (255,255,255))
    t2 = font_small.render(f"Bread collected: {score}", True, (220,220,220))

    screen.blit(t1, t1.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 20)))
    screen.blit(t2, t2.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 20)))

    # Instructions
    play_again = font_small.render("SPACE to play again", True, (220,220,220))
    play_stop  = font_small.render("ESC to quit", True, (220,220,220))
    screen.blit(play_again, play_again.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 100)))
    screen.blit(play_stop, play_stop.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 130)))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_SPACE:
                    return "restart"

    
def reset_game():
    """Reset all game objects and return them."""
    px, py = config.WIDTH // 2, config.HEIGHT // 2
    facing = "R"
    breads = spawn_breads(config.N_BREAD)
    balls = spawn_balls(config.N_BALLS, config.BALL_SPEEDS)
    score = 0
    return px, py, facing, breads, balls, score

# Sprite functionS
_goose_img = None
_bread_img = None

def load_goose(frame="R"):
    global _goose_img
    paths = {
        "L":  config.PLAYER_IMAGE_L,
        "LS": config.PLAYER_IMAGE_LS,
        "R":  config.PLAYER_IMAGE_R,
        "RS": config.PLAYER_IMAGE_RS,
    }
    path = paths.get(frame, config.PLAYER_IMAGE_R)
    img = pygame.image.load(path).convert_alpha()
    _goose_img = pygame.transform.smoothscale(img, config.PLAYER_IMAGE_SIZE)

def draw_player(screen, x, y):
    # center the sprite on (x,y)
    if _goose_img is None:
        return
    rect = _goose_img.get_rect(center=(int(x), int(y)))
    screen.blit(_goose_img, rect)

def load_bread():
    global _bread_img
    img = pygame.image.load(config.BREAD_IMAGE).convert_alpha()
    _bread_img = pygame.transform.smoothscale(img, config.BREAD_IMAGE_SIZE)

def draw_bread(screen, center):
    if _bread_img is None:
        return
    rect = _bread_img.get_rect(center=(int(center[0]), int(center[1])))
    screen.blit(_bread_img, rect)
    return rect

# --------- Game objects ---------
class Ball:
    def __init__(self, x, y, vx, vy, color=None):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = float(vx), float(vy)
        self.r = config.BALL_RADIUS
        self.color = color or config.BALL_COLOR

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r*2, self.r*2)

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # bounce on walls
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx *= -1
        elif self.x + self.r >= config.WIDTH:
            self.x = config.WIDTH - self.r
            self.vx *= -1
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy *= -1
        elif self.y + self.r >= config.HEIGHT:
            self.y = config.HEIGHT - self.r
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)

class Bread:
    def __init__(self, x, y):
        self.x, self.y = int(x), int(y)

    @property
    def center(self):
        return (self.x, self.y)

    @property
    def rect(self):
        # approximate bread as a 20x20 rect centered on (x,y)
        w, h = config.BREAD_IMAGE_SIZE
        return pygame.Rect(self.x - w//2, self.y - h//2, w, h)

# --------- Utility placement ---------
def random_point(margin=30):
    return (
        random.randint(margin, config.WIDTH - margin),
        random.randint(margin, config.HEIGHT - margin),
    )

def spawn_breads(n):
    items = []
    for _ in range(n):
        x, y = random_point(40)
        items.append(Bread(x, y))
    return items

def spawn_balls(n, speeds):
    balls = []
    # start them spaced roughly across the screen
    cols = max(1, n)
    for i in range(n):
        x = config.HEIGHT // 10 + (config.BALL_RADIUS *2)
        y = random.randint(80, config.HEIGHT - 80)
        vx, vy = speeds[i % len(speeds)]
        balls.append(Ball(x, y, vx, vy))
    return balls

def spawn_new_ball():
    x = config.WIDTH // 2
    y = config.WIDTH // 2
    vx, vy = (170, 160)
    # start them spaced roughly across the screen
    return Ball(x,y,vx,vy)
