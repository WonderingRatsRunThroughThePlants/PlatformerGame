import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Player
GREEN = (0, 255, 0)  # Platforms
BLUE = (0, 0, 255)  # Enemies
BLACK = (0, 0, 0)

# Gravity settings
GRAVITY = 0.5
JUMP_STRENGTH = -10

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Movement
        self.vel_x = 0
        if keys[pygame.K_a]:  # Left
            self.vel_x = -5
        if keys[pygame.K_d]:  # Right
            self.vel_x = 5

        # Jumping
        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

        # Apply gravity
        self.vel_y += GRAVITY

        # Move the player
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Prevent going off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Collision with platforms
        self.check_collision()

    def check_collision(self):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, move_range=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_range = move_range
        self.direction = 1  # 1 = right, -1 = left

    def update(self):
        if self.move_range:
            self.rect.x += self.direction * 3  # Move the platform
            if self.rect.left < self.move_range[0] or self.rect.right > self.move_range[1]:
                self.direction *= -1  # Reverse direction

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 2  # Moves right
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x

        # Check if enemy is on a platform
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        # If enemy is on the ground but no platform is directly beneath, let it fall
        if not self.on_ground:
            self.vel_y += GRAVITY

        # Remove enemy if it falls off screen
        if self.rect.top > HEIGHT:
            self.kill()

# Create groups
players = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player(150, 100)
players.add(player)

# Create platforms
platforms.add(Platform(100, 400, 200, 20))  # Static
platforms.add(Platform(400, 300, 200, 20, move_range=(300, 500)))  # Moving
platforms.add(Platform(600, 200, 200, 20))  # Static

# Create enemies
for i in range(3):  # Three enemies
    enemy = Enemy(random.randint(100, 700), 50)
    enemies.add(enemy)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    surface.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update entities
    players.update()
    platforms.update()
    enemies.update()

    # Draw everything
    platforms.draw(surface)
    players.draw(surface)
    enemies.draw(surface)

    # Win condition (reach top)
    if player.rect.top <= 0:
        print("You Win!")
        running = False

    # Lose condition (fall off)
    if player.rect.top > HEIGHT:
        print("Game Over!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
