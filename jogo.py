#!/usr/bin/env python

import pygame
import random

pygame.init()

comprimento_display = 736
altura_display = 588
VELOCIDADE = 8
music = pygame.mixer.music.load("13_Digital_Native.wav")
pygame.mixer.music.play(-1)

dano1 = 10
vida1 = 30

texto_grande = pygame.font.Font('freesansbold.ttf', 115)
texto_pequeno = pygame.font.Font('freesansbold.ttf', 30)

tela = pygame.display.set_mode((comprimento_display, altura_display))
pygame.display.set_caption("Python/Pygame Animation")
relogio = pygame.time.Clock()

posicao_porta = 730
largura_porta = 6

preto = (0,0,0)
branco = (255,255,255)

vida1 = 30
dano1 = 10

tela_menu = pygame.image.load('jogo_terror.jpg')
background_mansao = pygame.image.load("mansao_BG_certo.jpg")

class Tiro(pygame.sprite.Sprite):
    def __init__ (self, x, y, raio, velocidade, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Glenos-G_160_bullet.png')
        self.image = pygame.Surface((2*raio, 2*raio))
        pygame.draw.circle(self.image, preto, (0, 0), raio)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direcao = direcao
        self.vel = velocidade * direcao
    def update(self):
        self.rect.x += self.vel

class Neguinho(pygame.sprite.Sprite):

    parado = True

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load('personagem.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.x = self.rect.x
        self.y = self.rect.y
        self.frame = 0
        self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76),\
                            2: (156, 76, 52, 76) }
        self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76),\
                            2: (156, 152, 52, 76) }
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
                if self.rect.x >= 728-(52*2):
                    print("Funcionando")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.direction = 'stand_left'
            if event.key == pygame.K_RIGHT:
                self.direction = 'stand_right'

player = Neguinho((0, 475))

class MOBs(pygame.sprite.Sprite):
        walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),\
                    pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),\
                    pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),\
                    pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),\
                    pygame.image.load('R9E.png'), pygame.image.load('R10E.png'),\
                    pygame.image.load('R11E.png')]

        walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'),\
                    pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),\
                    pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),\
                    pygame.image.load('L7E.png'), pygame.image.load('L8E.png'),\
                    pygame.image.load('L9E.png'), pygame.image.load('L10E.png'),\
                    pygame.image.load('L11E.png')]

        def __init__(self, x, y, width, height, end):
            pygame.sprite.Sprite.__init__(self)
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.end = end
            self.path = [self.x, self.end]
            self.walkCount = 0
            self.vel = 3
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            self.health = 10
            self.rect = self.walkRight[self.walkCount].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.helth = vida1

        def draw(self):
            self.move()
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                tela.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            else:
                tela.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

            pygame.draw.rect(tela, (0,128,0), (self.hitbox[0],\
                                self.hitbox[1] - 20, 50, 10))


        def move(self):
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            self.rect.x = self.x
            self.rect.y = self.y

        def hit(self, dano, bala, acertos):
            if self.health > 0:
                self.health -= dano
                for bala in group_tiros:
                    pygame.draw.rect(tela, (255,0,0), (self.hitbox[0],\
                    self.hitbox[1] - 20, 50 - (3 * (10 - len(acertos))), 10))
            else:
                pygame.sprite.spritecollide(bala, mobs, True)
                print('morreu')



all_sprites = pygame.sprite.Group()
all_sprites.add(player)
mobs = pygame.sprite.Group()

def texto(texto, fonte):
    tipo_texto = fonte.render(texto, True, preto)
    return tipo_texto, tipo_texto.get_rect()

def butao(mensagem, x, y, largura, altura, cor_inativa, cor_ativa):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        pygame.draw.rect(tela, cor_ativa,(x,y,largura,altura))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(tela,cor_inativa,(x,y,largura,altura))

    texto_botao = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = texto(mensagem, texto_botao)
    textRect.center = ((x+(largura/2)), (y+(altura/2)))
    tela.blit(textSurf, textRect)
    return False

def menu():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return -1
        tela.fill(branco)
        TextSurf, TextRect = texto('Land of Blood', texto_grande)
        TextRect.center = ((comprimento_display/2), (altura_display/2))
        tela.blit(TextSurf, TextRect)

        if butao('jogar', 150,450,100,50,(0,255,0),(0,200,0)):
            return 1
        if butao('sair', 550,450,100,50,(255,0,0),(200,0,0)):
            return -1

        pygame.display.update()
        relogio.tick(15)

lista_x = []

group_tiros = pygame.sprite.Group()

def jogo():

    for w in range(8):
        x = random.randrange(100,600)
        lista_x.append(x)
    for i in range(8):
        for o in lista_x:
            m = MOBs(o,490,52,52,690)
            mobs.add(m)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return -1
            if evento.type == pygame.KEYDOWN:

                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    direcao = 1
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    direcao = -1
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if len(group_tiros) <= 5:
                        pygame.mixer.Sound.play(pygame.mixer.Sound("Gun+Silencer.wav"))
                        group_tiros.add(
                            Tiro((player.rect.x + (player.rect.width /2)),\
                                 (player.rect.y + 45), 7, VELOCIDADE, direcao))

            player.handle_event(evento)

        for mob in mobs:
            balas_atingidas = pygame.sprite.spritecollide(mob, group_tiros, True)
            for bala in balas_atingidas:
                mob.hit(dano1, bala, balas_atingidas)

        player.update()
        mobs.update()
        group_tiros.update()

        if player.rect.x <= 0:
            player.rect.x = 0
        if player.rect.x >= 736 - player.rect.width:
            player.rect.x = 736 - player.rect.width

        tela.blit(background_mansao, [0,0])
        tela.blit(player.image, player.rect)
        group_tiros.draw(tela)

        for bixo in mobs:
            bixo.draw()

        pygame.display.flip()
        pygame.display.update()
        relogio.tick(15)

def gameloop():
    # Variavel estado: em que estado o jogo se encontra
    #
    # -1: game over
    # 0: tela inicial
    # 1: proxima tela
    estado = 1
    #enquanto o jogo esta aberto
    while estado != -1:
        if estado == 0:
            estado = menu()
        elif estado == 1:
            estado = jogo()

gameloop()
pygame.quit()
