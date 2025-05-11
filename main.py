import pygame
import random
import time
import math
import asyncio  # Compatibility with pygbag

# Initialize pygame
pygame.init()

# Screen configuration
WIDTH = 1024
HEIGHT = 576
PANEL_HEIGHT = int(HEIGHT * 0.1)  # 10% of the height for the panel
GAME_HEIGHT = HEIGHT  # All available height for the game

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Constellations")

# Colors
DARK_GRAY = (40, 40, 40)
PANEL_GRAY = (45, 45, 45)
BEIGE = (245, 245, 220)
TRAPEZOID_COLOR = (65, 65, 65)

# Fixed speed for all points
SPEED = 0.5
SPEED_MIN = 0.5
SPEED_MAX = 10.0

# Point configuration
NUM_POINTS = 40
NUM_POINTS_MIN = 10
NUM_POINTS_MAX = 100

# Line configuration
MAX_DISTANCE = 100  # Maximum distance to draw a line
MIN_DISTANCE = 50
MAX_DISTANCE_LIMIT = 300
LINE_OPACITY = 50    # Line opacity (0-255)

# Panel state
panel_visible = True
# Trapezoid dimensions
TRAPEZOID_BASE_LARGE = 40
TRAPEZOID_BASE_SMALL = 20
TRAPEZOID_HEIGHT = 10

# Slider configuration
SLIDER_WIDTH = 150
SLIDER_HEIGHT = 20
SLIDER_MARGIN = 20
SLIDER_Y = HEIGHT - PANEL_HEIGHT + (PANEL_HEIGHT // 2) - (SLIDER_HEIGHT // 2)  # Vertically centered in the panel

# Horizontal positions based on percentages of the width. Arbitrary values as the width is not fixed.
SLIDER_POS_1 = int(WIDTH * 0.22)  # 22% of the width
SLIDER_POS_2 = int(WIDTH * 0.53)  # 53% of the width
SLIDER_POS_3 = int(WIDTH * 0.86)  # 86% of the width

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_value, text):
        self.x = x - (width // 2)  # Center the slider at position x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_value
        self.text = text
        self.dragging = False
        self.rect = pygame.Rect(self.x, y, width, height)
        self.rect_control = pygame.Rect(self.x, y, 10, height)

    def update_value(self, pos_x):
        relative_pos = max(0, min(pos_x - self.x, self.width))
        self.value = self.min_val + (relative_pos / self.width) * (self.max_val - self.min_val)
        self.rect_control.x = self.x + relative_pos - 5

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.text, True, BEIGE)
        text_rect = text.get_rect()
        text_rect.x = self.x - text_rect.width - 10
        text_rect.centery = self.y + self.height//2
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, BEIGE, self.rect_control)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_control.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])

class Point:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        angle = random.uniform(0, 2*math.pi)
        self.speed_x = SPEED * math.cos(angle)
        self.speed_y = SPEED * math.sin(angle)
        self.radius = 3
        self.creation_time = time.time()
        self.lifetime = random.uniform(4, 10)
        self.appear_time = 1.0
        self.disappear_time = 1.0
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surface, BEIGE, (self.radius, self.radius), self.radius)

    def update_speed(self, new_speed):
        proportion = math.sqrt(self.speed_x**2 + self.speed_y**2) / SPEED
        self.speed_x = new_speed * (self.speed_x / (proportion * SPEED))
        self.speed_y = new_speed * (self.speed_y / (proportion * SPEED))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def is_outside(self):
        return (self.x < -self.radius or self.x > WIDTH + self.radius or self.y < -self.radius or self.y > HEIGHT)

    def should_destroy(self):
        return time.time() - self.creation_time > self.lifetime

    def get_opacity(self):
        elapsed_time = time.time() - self.creation_time
        if elapsed_time < self.appear_time:
            return int((elapsed_time / self.appear_time) * 255)
        remaining_time = self.lifetime - elapsed_time
        if remaining_time < self.disappear_time:
            return int((remaining_time / self.disappear_time) * 255)
        return 255

    def draw(self, screen):
        current_surface = self.surface.copy()
        current_surface.set_alpha(self.get_opacity())
        screen.blit(current_surface, (int(self.x - self.radius), int(self.y - self.radius)))

    def distance_to(self, other_point):
        return math.hypot(self.x - other_point.x, self.y - other_point.y)


