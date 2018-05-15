#!/usr/bin/env python
import pygame
import personagem

pygame.init()


comprimento_display = 736
altura_display = 588

texto_grande = pygame.font.Font('freesansbold.ttf', 115)
texto_pequeno = pygame.font.Font('freesansbold.ttf', 30)

tela = pygame.display.set_mode((comprimento_display, altura_display))
pygame.display.set_caption("Python/Pygame Animation")
relogio = pygame.time.Clock()
player = personagem.Neguinho((150, 150))


preto = (0,0,0)
branco = (255,255,255)

tela_menu = pygame.image.load('jogo_terror.jpg')
background_mansao = pygame.image.load("mansao_BG_certo.jpg")

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

def jogo():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return -1
            player.handle_event(evento)
        
        player.update()
	tela.blit(background_mansao, [0,0])
        #tela.fill(pygame.Color('blue'))  
        tela.blit(player.image, player.rect)
        
        pygame.display.flip()              
        relogio.tick(15)      

def gameloop():
    # Variavel estado: em que estado o jogo se encontra
    #
    # -1: game over
    # 0: tela inicial
    # 1: proxima tela
    estado = 0
    #enquanto o jogo esta aberto
    while estado != -1:
        if estado == 0:
            estado = menu()
        elif estado == 1:
            print('Funcionando')
            estado = jogo()
 
gameloop()
pygame.quit()
