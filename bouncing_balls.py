import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Balls Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.dx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

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
        ball1.x += overlap * cos
        ball1.y += overlap * sin
        ball2.x -= overlap * cos
        ball2.y -= overlap * sin

def main():
    clock = pygame.time.Clock()
    balls = [Ball(random.randint(50, width-50), random.randint(50, height-50), random.randint(10, 30)) for _ in range(10)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
