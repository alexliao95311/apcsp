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

# Bullet constants
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7
BULLET_COLOR = YELLOW

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
    
    def get_gun_center(self):
        """Get the center position of the gun for bullet spawning"""
        return self.x + self.width // 2, self.y

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x - self.width // 2  # Center the bullet on the gun
        self.y = y
        self.speed = BULLET_SPEED
        self.color = BULLET_COLOR
        self.active = True
    
    def update(self):
        """Move bullet up the screen"""
        self.y -= self.speed
        # Remove bullet if it goes off screen
        if self.y < 0:
            self.active = False
    
    def draw(self, screen):
        """Draw the bullet as a rectangle"""
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Create gun instance
gun = Gun()

# Bullet management
bullets = []

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle spacebar for shooting (single press)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gun_center_x, gun_center_y = gun.get_gun_center()
                bullets.append(Bullet(gun_center_x, gun_center_y))
    
    # Handle continuous keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        gun.move_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        gun.move_right()
    
    # Fill the screen with black background
    screen.fill(BLACK)
    
    # Update and draw game objects
    gun.update()
    gun.draw(screen)
    
    # Update and draw bullets
    for bullet in bullets[:]:  # Use slice to avoid modification during iteration
        bullet.update()
        bullet.draw(screen)
        # Remove inactive bullets
        if not bullet.active:
            bullets.remove(bullet)
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()