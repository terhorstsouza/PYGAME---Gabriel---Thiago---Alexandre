#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random

pygame.init()

#Acessa-se um arquivo de texto que contem os dados do Highscore
with open('HighScore.txt', 'r') as arquivo:
	HighScore_antigo = arquivo.read()

morte = []

#Aqui definimos os backgrounds
background  = pygame.image.load("mansao_BG_certo.jpg")
background2 = pygame.image.load('Outro_cenario.png')
background3 = pygame.image.load('cenario_zap.png')
background4 = pygame.image.load('cenario_wow.png')
background5 = pygame.image.load('NOVO_CENARIO_1.png')
background6 = pygame.image.load('cenario_caverna.png')
background7 = pygame.image.load('cenario_floresta.png')
background8 = pygame.image.load('cenario_mario.png')
background9 = pygame.image.load('lua.png')

#Aqui criamos uma lista dos backgrounds
backgrounds = [background ,background2,background3, background4, background5,background6,background7,background8,background9]

#Definimos o tamanho da tela
comprimento_display = 736
altura_display = 588

VELOCIDADE = 10

#Definimos a musica do jogo
music = pygame.mixer.music.load("13_Digital_Native.wav")


vida_player = 10

dano_mob = 10

tela_HUB = pygame.image.load('tela_Hub.png')

pygame.mixer.music.play(-1)

dano1 = 10
vida1 = 50

#Definimos as fontes que utilizamos
texto_grande = pygame.font.Font('Kingthings_Calligraphica_2.ttf', 115)
texto_pequeno = pygame.font.Font('Kingthings_Calligraphica_2.ttf', 30)
tiro = pygame.image.load("bullet.png")
tela = pygame.display.set_mode((comprimento_display, altura_display))
pygame.display.set_caption("Python/Pygame Animation")
relogio = pygame.time.Clock()

#definimos 2 cores
preto = (0,0,0)
branco = (255,255,255)

tela_menu = pygame.image.load('MENUU.png')

#Definimos 3 tipos de jogadores para futuro uso na seleção de personagens
jogador1 = pygame.image.load('jogador1.png')
jogador2 = pygame.image.load('jogador2.png')
jogador3 = pygame.image.load('jogador3.png')

#implementamos a classe responsavel por criar os tiros
class Tiro(pygame.sprite.Sprite):
	def __init__ (self, x, y, velocidade, direcao):
	   pygame.sprite.Sprite.__init__(self)
	   self.image = tiro
	   self.rect = self.image.get_rect()
	   self.mask = pygame.mask.from_surface(self.image)
	   self.rect.x = x
	   self.rect.y = y
	   self.direcao = direcao
	   self.vel = velocidade * direcao

	def update(self):

		self.rect.x += self.vel

		if self.rect.x < 0 or self.rect.x > comprimento_display:
			
			self.kill()

		if self.rect.y <= player.rect.y/2:
			self.rect.y = player.rect.y/2

#implementamos a classe responsavel por criar o Player
class Neguinho(pygame.sprite.Sprite):

	parado = True

	def __init__(self, position,personagem):
		pygame.sprite.Sprite.__init__(self)

		#aqui colocamos uma gama de 3 possibilidades de personagens a serem escolhidos
		self.personagem = personagem
		if self.personagem == jogador1:
			self.sheet = pygame.image.load('personagem.png')
		elif self.personagem == jogador2:
			self.sheet = pygame.image.load('personagem2.png')
		elif self.personagem == jogador3:
			self.sheet = pygame.image.load('personagem3.png')
		self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
		self.image = self.sheet.subsurface(self.sheet.get_clip())
		self.rect = self.image.get_rect()
		self.rect.topleft = position
		self.mask = pygame.mask.from_surface(self.image)
		self.x = self.rect.x
		self.y = self.rect.y
		self.frame = 0
		self.vy = 0
		self.ay = 1
		self.pulo = 15
		self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76),\
							2: (156, 76, 52, 76) }
		self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76),\
							2: (156, 152, 52, 76) }
		self.directionx = 'stand_left'
		self.directiony = 'stand_right'

	#Aqui começamos a implementação da animação
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

	#Aqui o atualizamos
	def update(self):
		if self.directionx == 'left':
			self.clip(self.left_states)
			self.rect.x -= 5

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

		if self.directionx == 'right':
			self.clip(self.right_states)
			self.rect.x += 5

		if self.directionx == 'stand_left':
			self.clip(self.left_states[0])

		if self.directionx == 'stand_right':
			self.clip(self.right_states[0])

		self.image = self.sheet.subsurface(self.sheet.get_clip())

	def handle_event(self, event):

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				self.directionx = 'left'

			if event.key == pygame.K_d:
				self.directionx = 'right'

			if event.key == pygame.K_w:
				print('pulando')
				if self.rect.y >= 475:
					self.vy = -15
					self.directiony = 'jump'

			if event.key == pygame.K_e:
				if self.rect.x >= 728-(52*2):
					print("Funcionando")

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_a:
				self.directionx = 'stand_left'

			if event.key == pygame.K_d:
				self.directionx = 'stand_right'

			if event.key == pygame.K_w:
				if self.rect.y <= 475:
					self.directiony = 'baixo'  

