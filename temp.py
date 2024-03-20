import pygame
import math
from globals import SCREEN_Y, SCREEN_X

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("Quarter Oval")

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the starting and ending points (p1 and p2)
p1 = pygame.math.Vector2(500, 500)
p2 = pygame.math.Vector2(900, 300)

# Calculate the center point of the oval
center = pygame.math.Vector2(min(p1.x, p2.x), max(p1.y, p2.y))

# Calculate the radii of the oval
a = abs(p1.x - p2.x) / 2  # Semi-major axis
b = abs(p1.y - p2.y) / 2  # Semi-minor axis

# Calculate the angle increment between points
num_points = 10
angle_increment = math.pi / (2 * (num_points - 1))

# Generate points along the quarter oval path
points = []
for i in range(num_points):
    angle = i * angle_increment
    x = center.x + a * math.cos(angle)
    y = center.y - b * math.sin(angle)  # Note the minus sign for the y-coordinate
    points.append((x, y))

# Set up the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the oval
    pygame.draw.ellipse(screen, (255, 255, 255), (center.x - a, center.y - b, 2 * a, 2 * b), 1)

    # Draw small red, green, and blue circles at the center, p1, and p2
    pygame.draw.circle(screen, RED, center, 5)
    pygame.draw.circle(screen, GREEN, p1, 5)
    pygame.draw.circle(screen, BLUE, p2, 5)

    # Draw points along the quarter oval path
    for point in points:
        pygame.draw.circle(screen, (255, 255, 255), (point[0], point[1]), 3)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
