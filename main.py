import pygame
import sys
# math imports
import math, random

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,color,keybinds,isdead):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.color = color
        self.keybinds = keybinds
        isdead = False
        self.isdead = isdead
        self.image = pygame.Surface((100,100),pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.image,color,pygame.Rect(30,30,30,30))
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.keybinds[0]]:
            self.rect.centery -= 5
        if keys[self.keybinds[1]]:
            self.rect.centerx -= 5
        if keys[self.keybinds[2]]:
            self.rect.centery += 5
        if keys[self.keybinds[3]]:
            self.rect.centerx += 5


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,color,boundsL,boundsR):
        super(Platform, self).__init__()
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((100,100),pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.image,color,pygame.Rect(30,30,100,30))
        self.deltax = random.randint(-10,10)
        self.boundsL = boundsL
        self.boundsR = boundsR
    def move(self):
        if self.rect.left < self.boundsL or self.rect.right > self.boundsR:
            self.deltax = -self.deltax
        self.rect.x += self.deltax

surface = pygame.display.set_mode((800,800))
pygame.display.set_caption("Platformer")

platforms = pygame.sprite.Group()
platforms.add(Platform(100,100,(0,255,0),0,400))
platforms.add(Platform(600,100,(0,255,0),400,800))

players = pygame.sprite.Group()
players.add(Player(800,0,(255,0,0),[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d],False))

clock = pygame.time.Clock()

alive = True
while alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
    surface.fill((0,0,0))

    for plat in platforms:
        plat.move()
    platforms.draw(surface)

    players.update()
    players.draw(surface)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
    