#criamos um grupo de sprites e uma classe para criar os mobs
mobs = pygame.sprite.Group()
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

	def __init__(self, x, y, width, height, end, vida, dano, direcao):
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
		self.rect = self.walkLeft[self.walkCount].get_rect()
		self.mask = pygame.mask.from_surface(self.walkRight[0])
		self.rect.x = self.x
		self.rect.y = self.y
		self.health = vida
		self.dano = dano
		self.direcao = direcao

	def draw(self):
		self.move()
		if self.walkCount + 1 >= 33:
			self.walkCount = 0

		if self.vel * self.direcao > 0:
			tela.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
			self.walkCount += 1
			self.mask = pygame.mask.from_surface(self.walkRight[0])

		else:
			tela.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
			self.walkCount += 1
			self.mask = pygame.mask.from_surface(self.walkLeft[0])

	def move(self):
		if self.vel * self.direcao > 0:
			if self.x < self.path[1] + self.vel:
				self.x += self.vel * self.direcao
			else:
				self.vel = self.vel * -1
				self.x += self.vel * self.direcao
				self.walkCount = 0
		else:
			if self.x + self.vel > self.path[0]:
				self.x += self.vel * self.direcao
			else:
				self.vel = self.vel * -1
				self.walkCount = 0

		self.rect.x = self.x
		self.rect.y = self.y

	#Aqui detectamos colisões com os tiros
	def hit(self, bala, acertos):
		if self.health > 0:
			self.health -= self.dano
		else:
			pygame.sprite.spritecollide(bala, mobs, True)
			morte.append(1)

			pygame.display.update()

#Criamos uma função responsavel por criar texto
def texto(texto, fonte, cor):
	tipo_texto = fonte.render(texto, True, cor)
	return tipo_texto, tipo_texto.get_rect()

#criamos uma função q cria botões
def butao(mensagem, x, y, largura, altura, cor_inativa, cor_ativa):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + largura > mouse[0] > x and y + altura > mouse[1] > y:
		pygame.draw.rect(tela, cor_ativa,(x,y,largura,altura))
		if click[0] == 1:
			return True
	else:
		pass

	texto_botao = pygame.font.Font('Kingthings_Calligraphica_2.ttf', 35)
	textSurf, textRect = texto(mensagem, texto_botao, cor_inativa)
	textRect.center = ((x+(largura/2)), (y+(altura/2)))
	tela.blit(textSurf, textRect)
	return False

#criamos uma função de pause
def pause():

	paused = True

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False

				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_e:
					pausado = 1
					Controles(pausado)

		TextSurf, TextRect = texto('Pausado', texto_grande, preto)
		TextRect.center = ((300), (75))
		tela.blit(TextSurf, TextRect)

		TextSurf, TextRect = texto('Pressione C para continuar, Q para sair ou E para ver as instruções', texto_pequeno, preto)
		TextRect.center = ((comprimento_display/2), (altura_display/2))
		tela.blit(TextSurf, TextRect)

		pygame.display.update()
	relogio.tick(5)
	pause = True

