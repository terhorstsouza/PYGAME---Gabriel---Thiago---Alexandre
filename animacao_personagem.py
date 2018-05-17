#Esse código foi copiado e adaptado do seguinte site: http://xorobabel.blogspot.com.br/2012/10/pythonpygame-2d-animation-jrpg-style.html

import pygame
import interação_objetos as io
 
class Neguinho(pygame.sprite.Sprite):
    
    def __init__(self, position):
        self.sheet = pygame.image.load('personagem.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.frame = 0
        self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) }
        self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.direction = 'stand_left'
    
    
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
        if self.direction == 'left':
            self.clip(self.left_states)
            self.rect.x -= 5
        if self.direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
        if self.direction == "cima":
            self.clip(self.right_states)
            io.Teste
            
        if self.direction == 'stand_left':
            self.clip(self.left_states[0])
        if self.direction == 'stand_right':
            self.clip(self.right_states[0])
    
        self.image = self.sheet.subsurface(self.sheet.get_clip())



    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:           
            if event.key == pygame.K_LEFT:
                self.direction = 'left'
            if event.key == pygame.K_RIGHT:
                self.direction = 'right'
            
            if event.key == pygame.K_UP:
                if player.rect.x >= 728 and player.rect.x < 736:
                    self.direction = "cima"
                    
        if event.type == pygame.KEYUP:  
 
            if event.key == pygame.K_LEFT:
                self.direction = 'stand_left'           
            if event.key == pygame.K_RIGHT:
                self.direction = 'stand_right'
                
           
player = Neguinho((0, 475))