def draw_lines(screen, points):
    line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i, point1 in enumerate(points):
        for point2 in points[i+1:]:
            distance = point1.distance_to(point2)
            if distance < MAX_DISTANCE:
                opacity = int(LINE_OPACITY * (1 - distance/MAX_DISTANCE))
                pygame.draw.line(line_surface, (*BEIGE, opacity), (int(point1.x), int(point1.y)), (int(point2.x), int(point2.y)), 1)
    screen.blit(line_surface, (0, 0))


def draw_control_panel(screen):
    y_panel = HEIGHT - PANEL_HEIGHT if panel_visible else HEIGHT
    if panel_visible:
        pygame.draw.rect(screen, PANEL_GRAY, (0, y_panel, WIDTH, PANEL_HEIGHT))
        for slider in sliders:
            slider.draw(screen)
    x_center = WIDTH // 2
    y_trapezoid = y_panel
    trapezoid_points = [
        (x_center + TRAPEZOID_BASE_SMALL//2, y_trapezoid - TRAPEZOID_HEIGHT),
        (x_center - TRAPEZOID_BASE_SMALL//2, y_trapezoid - TRAPEZOID_HEIGHT),
        (x_center - TRAPEZOID_BASE_LARGE//2, y_trapezoid),
        (x_center + TRAPEZOID_BASE_LARGE//2, y_trapezoid)
    ]
    pygame.draw.polygon(screen, BEIGE, trapezoid_points)
    return pygame.Rect(x_center - TRAPEZOID_BASE_LARGE//2, y_trapezoid - TRAPEZOID_HEIGHT, TRAPEZOID_BASE_LARGE, TRAPEZOID_HEIGHT)

# Sliders
sliders = [
    Slider(SLIDER_POS_1, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT, SPEED_MIN, SPEED_MAX, SPEED, "SPEED"),
    Slider(SLIDER_POS_2, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT, NUM_POINTS_MIN, NUM_POINTS_MAX, NUM_POINTS, "POINTS"),
    Slider(SLIDER_POS_3, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT, MIN_DISTANCE, MAX_DISTANCE_LIMIT, MAX_DISTANCE, "DISTANCE")
]

async def main():
    global SPEED, NUM_POINTS, MAX_DISTANCE, panel_visible
    points = []
    running = True
    clock = pygame.time.Clock()
    button_rect = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect and button_rect.collidepoint(event.pos):
                    panel_visible = not panel_visible
                if panel_visible:
                    for slider in sliders:
                        slider.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if panel_visible:
                    for slider in sliders:
                        slider.handle_event(event)
            elif event.type == pygame.MOUSEMOTION and panel_visible:
                for slider in sliders:
                    slider.handle_event(event)

        # Update parameters
        if SPEED != sliders[0].value:
            SPEED = sliders[0].value
            for p in points:
                p.update_speed(SPEED)
        if NUM_POINTS != int(sliders[1].value):
            NUM_POINTS = int(sliders[1].value)
            while len(points) < NUM_POINTS:
                points.append(Point())
            while len(points) > NUM_POINTS:
                points.pop(0)
        if MAX_DISTANCE != sliders[2].value:
            MAX_DISTANCE = sliders[2].value

        # Movement and lifecycle
        to_remove = []
        for p in points:
            p.move()
            if p.should_destroy() or p.is_outside():
                to_remove.append(p)
        for p in to_remove:
            if p in points:
                points.remove(p)
        if len(points) < NUM_POINTS:
            points.append(Point())

        # Drawing
        screen.fill(DARK_GRAY)
        draw_lines(screen, points)
        for p in points:
            p.draw(screen)
        button_rect = draw_control_panel(screen)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # Yield control to the WebAssembly runtime

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
