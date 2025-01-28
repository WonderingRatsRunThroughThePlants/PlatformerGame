import pygame
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
        pygame.draw.rect(self.image,color,pygame.rect(30,30,30,30))

surface = pygame.display.set_mode((800,800))
pygame.display.set_caption("Platformer")

pygame.draw.rect(surface, (0,0,255), pygame.rect(30,30,30,30))
pygame.display.flip()