#criamos uma função para quando o player morre
def tela_morte():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return -1
			tela.fill(preto)
			TextSurf, TextRect = texto('faleceu', texto_grande, branco)
			TextRect.center = ((comprimento_display/2), (altura_display/2))
			tela.blit(TextSurf, TextRect)

			if pontuacao[0] > int(HighScore_antigo):
				fonte_highscore = pygame.font.SysFont(None, 50)
				texto_seuscore = fonte_highscore.render(
					"Sua Pontuação: "+str(pontuacao[0]), True, branco)
				texto_highscore = fonte_highscore.render(
					"Highscore: "+str(pontuacao[0]), True, branco)

				with open('HighScore.txt', 'w') as arquivo:
					arquivo.write(str(pontuacao[0]))

			else:
				fonte_highscore = pygame.font.SysFont(None, 50)
				texto_seuscore = fonte_highscore.render(
					"Sua Pontuação: "+str(pontuacao[0]), True, branco)
				texto_highscore = fonte_highscore.render(
					"Highscore: "+str(HighScore_antigo), True, branco)

			tela.blit(texto_seuscore,(15,15))
			tela.blit(texto_highscore,(50,50))
			if butao('Jogar Novamente', 318,425,75,25,(0,255,0),(128,128,128)):
				pontuacao[0] = 0
				return 2
			if butao('sair', 318,475,75,25,(255,0,0),(128,128,128)):
				return -1


			pygame.display.update()

#criamos uma função para o menu do jogo
def menu():
	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				return -1
		tela.blit(tela_menu, [0,0])
		TextSurf, TextRect = texto('Land of Blood', texto_grande, preto)
		TextRect.center = ((comprimento_display/2), (altura_display/2))
		tela.blit(TextSurf, TextRect)

		if butao('jogar', 318,425,75,25,(0,255,0),(128,128,128)):
			return 5
		if butao('sair', 318,525,75,25,(255,0,0),(128,128,128)):
			return -1

		if butao('comandos',318,475,75,25,(0,255,0),(128,128,128)):
			return 3

		pygame.display.update()
		relogio.tick(15)

#criamos uma função para criar uma tela com os comandos do jogo
def Controles(pausado):
	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				return -1

		#se pausado for = 1 , ele vai para a tela onde mostra os comandos do jogo
		if pausado == 1:
			tela.blit(tela_menu,[0,0])
			TextSurf, TextRect = texto('Controles', texto_grande, branco)
			TextRect.center = ((394), (75))
			tela.blit(TextSurf, TextRect)
			TextSurf, TextRect = texto('W,A,S,D para movimentar o personagem', texto_pequeno, branco)
			TextRect.center = ((300), (250))
			tela.blit(TextSurf, TextRect)
			TextSurf, TextRect = texto('Barra de Espaço para atirar', texto_pequeno, branco)
			TextRect.center = ((300), (275))
			tela.blit(TextSurf, TextRect)
			TextSurf, TextRect = texto('P para pausar', texto_pequeno, branco)
			TextRect.center = ((300), (300))
			tela.blit(TextSurf, TextRect)

			if butao('retornar ao jogo',318,450,75,25,(0,255,0),(128,128,128)):
				tela.blit(background,[0,0])
				return 4

		#caso contrário:		
		else:
			tela.blit(tela_menu,[0,0])
			TextSurf, TextRect = texto('Controles', texto_grande, branco)
			TextRect.center = ((394), (75))
			tela.blit(TextSurf, TextRect)
			TextSurf, TextRect = texto('W,A,S,D para movimentar o personagem', texto_pequeno, branco)
			TextRect.center = ((300), (250))
			tela.blit(TextSurf, TextRect)
			TextSurf, TextRect = texto('Barra de Espaço para atirar', texto_pequeno, branco)
			TextRect.center = ((300), (275))
			tela.blit(TextSurf, TextRect)
			TextSurf, TextRect = texto('P para pausar', texto_pequeno, branco)
			TextRect.center = ((300), (300))
			tela.blit(TextSurf, TextRect)

			if butao('retornar ao menu', 318,450,75,25,(0,255,0),(128,128,128)):
				return 0

		#estas condicionais servem para fazer com que esta tela funcione tanto no menu quanto no meio do jogo

		pygame.display.update()
		relogio.tick(15)

#criamos uma função que após a seleção de personagens, inicializa o jogo
def Comeco():
	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				return -1

		tela.fill(preto)
		TextSurf, TextRect = texto('Vamos Começar?', texto_grande, branco)
		TextRect.center = ((375), (75))
		tela.blit(TextSurf, TextRect)

		if butao('SIM!',300,450,100,50,(0,255,0),(128,128,128)):
			return 1


		pygame.display.update()
		relogio.tick(15)

