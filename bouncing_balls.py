import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Bouncing Balls Simulation with Gravity")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Gravity
GRAVITY = 0.0005  # Reduced gravity for relative coordinates

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = random.uniform(-0.005, 0.005)
        self.dy = random.uniform(-0.005, 0.005)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVITY  # Apply gravity

        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= 1:
            self.dx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= 1:
            self.dy *= -0.9  # Reduce velocity on floor bounce
            self.y = max(self.radius, min(1 - self.radius, self.y))  # Ensure ball stays within bounds

    def draw(self, screen):
        screen_x = int(self.x * width)
        screen_y = int(self.y * height)
        screen_radius = int(self.radius * min(width, height))
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), screen_radius)

def check_collision(ball1, ball2):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < ball1.radius + ball2.radius:
        # Collision detected, calculate new velocities
        angle = math.atan2(dy, dx)
        sin = math.sin(angle)
        cos = math.cos(angle)

        # Rotate velocities
        ball1.dx, ball1.dy = ball1.dx * cos + ball1.dy * sin, ball1.dy * cos - ball1.dx * sin
        ball2.dx, ball2.dy = ball2.dx * cos + ball2.dy * sin, ball2.dy * cos - ball2.dx * sin

        # Swap velocities
        ball1.dx, ball2.dx = ball2.dx, ball1.dx

        # Rotate velocities back
        ball1.dx, ball1.dy = ball1.dx * cos - ball1.dy * sin, ball1.dy * cos + ball1.dx * sin
        ball2.dx, ball2.dy = ball2.dx * cos - ball2.dy * sin, ball2.dy * cos + ball2.dx * sin

        # Move balls apart to prevent sticking
        overlap = (ball1.radius + ball2.radius - distance) / 2
        ball1.x += overlap * cos / width
        ball1.y += overlap * sin / height
        ball2.x -= overlap * cos / width
        ball2.y -= overlap * sin / height

def main():
    global width, height, screen
    clock = pygame.time.Clock()
    balls = [Ball(random.uniform(0.1, 0.9), random.uniform(0.1, 0.9), random.uniform(0.02, 0.05)) for _ in range(10)]
    
    # Give initial upward velocity
    for ball in balls:
        ball.dy = random.uniform(-0.015, -0.01)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        screen.fill(BLACK)

        for i, ball in enumerate(balls):
            ball.move()
            for other_ball in balls[i+1:]:
                check_collision(ball, other_ball)
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
