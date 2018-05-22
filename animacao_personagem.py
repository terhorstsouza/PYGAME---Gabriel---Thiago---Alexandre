import pygame
import numpy as np
import random

cenarios = []
branco = (255,255,255)
comprimento_display = 736
altura_display = 588
tela = pygame.display.set_mode((comprimento_display, altura_display))


tempo = np.arange(0,2,1) 
gravidade = 1
contadorzinho = 0
 
class Neguinho(pygame.sprite.Sprite):
    
    
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load('personagem.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.frame = 0
        self.vy = 0
        self.ay = 1
        self.pulo = 15
        self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) }
        self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.directionx = 'stand_left'
        self.directiony = 'stand_right'
    
    
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    
    def update(self):
        
        if self.directionx == 'left':
            self.clip(self.left_states)
            self.rect.x -= 5

        if self.directionx == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
            
        if self.directiony == 'jump':
            self.vy += self.ay
            self.rect.y += self.vy
            
        if self.directiony == 'baixo':
            if self.rect.y <475:
                gravidade = 50
                self.rect.y += gravidade

        if self.directiony == 'jump' and self.directionx == 'right':
            self.vy += self.ay
            self.rect.y += self.vy
            self.clip(self.right_states)
            self.rect.x += 5
            
        if self.directiony == 'jump' and self.directionx == 'left':
            self.vy += self.ay
            self.rect.y += self.vy
            self.clip(self.left_states)
            self.rect.x -= 5
                
        if self.directionx == 'stand_left':
            self.clip(self.left_states[0])
        
        if self.directionx == 'stand_right':
            self.clip(self.right_states[0])
    
        self.image = self.sheet.subsurface(self.sheet.get_clip())
            


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:           
            if event.key == pygame.K_LEFT:
                self.directionx = 'left'
            if event.key == pygame.K_RIGHT:
                self.directionx = 'right'
            
            if event.key == pygame.K_UP:
                if self.rect.y == 475:
                    self.vy = -15
                    self.directiony = 'jump'
            
        if event.type == pygame.KEYUP:  
 
            if event.key == pygame.K_LEFT:
                self.directionx = 'stand_left'           
            if event.key == pygame.K_RIGHT:
                self.directionx = 'stand_right'
            
            if event.key == pygame.K_UP:
                if self.rect.y <= 475:
                    self.directiony = 'baixo'
            
                    