#criamos uma função para a seleção de personagens
def character():
	global player
	global opcao
	global all_sprites

	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				return -1

		tela.blit(tela_HUB,[0,0])
		TextSurf, TextRect = texto('Selecione seu personagem', texto_pequeno, branco)
		TextRect.center = ((350), (75))
		tela.blit(TextSurf, TextRect)

		tela.blit(jogador1, [175,200])
		tela.blit(jogador2, [375,200])
		tela.blit(jogador3, [575,200])

		#Para cada personagem definimos um botão que especifica qual player foi escolhido


		if butao('Bahia',170,270,75,25,(0,255,0),(128,128,128)):
			player = Neguinho((0,475),jogador1)
			opcao = jogador1
			return 6


		if butao('Alê',350,270,75,25,(0,255,0),(128,128,128)):
			player = Neguinho((0,475),jogador2)
			opcao = jogador2
			return 6


		if butao('Terhorst',550,270,75,25,(0,255,0),(128,128,128)):
			player = Neguinho((0,475),jogador3)
			opcao = jogador3
			print('ma oe')
			return 6


		
		pygame.display.update()
		relogio.tick(15)

	all_sprites = pygame.sprite.Group()
	all_sprites.add(player)

lista_x = []

group_tiros = pygame.sprite.Group()

#criamos uma função para reiniciar o jogo depois que o player morreu
def reiniciar():
	player.rect.x = 0
	player.rect.y = 480
	vida = 10
	contador_imagem = 0
	return 1

#criamos uma função para fazer um Score
def ScoreBoard(grupo,mobz,pontuacao):

	if grupo > len(mobz):
		resultado = grupo - len(mobz)
		print('resultado vale {0}'.format(resultado))
		pontuacao[0] += (15*resultado)
		print('pontuação é: {0}'.format(pontuacao[0]))
	fonte_score = pygame.font.SysFont(None, 25)
	texto_score = fonte_score.render("Pontuação: "+str(pontuacao[0]), True, preto)
	tela.blit(texto_score,(15,15))

	pygame.display.update()

	return 1

pontuacao = [0]

#criamos uma função onde ocorre a parte principal do jogo
def jogo():

	contador_imagem = 'comeco'

	reinicio = True



	#Criamos os primeiros mobs
	for w in range(8):
		x = random.randrange(100,600)
		lista_x.append(x)
	for i in range(8):
		for o in lista_x:
			direcao_inicial = random.uniform(0, 1)
			direcao_inicial = (direcao_inicial * 2) - 1
			m = MOBs(o,490,52,52,690, vida1, dano1, direcao_inicial)
			mobs.add(m)
			if len(mobs) > 8 or len(mobs) > 7:
				break

	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				return -1
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_p:
					pause()
				if player.directionx == 'stand_left' or player.directionx == 'left':
					direcao = -1
				elif player.directionx == 'stand_right' or player.directionx == 'right':
					direcao = 1

				if pygame.key.get_pressed()[pygame.K_SPACE]:
					if len(group_tiros) <= 5:
						pygame.mixer.Sound.play(pygame.mixer.Sound("Gun+Silencer.wav"))
						group_tiros.add(
							Tiro((player.rect.x + (player.rect.width /2)),\
								 (player.rect.y + 45), VELOCIDADE, direcao))

			player.handle_event(evento)


		if contador_imagem == 'comeco' and reinicio == True:
			for w in range(8):
				x = random.randrange(100,600)
				lista_x.append(x)
			for i in range(8):
				for o in lista_x:
					m = MOBs(o,490,52,52,690, vida1, dano1, direcao_inicial)
					mobs.add(m)
					contador_imagem = 0
					if len(mobs) > 8 or len(mobs) > 7:
						break

		grupo_mobs = len(mobs)

		if len(mobs) == 0:
			contador_imagem += 1
			if contador_imagem == len(backgrounds):
				contador_imagem = 0
			for w in range(random.randrange(11,20)):
				x = random.randrange(100,600)
				lista_x.append(x)
				for i in range(15):
					for o in lista_x:
						m = MOBs(o,490,52,52,690, vida1, dano1, direcao_inicial)
						mobs.add(m)
						grupo_mobs = len(mobs)
						if len(mobs) > 8 or len(mobs) > 7:
							break

		for mob in mobs:
			mortes = pygame.sprite.spritecollide(
				player, mobs, True, pygame.sprite.collide_mask)
			for morte in mortes:
				return -2

			balas_atingidas = pygame.sprite.spritecollide(
					mob, group_tiros, True, pygame.sprite.collide_mask)
			for bala in balas_atingidas:
				mob.hit(bala, balas_atingidas)
				if player.x < mob.x:
					mob.x += 5
				else:
					mob.x -= 5

			#Aqui delimitamos as colisões do jogador com o cenário
			if player.rect.x <= 0:
				player.rect.x = 0
			if player.rect.x >= 736 - player.rect.width:
				player.rect.x = 736 - player.rect.width
			if player.rect.y >= 475:
				player.rect.y =  475

		background_novo = backgrounds[contador_imagem]

		#Aqui fazemos uma ação que troca de background toda vez que todos os mobs tiverem sido mortos

		if len(lista_x) > 8:
			tela.blit(background_novo, [0,0])

		if len(lista_x) == 8 and reinicio == True:
			tela.blit(background, [0,0])

		tela.blit(player.image, player.rect)
		group_tiros.draw(tela)

		for bixo in mobs:
			bixo.draw()
			
		#Aqui atualizamos tudo

		ScoreBoard(grupo_mobs,mobs,pontuacao)
		player.update()
		mobs.update()
		group_tiros.update()
		pygame.display.flip()
		pygame.display.update()
		relogio.tick(15)

