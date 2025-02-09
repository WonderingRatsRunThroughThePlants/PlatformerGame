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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Gravity
GRAVITY = 0.5
JUMP_STRENGTH = -10

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, keybinds):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.keybinds = keybinds
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        self.vel_x = 0
        if keys[self.keybinds[1]]:  # Left
            self.vel_x = -5
        if keys[self.keybinds[3]]:  # Right
            self.vel_x = 5

        # Jumping
        if keys[self.keybinds[0]] and self.on_ground:  # Jump only if on the ground
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
    def __init__(self, x, y, width, height, color, move_range=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_range = move_range
        self.direction = 1  # Movement direction

    def update(self):
        if self.move_range:
            self.rect.x += self.direction * 2  # Move the platform
            if self.rect.left < self.move_range[0] or self.rect.right > self.move_range[1]:
                self.direction *= -1  # Reverse direction

# Create groups
players = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player
player = Player(150, 100, RED, [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d])
players.add(player)

# Create platforms
platforms.add(Platform(100, 400, 200, 20, GREEN))
platforms.add(Platform(400, 300, 200, 20, GREEN, move_range=(300, 500)))  # Moving platform
platforms.add(Platform(600, 200, 200, 20, GREEN))

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

    # Draw everything
    platforms.draw(surface)
    players.draw(surface)

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