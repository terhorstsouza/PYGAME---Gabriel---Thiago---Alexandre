import pygame

class Tiro():

    DANO = 100 #dano que a bala faz
    VELOCIDADE = 20 #pixels por frame que ela viaja

    def __init__ (self, x, y, raio, direcao):
        self.x = x
        self.y = y
        self.r = raio
        self.direcao = direcao
        self.vel = VELOCIDADE * direcao

    def draw():
        pygame.draw.circle(tela, (0,0,0), (self.x, self.y), self.r)

    def direcao():
        if event.key == pygame.K_LEFT:
            direcao = -1
        if event.key == pygame.K_RIGHT:
            direcao = 1