#criamos o loop do jogo
def gameloop():
	# Variavel estado: em que estado o jogo se encontra
	# -2: tela de morte
	# -1: game over
	# 0: tela inicial
	# 1: proxima tela
	estado = 0
	#enquanto o jogo esta aberto
	while estado != -1:
		if estado == -2:
			estado = tela_morte()

		elif estado == -3:
			estado = nova_tela_morte()

		elif estado == 0:
			estado = menu()

		elif estado == 1:
			estado = jogo()

		elif estado == 2:
			estado = reiniciar()

		elif estado == 3:
			pausado = 0
			estado = Controles(pausado)

		elif estado == 4:
			estado = pause()

		elif estado == 5:
			estado = character()

		elif estado == 6:
			estado = Comeco()

#Ativamos a função do loop e ou fechamos o jogo
gameloop()
pygame.quit()

#FONTES:
#
#https://www.google.com/search?client=firefox-b-ab&biw=1696&bih=829&tbm=isch&sa=1&ei=6PYHW_7OLcqUwgSNjZrwCA&q=background+pixelado+floresta&oq=background+pixelado+floresta&gs_l=img.3...103953.112415.0.112571.34.29.3.2.2.0.146.2800.21j8.29.0....0...1c.1.64.img..0.24.1913...0j35i39k1j0i67k1j0i10k1j0i30k1j0i10i30k1j0i5i10i30k1j0i5i30k1j0i8i30k1.0.jIUYbIBiQaA#imgrc=keYFzz6zbI3HFM:
#https://pythonprogramming.net/adding-score-pygame-video-game/
#https://www.youtube.com/watch?v=vc1pJ8XdZa0
#https://www.google.com/imgres?imgurl=https%3A%2F%2Fhdbackgroundspot.com%2F%2Fstorage%2Fupload%2Fsprites-background%2Fsprites-background-13.png&imgrefurl=https%3A%2F%2Fhdbackgroundspot.com%2Farticle%2Ftop-92-sprites-background&docid=x9L2vsklbQ6URM&tbnid=47eBJOD_UE_TIM%3A&vet=10ahUKEwjQgcKYwtHbAhUMjpAKHaTWBOYQMwg3KAIwAg..i&w=504&h=240&client=firefox-b-ab&bih=829&biw=1696&q=sprites%20background&ved=0ahUKEwjQgcKYwtHbAhUMjpAKHaTWBOYQMwg3KAIwAg&iact=mrc&uact=8
#https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg00.deviantart.net%2F8e61%2Fi%2F2017%2F162%2F0%2F8%2Fbackground_and_midground_sprite_by_sacrosanity-dbccflt.png&imgrefurl=https%3A%2F%2Fsacrosanity.deviantart.com%2Fart%2FBackground-and-Midground-Sprite-685863425&docid=PFEtyQBhrVa9rM&tbnid=NIjAIU8c22dh0M%3A&vet=10ahUKEwjQgcKYwtHbAhUMjpAKHaTWBOYQMwhpKCowKg..i&w=1024&h=512&client=firefox-b-ab&bih=829&biw=1696&q=sprites%20background&ved=0ahUKEwjQgcKYwtHbAhUMjpAKHaTWBOYQMwhpKCowKg&iact=mrc&uact=8
#https://www.google.com/imgres?imgurl=http%3A%2F%2Fmoziru.com%2Fimages%2Fdrawn-cavern-sprite-6.png&imgrefurl=http%3A%2F%2Fmoziru.com%2Fexplore%2FDrawn%2520cavern%2520sprite%2F&docid=gjVYVDOpEWb5rM&tbnid=iy9WIhsA7ycoKM%3A&vet=12ahUKEwjDm82mwtHbAhUHk5AKHbpiAp84ZBAzKDswO3oECAEQPA..i&w=1600&h=574&client=firefox-b-ab&bih=829&biw=1696&q=sprites%20background&ved=2ahUKEwjDm82mwtHbAhUHk5AKHbpiAp84ZBAzKDswO3oECAEQPA&iact=mrc&uact=8
#https://www.google.com/imgres?imgurl=https%3A%2F%2Fs3.amazonaws.com%2Fzoraw.2draw.net%2Fdata%2F8%2F80388%2F80388-v3.png&imgrefurl=https%3A%2F%2F2draw.net%2Fview%2F80388%2F&docid=ZwC1M7PZEadxTM&tbnid=DmAOiAqEqvKhnM%3A&vet=12ahUKEwjDm82mwtHbAhUHk5AKHbpiAp84ZBAzKEwwTHoECAEQTQ..i&w=320&h=200&client=firefox-b-ab&bih=829&biw=1696&q=sprites%20background&ved=2ahUKEwjDm82mwtHbAhUHk5AKHbpiAp84ZBAzKEwwTHoECAEQTQ&iact=mrc&uact=8
#https://www.google.com/search?client=firefox-b-ab&biw=1696&bih=829&tbm=isch&sa=1&ei=XIUhW5DlIsWhwASzk5WoAg&q=+background+mario&oq=+background+mario&gs_l=img.3..0i67k1j0l2j0i7i30k1l4j0i30k1l3.48027.48027.0.48244.1.1.0.0.0.0.93.93.1.1.0....0...1c..64.img..0.1.93....0.RhAPACYW3BI#imgrc=_3Ik1xDL3U4XIM:
#https://hofarts.deviantart.com/art/Abandoned-city-background-404167869
#https://br.pinterest.com/pin/52706258114094348/
#https://www.google.com/search?tbs=sbi:AMhZZiuDtaHLKr355j6DKOabLLAcVAweyIPSmFmC06_1JX5kMDxY5u7WaQCzJY1NzrVXskVSDNU4Smq-fud2ZwwE_1w0RXZxHcOBtU9XYrDlreqZjgzLv7YUysK1ZXDvtQxlApujuwGqsIzGu3L6Vb_13iQM4udDYZHg0mRpyJjOrWACWbLF8mj5JphqQtlWYdTF5xaLlvKVxsVo_1RBXtqM12_1Yvs-9vx1Vwi8Be85HNNaQ279IfcZOgaY6v6joqlekMmO4CcHqRlnzrNDtX1wCr9goL6yLYSre1IAgY0eE-wDr6ilNxCAH4TDHUF3eS6zTWyeHcrRTQiZc&btnG=Pesquisa por imagem&hl=pt-BR
#https://www.google.com/search?sa=G&hl=pt-BR&q=tree&tbm=isch&tbs=simg:CAQSmQEJwsWE3pPOXEQajQELEKjU2AQaBggVCAUICAwLELCMpwgaYgpgCAMSKKALhQT0C7gWiAuGC4cEhATwC_1UL0yjKKNIopCrIKKEqvDflIdkhySgaMJYkedHknzlT79p5LxxDKNvQpPBtuEgsNtVAC0qg_12j55PGKLHZLmBQmOgJkARLOFCAEDAsQjq7-CBoKCggIARIEPOFRDAw&ved=0ahUKEwih-omjxtHbAhVMH5AKHW_cDJAQwg4IJSgA&biw=1696&bih=829
#https://www.google.com/search?client=firefox-b-ab&biw=1696&bih=829&tbm=isch&sa=1&ei=JzQZW42eN4WZwgT6n7-IDQ&q=terror+wallbrick+night&oq=terror+wallbrick+night&gs_l=img.3...2170.2488.0.3016.2.2.0.0.0.0.83.158.2.2.0....0...1c.1.64.img..0.0.0....0.tNPPUOewj8g#imgrc=SsnDwPopxVm3eM:
#http://xorobabel.blogspot.com/2012/10/pythonpygame-2d-animation-jrpg-style.html
#https://www.piskelapp.com/p/agxzfnBpc2tlbC1hcHByEwsSBlBpc2tlbBiAgMDv7uTTCQw/edit
#https://www.youtube.com/watch?v=33g62PpFwsE
#https://github.com/techwithtim/pygame-tutorials
#https://github.com/techwithtim/pygame-tutorials/tree/master/Game
#https://stackoverflow.com/questions/16643922/making-sprite-jump-in-pygame
#https://pt.stackoverflow.com/questions/252228/duvida-sobre-keypress-no-pygame
#https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.DirtySprite
#http://www.dsc.ufcg.edu.br/~pet/atividades/minicurso_pygame/MiniCursoPygame.pdf
#https://www.google.com.br/search?hl=pt-BR&q=window&tbm=isch&source=iu&ictx=1&tbs=simg:CAESqgIJD4q3C-fKc_18angILEKjU2AQaAggVDAsQsIynCBphCl8IAxIn2QPUA9gDWPwL1gXvAowJ1wPzAqc1hzeIN_181_1TaDN-w1jD3UNecpGjANWzKRgAjt4lwHasVjO-9_1Ri-md_15tc135FCe1exQ1Ql_1xEZeJ1VRjSfSdy9bQ7uwgBAwLEI6u_1ggaCgoICAESBKshkZwMCxCd7cEJGowBChgKBndpbmRvd9qliPYDCgoIL20vMGQ0djQKFwoFaG91c2XapYj2AwoKCC9tLzAzam01ChYKBHdvb2TapYj2AwoKCC9tLzA4M3Z0Ch8KDGFyY2hpdGVjdHVyZdqliPYDCwoJL20vMDNuZm1xCh4KC3NjYWxlIG1vZGVs2qWI9gMLCgkvbS8wMXJoN3kM&fir=gEf1t5mOiwVmeM%253A%252C4aHRhjKqy13I0M%252C_&usg=__mnm23F3H2mk1YKJdMBL-H8iMXCM%3D&sa=X&ved=0ahUKEwjEg_aGy9HbAhUIlpAKHS7aDWsQ9QEIOTAC#imgrc=gEf1t5mOiwVmeM:
#https://www.google.com.br/search?sa=G&hl=pt-BR&q=game+main+menu+background&tbm=isch&source=iu&ictx=1&tbs=simg:CAESpQIJM5cGpO3Q_1EIamQILEKjU2AQaBAgVCAEMCxCwjKcIGmIKYAgDEijoFbgOkwvnFYIYuQ7vF7wMtw6wDLUttiDLLcgkrDeFIKo35CjRLLktGjAObNI18WQPF8LP_1yFwI5cZmdTyZcMfGWj_1uOE-8PZlJcvfToq3P6vbEbLhjN0yVwsgBAwLEI6u_1ggaCgoICAESBHHqu8oMCxCd7cEJGoQBChsKCGRhcmtuZXNz2qWI9gMLCgkvbS8wMWt5cjgKGQoGdHVubmVs2qWI9gMLCgkvbS8wMTU4dnQKGAoFYWxsZXnapYj2AwsKCS9tLzAxbHdmMAoYCgVuaWdodNqliPYDCwoJL20vMDFkNzR6ChYKBG1vb27apYj2AwoKCC9tLzA0d3ZfDA&fir=lLSdo9A7PLTkmM%253A%252CdF4C12fj2cLJqM%252C_&usg=__7nxX67Bl9R8HJKSDRZhcOW2H-vA%3D&ved=0ahUKEwiQvdv0ztHbAhVDDJAKHVyRDYsQ9QEIQDAC#imgrc=lLSdo9A7PLTkmM:

