import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants - Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB values)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Gun/Player constants
GUN_WIDTH = 60
GUN_HEIGHT = 40
GUN_SPEED = 5

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids Shooter Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Gun/Player class
class Gun:
    def __init__(self):
        self.width = GUN_WIDTH
        self.height = GUN_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2  # Center horizontally
        self.y = SCREEN_HEIGHT - self.height - 10  # Position near bottom
        self.speed = GUN_SPEED
        self.color = WHITE
    
    def draw(self, screen):
        """Draw the gun as a rectangle"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def move_left(self):
        """Move gun to the left"""
        if self.x > 0:
            self.x -= self.speed
    
    def move_right(self):
        """Move gun to the right"""
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def update(self):
        """Update gun state (for future use)"""
        pass

# Create gun instance
gun = Gun()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with black background
    screen.fill(BLACK)
    
    # Update and draw game objects
    gun.update()
    gun.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()