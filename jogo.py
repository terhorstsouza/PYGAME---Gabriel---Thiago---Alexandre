#!/usr/bin/env python
import pygame
import animacao_personagem

pygame.init()

comprimento_display = 800
altura_display = 600

texto_grande = pygame.font.Font('freesansbold.ttf', 115)
texto_pequeno = pygame.font.Font('freesansbold.ttf', 30)

preto = (0,0,0)
branco = (255,255,255)

#cria tela
tela = pygame.display.set_mode((comprimento_display,altura_display))
pygame.display.set_caption('nome do jogo')
relogio = pygame.time.Clock()
player = animacao_personagem.Serge((150, 150))

def texto(texto, fonte):
    tipo_texto = fonte.render(texto, True, preto)
    return tipo_texto, tipo_texto.get_rect()

def butao(mensagem, x, y, largura, altura, cor_inativa, cor_ativa, acao = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
        pygame.draw.rect(tela, cor_ativa,(x,y,largura,altura))
        if click[0] == 1:
            acao()
    else:
        pygame.draw.rect(tela,cor_inativa,(x,y,largura,altura))
    texto_botao = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = texto(mensagem, texto_botao)
    textRect.center = ((x+(largura/2)), (y+(altura/2)))
    tela.blit(textSurf, textRect)

def menu():
    intro = True
    while intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        tela.fill(branco)
        TextSurf, TextRect = texto('nome do jogo', texto_grande)
        TextRect.center = ((comprimento_display/2), (altura_display/2))
        tela.blit(TextSurf, TextRect)

        butao('jogar', 150,450,100,50,(0,255,0),(0,200,0), gameloop)
        butao('sair', 550,450,100,50,(255,0,0),(200,0,0))

        pygame.display.update()
        relogio.tick(15)


def gameloop():


    
    #enquanto o jogo esta aberto
    fora_do_jogo = False
    while not fora_do_jogo:

	for event in pygame.event.get():
            if event.type == pygame.QUIT:
            	    fora_do_jogo = True
    	player.handle_event(event)
    	tela.fill(pygame.Color('blue'))
    	tela.blit(player.image, player.rect)
    	pygame.display.flip()

        menu()
        
        pygame.display.flip()
        #FPS
        relogio.tick(60)

gameloop()
pygame.quit()
quit()
