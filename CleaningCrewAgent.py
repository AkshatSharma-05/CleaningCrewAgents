import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Cleaning Crew Simulation")

# Colors
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
FLOOR = (220, 220, 220)
TILE = (200, 200, 200)
ROBOT_BODY = (120, 120, 255)
ROBOT_WITH_TRASH = (255, 180, 80)

# Crew settings
NUM_CLEANERS = 5
CREW_SPEED = 2.0
DIRT_COUNT = 20

# Clock
clock = pygame.time.Clock()
FPS = 60

# Dustbin location
DUSTBIN = (WIDTH - 90, HEIGHT - 90)
DUSTBIN_SIZE = 60

# Utility functions
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def move_towards(src_x, src_y, tx, ty, speed):
    dx = tx - src_x
    dy = ty - src_y
    dist = math.hypot(dx, dy)
    if dist == 0:
        return src_x, src_y, True
    if dist <= speed:
        return tx, ty, True
    nx = src_x + (dx / dist) * speed
    ny = src_y + (dy / dist) * speed
    return nx, ny, False

# Cleaner class (robot-like)
class Cleaner:
    def __init__(self, x, y, id_num=0):
        self.x = float(x)
        self.y = float(y)
        self.target = None
        self.has_garbage = False
        self.id = id_num
        # small randomness to robot appearance
        self.color = ROBOT_BODY
        self.size_scale = random.uniform(0.9, 1.15)

    def set_target(self, t):
        self.target = t

    def move_towards_target(self):
        if not self.target:
            return False
        tx, ty = self.target
        self.x, self.y, reached = move_towards(self.x, self.y, tx, ty, CREW_SPEED)
        return reached

    def draw(self):
        # robot dimensions (scaleable)
        head_size = int(18 * self.size_scale)
        body_width = int(18 * self.size_scale)
        body_height = int(26 * self.size_scale)
        arm_length = int(12 * self.size_scale)
        leg_length = int(12 * self.size_scale)

        body_color = self.color if not self.has_garbage else ROBOT_WITH_TRASH
        eye_color = BLACK

        # Head (square)
        head_rect = pygame.Rect(int(self.x - head_size // 2), int(self.y - 36), head_size, head_size)
        pygame.draw.rect(WIN, body_color, head_rect, border_radius=4)
        pygame.draw.rect(WIN, BLACK, head_rect, 2, border_radius=4)

        # Antenna
        ant_top = (int(self.x), int(self.y - 46))
        ant_bottom = (int(self.x), int(self.y - 36))
        pygame.draw.line(WIN, body_color, ant_bottom, ant_top, 3)
        pygame.draw.circle(WIN, YELLOW, (ant_top[0], ant_top[1] - 4), 4)

        # Eyes that look toward target slightly
        eye_offset_x = int(6 * self.size_scale)
        eye_y = int(self.y - 28)
        dx = dy = 0
        if self.target:
            tx, ty = self.target
            vx = tx - self.x
            vy = ty - self.y
            vlen = math.hypot(vx, vy)
            if vlen > 0:
                # small movement factor so eyes shift subtly
                factor = min(3, vlen * 0.03)
                dx = (vx / vlen) * factor
                dy = (vy / vlen) * factor

        pygame.draw.circle(WIN, eye_color, (int(self.x - eye_offset_x + dx), int(eye_y + dy)), max(2, int(3 * self.size_scale)))
        pygame.draw.circle(WIN, eye_color, (int(self.x + eye_offset_x + dx), int(eye_y + dy)), max(2, int(3 * self.size_scale)))

        # Body
        body_rect = pygame.Rect(int(self.x - body_width//2), int(self.y - 15), body_width, body_height)
        pygame.draw.rect(WIN, body_color, body_rect, border_radius=6)
        pygame.draw.rect(WIN, BLACK, body_rect, 2, border_radius=6)

        # Arms (metal rods)
        left_arm_start = (int(self.x - body_width//2), int(self.y))
        left_arm_end = (int(self.x - body_width//2 - arm_length), int(self.y + 6))
        right_arm_start = (int(self.x + body_width//2), int(self.y))
        right_arm_end = (int(self.x + body_width//2 + arm_length), int(self.y + 6))
        pygame.draw.line(WIN, body_color, left_arm_start, left_arm_end, max(3, int(3 * self.size_scale)))
        pygame.draw.line(WIN, BLACK, left_arm_start, left_arm_end, 1)
        pygame.draw.line(WIN, body_color, right_arm_start, right_arm_end, max(3, int(3 * self.size_scale)))
        pygame.draw.line(WIN, BLACK, right_arm_start, right_arm_end, 1)

        # Legs
        left_leg_start = (int(self.x - body_width//4), int(self.y + body_height))
        left_leg_end = (left_leg_start[0], int(self.y + body_height + leg_length))
        right_leg_start = (int(self.x + body_width//4), int(self.y + body_height))
        right_leg_end = (right_leg_start[0], int(self.y + body_height + leg_length))
        pygame.draw.line(WIN, body_color, left_leg_start, left_leg_end, max(3, int(3 * self.size_scale)))
        pygame.draw.line(WIN, BLACK, left_leg_start, left_leg_end, 1)
        pygame.draw.line(WIN, body_color, right_leg_start, right_leg_end, max(3, int(3 * self.size_scale)))
        pygame.draw.line(WIN, BLACK, right_leg_start, right_leg_end, 1)

        # optional small ID text above body
        try:
            font_small = pygame.font.SysFont(None, 16)
            id_surf = font_small.render(f"R{self.id}", True, BLACK)
            WIN.blit(id_surf, (int(self.x - id_surf.get_width()//2), int(self.y - 54)))
        except Exception:
            pass

# Generate dirt spots (avoid spawning on dustbin)
def generate_dirt(count):
    spots = []
    for _ in range(count):
        while True:
            x = random.randint(50, WIDTH-150)
            y = random.randint(50, HEIGHT-150)
            # simple avoidance of dustbin area
            if not (DUSTBIN[0] - 20 < x < DUSTBIN[0] + DUSTBIN_SIZE + 20 and DUSTBIN[1] - 20 < y < DUSTBIN[1] + DUSTBIN_SIZE + 20):
                spots.append((x, y))
                break
    return spots

dirt_spots = generate_dirt(DIRT_COUNT)

# Generate cleaners
cleaners = [Cleaner(random.randint(60, WIDTH-160), random.randint(60, HEIGHT-160), id_num=i+1) for i in range(NUM_CLEANERS)]

# Main loop
running = True
font = pygame.font.SysFont(None, 24)
while running:
    clock.tick(FPS)

    # Draw floor tiles
    WIN.fill(FLOOR)
    tile_size = 50
    for x in range(0, WIDTH, tile_size):
        for y in range(0, HEIGHT, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            color = TILE if (x//tile_size + y//tile_size) % 2 == 0 else FLOOR
            pygame.draw.rect(WIN, color, rect)

    # Draw dustbin
    pygame.draw.rect(WIN, GREEN, (*DUSTBIN, DUSTBIN_SIZE, DUSTBIN_SIZE))
    pygame.draw.rect(WIN, BLACK, (*DUSTBIN, DUSTBIN_SIZE, DUSTBIN_SIZE), 2)
    WIN.blit(font.render("Dustbin", True, BLACK), (DUSTBIN[0] - 6, DUSTBIN[1] - 24))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Add dirt by clicking
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            dirt_spots.append((mx, my))

    # Coordinator assigns tasks to each robot
    for cleaner in cleaners:
        # If robot doesn't have garbage, assign nearest dirt if it doesn't have a valid target
        if not cleaner.has_garbage:
            # If their target is invalid or None, pick nearest dirt
            if not cleaner.target or cleaner.target not in dirt_spots:
                if dirt_spots:
                    nearest = min(dirt_spots, key=lambda d: (d[0]-cleaner.x)**2 + (d[1]-cleaner.y)**2)
                    cleaner.set_target(nearest)
                else:
                    cleaner.set_target(None)
        else:
            # Head for dustbin center
            cleaner.set_target((DUSTBIN[0] + DUSTBIN_SIZE//2, DUSTBIN[1] + DUSTBIN_SIZE//2))

        # Move cleaner and check if reached
        reached = cleaner.move_towards_target()
        if reached and cleaner.target:
            # If reaching dirt and not carrying anything, pick it up
            if not cleaner.has_garbage and cleaner.target in dirt_spots:
                try:
                    dirt_spots.remove(cleaner.target)
                except ValueError:
                    pass
                cleaner.has_garbage = True
                # set dustbin as next target
                cleaner.set_target((DUSTBIN[0] + DUSTBIN_SIZE//2, DUSTBIN[1] + DUSTBIN_SIZE//2))
            # If reached dustbin with garbage, drop it
            elif cleaner.has_garbage:
                cleaner.has_garbage = False
                cleaner.set_target(None)

        cleaner.draw()

    # Draw dirt spots
    for dirt in dirt_spots:
        pygame.draw.circle(WIN, RED, (int(dirt[0]), int(dirt[1])), 8)
        pygame.draw.circle(WIN, BLACK, (int(dirt[0]), int(dirt[1])), 8, 2)

    # HUD: remaining dirt
    hud = font.render(f"Dirt remaining: {len(dirt_spots)}    Robots: {len(cleaners)}    (Click to add dirt)", True, BLACK)
    WIN.blit(hud, (10, 10))

    pygame.display.update()

pygame.quit()

