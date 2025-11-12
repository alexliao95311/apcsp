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
GUN_SPEED = 10

# Bullet constants
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7
BULLET_COLOR = YELLOW

# Asteroid constants
ASTEROID_SIZES = [
    {"width": 30, "height": 30, "speed": 4, "points": 15},  # Small asteroid
    {"width": 40, "height": 40, "speed": 3, "points": 10},  # Medium asteroid
    {"width": 60, "height": 60, "speed": 2, "points": 5},   # Large asteroid
]
ASTEROID_COLOR = RED
ASTEROID_SPAWN_RATE = 60  # Spawn every 60 frames (1 second at 60 FPS)

# Game constants
STARTING_LIVES = 3

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids Shooter Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Initialize font for text display
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Load images
def load_image(filename):
    """Load and return an image, with error handling"""
    try:
        image = pygame.image.load(f"1.2.5/images/{filename}")
        return image
    except pygame.error:
        print(f"Could not load image: {filename}")
        return None

# Load all game images
spaceship_off_img = load_image("spaceship-off.png")
spaceship_on_img = load_image("spaceship-on.png")
missile_img = load_image("missile.png")
rock_small_img = load_image("rock-small.png")
rock_normal_img = load_image("rock-normal.png")
rock_big_img = load_image("rock-big.png")

# Scale images to appropriate sizes if needed
if spaceship_off_img:
    spaceship_off_img = pygame.transform.scale(spaceship_off_img, (GUN_WIDTH, GUN_HEIGHT))
if spaceship_on_img:
    spaceship_on_img = pygame.transform.scale(spaceship_on_img, (GUN_WIDTH, GUN_HEIGHT))
if missile_img:
    missile_img = pygame.transform.scale(missile_img, (BULLET_WIDTH, BULLET_HEIGHT))

# Gun/Player class
class Gun:
    def __init__(self):
        self.width = GUN_WIDTH
        self.height = GUN_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2  # Center horizontally
        self.y = SCREEN_HEIGHT - self.height - 10  # Position near bottom
        self.speed = GUN_SPEED
        self.color = WHITE
        self.is_moving = False  # Track if the spaceship is moving
    
    def draw(self, screen):
        """Draw the gun using images"""
        # Choose image based on movement state
        if self.is_moving and spaceship_on_img:
            screen.blit(spaceship_on_img, (self.x, self.y))
        elif spaceship_off_img:
            screen.blit(spaceship_off_img, (self.x, self.y))
        else:
            # Fallback to rectangle if images don't load
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def move_left(self):
        """Move gun to the left"""
        if self.x > 0:
            self.x -= self.speed
            self.is_moving = True
    
    def move_right(self):
        """Move gun to the right"""
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.is_moving = True
    
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
        """Draw the bullet using image"""
        if self.active:
            if missile_img:
                screen.blit(missile_img, (self.x, self.y))
            else:
                # Fallback to rectangle if image doesn't load
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Create gun instance
gun = Gun()

# Asteroid class
class Asteroid:
    def __init__(self, x, y, size_index):
        self.size_data = ASTEROID_SIZES[size_index]
        self.width = self.size_data["width"]
        self.height = self.size_data["height"]
        self.x = x
        self.y = y
        self.speed = self.size_data["speed"]
        self.points = self.size_data["points"]
        self.color = ASTEROID_COLOR
        self.active = True
        self.size_index = size_index
        
        # Select appropriate image based on size
        if size_index == 0:  # Small
            self.image = rock_small_img
        elif size_index == 1:  # Medium
            self.image = rock_normal_img
        else:  # Large
            self.image = rock_big_img
        
        # Scale image to match size if needed
        if self.image:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
    
    def update(self):
        """Move asteroid down the screen"""
        self.y += self.speed
        # Mark asteroid as inactive if it goes past the bottom
        if self.y > SCREEN_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        """Draw the asteroid using image"""
        if self.active:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                # Fallback to rectangle if image doesn't load
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """Get pygame.Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Asteroid spawner function
def spawn_asteroid():
    """Spawn an asteroid at a random x position at the top of the screen with random size"""
    # Choose random size (0=small, 1=medium, 2=large)
    size_index = random.randint(0, 2)
    asteroid_width = ASTEROID_SIZES[size_index]["width"]
    asteroid_height = ASTEROID_SIZES[size_index]["height"]
    
    x = random.randint(0, SCREEN_WIDTH - asteroid_width)
    return Asteroid(x, -asteroid_height, size_index)

# Collision detection function
def check_bullet_asteroid_collision(bullet, asteroid):
    """Check if bullet and asteroid rectangles overlap"""
    bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
    asteroid_rect = asteroid.get_rect()
    return bullet_rect.colliderect(asteroid_rect)

# UI display functions
def draw_score(screen, score):
    """Draw the current score on screen"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_lives(screen, lives):
    """Draw the current lives on screen"""
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 50))

def draw_game_over(screen, score):
    """Draw game over screen with final score and restart instructions"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game over text
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(game_over_text, game_over_rect)
    
    # Final score
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(final_score_text, final_score_rect)
    
    # Restart instructions
    restart_text = font.render("Press R to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(restart_text, restart_rect)

def reset_game():
    """Reset all game variables to start a new game"""
    global score, lives, game_over, bullets, asteroids, asteroid_spawn_timer
    score = 0
    lives = STARTING_LIVES
    game_over = False
    bullets.clear()
    asteroids.clear()
    asteroid_spawn_timer = 0
    # Reset gun position
    gun.x = SCREEN_WIDTH // 2 - gun.width // 2

# Bullet management
bullets = []

# Asteroid management
asteroids = []
asteroid_spawn_timer = 0

# Game state variables
score = 0
lives = STARTING_LIVES
game_over = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if not game_over:
                # Handle spacebar for shooting (single press)
                if event.key == pygame.K_SPACE:
                    gun_center_x, gun_center_y = gun.get_gun_center()
                    bullets.append(Bullet(gun_center_x, gun_center_y))
            else:
                # Handle game over screen inputs
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
    
    # Only handle game input if not game over
    if not game_over:
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        gun.is_moving = False  # Reset movement state first
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
    
    if not game_over:
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
            # Remove inactive asteroids (hit ground) and decrement lives
            if not asteroid.active:
                asteroids.remove(asteroid)
                lives -= 1
                print(f"Asteroid hit the ground! Lives remaining: {lives}")
                # Check if game over
                if lives <= 0:
                    game_over = True
        
        # Check bullet-asteroid collisions
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet.active and asteroid.active and check_bullet_asteroid_collision(bullet, asteroid):
                    # Remove both bullet and asteroid on collision
                    bullet.active = False
                    asteroid.active = False
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    # Increase score based on asteroid size
                    score += asteroid.points
                    print(f"Asteroid destroyed! Points: {asteroid.points}, Total Score: {score}")
                    break  # Break inner loop since bullet is destroyed
        
        # Draw UI elements
        draw_score(screen, score)
        draw_lives(screen, lives)
    else:
        # Draw game over screen
        draw_game_over(screen, score)
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()