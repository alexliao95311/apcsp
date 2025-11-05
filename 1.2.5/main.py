import pygame
import sys
import random

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
GUN_SPEED = 15

# Bullet constants
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7
BULLET_COLOR = YELLOW

# Asteroid constants
ASTEROID_WIDTH = 40
ASTEROID_HEIGHT = 40
ASTEROID_SPEED = 3
ASTEROID_COLOR = RED
ASTEROID_SPAWN_RATE = 60  # Spawn every 60 frames (1 second at 60 FPS)

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

# Asteroid class
class Asteroid:
    def __init__(self, x, y):
        self.width = ASTEROID_WIDTH
        self.height = ASTEROID_HEIGHT
        self.x = x
        self.y = y
        self.speed = ASTEROID_SPEED
        self.color = ASTEROID_COLOR
        self.active = True
    
    def update(self):
        """Move asteroid down the screen"""
        self.y += self.speed
        # Mark asteroid as inactive if it goes past the bottom
        if self.y > SCREEN_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        """Draw the asteroid as a rectangle"""
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """Get pygame.Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Asteroid spawner function
def spawn_asteroid():
    """Spawn an asteroid at a random x position at the top of the screen"""
    x = random.randint(0, SCREEN_WIDTH - ASTEROID_WIDTH)
    return Asteroid(x, -ASTEROID_HEIGHT)

# Collision detection function
def check_bullet_asteroid_collision(bullet, asteroid):
    """Check if bullet and asteroid rectangles overlap"""
    bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
    asteroid_rect = asteroid.get_rect()
    return bullet_rect.colliderect(asteroid_rect)

# Bullet management
bullets = []

# Asteroid management
asteroids = []
asteroid_spawn_timer = 0

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
    
    # Spawn asteroids
    asteroid_spawn_timer += 1
    if asteroid_spawn_timer >= ASTEROID_SPAWN_RATE:
        asteroids.append(spawn_asteroid())
        asteroid_spawn_timer = 0
    
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
    
    # Update and draw asteroids
    for asteroid in asteroids[:]:  # Use slice to avoid modification during iteration
        asteroid.update()
        asteroid.draw(screen)
        # Remove inactive asteroids (hit ground)
        if not asteroid.active:
            asteroids.remove(asteroid)
            print("Asteroid hit the ground!")  # Debug message - can be removed later
    
    # Check bullet-asteroid collisions
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if bullet.active and asteroid.active and check_bullet_asteroid_collision(bullet, asteroid):
                # Remove both bullet and asteroid on collision
                bullet.active = False
                asteroid.active = False
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                print("Asteroid destroyed!")  # Debug message - can be removed later
                break  # Break inner loop since bullet is destroyed
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()