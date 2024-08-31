import pygame
import sys
import os
from pygame.locals import *
from random import randint
#versão Alfa 0.1

#inicialização
pygame.init()
pygame.mixer.init() 

#tela
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h
janela = pygame.display.set_mode((largura, altura), FULLSCREEN)
#frames
FPS = 60
fps = pygame.time.Clock()
#classe do jogador
class Jogador(pygame.sprite.Sprite):

    def __init__(self,vida,oxigenio,velocidadeJogador,gravidade,posicaoX,posicaoY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('Entidades/SpritesJogador/argonaut.png'))
        self.sprites.append(pygame.image.load('Entidades/SpritesJogador/jogador2.png'))
        self.sprites.append(pygame.image.load('Entidades/SpritesJogador/jogador3.png'))
        self.sprites.append(pygame.image.load('Entidades/SpritesJogador/jogador4.png'))
        self.sprites.append(pygame.image.load('Entidades/SpritesJogador/jogador5.png'))
        self.image = self.sprites[0]

        #criar retângulo do jogador,coletando coordenadas ao redor da imagem
        self.rect = self.image.get_rect()
    
        #posicao do sprite
        self.rect.topleft = (posicaoX,posicaoY)

        #Propiedades do Jogador
        self.vida = vida
        self.oxigenio = oxigenio
        self.velocidadeJogador = velocidadeJogador
        self.direcao = 1  # 1 para direita, -1 para esquerda

        #controle de Pulo
        self.velocidadeVertical = 0
        self.pulando = False
        self.gravidade = gravidade
        self.chao = altura - 500

        #controle de animação
        self.animacao_index = 0
        self.contador_frames = 0
        self.velocidade_animacao = 5 #5 velocidade da animação


    def update(self):
        #movimentação do Jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.velocidadeJogador
            self.movendo = True
            self.direcao = -1
                  
        elif keys[pygame.K_d]:
            self.rect.x += self.velocidadeJogador
            self.movendo = True
            self.direcao = 1  # Virar para a direita
        else:
            self.movendo = False
            self.image = self.sprites[0]
  
            

        if keys[pygame.K_SPACE] and not self.pulando:
          self.pulando = True

          self.velocidadeVertical = -30

        #aplicando a gravidade
        self.velocidadeVertical += self.gravidade
        self.rect.y += self.velocidadeVertical

        #Verificando condição do jogador no chão
        if self.rect.y >= self.chao:
            self.rect.y = self.chao
            self.pulando = False
            self.velocidadeVertical = 0

        if self.movendo:
            self.animate() 
            self.image = pygame.transform.flip(self.sprites[self.animacao_index], self.direcao == -1, False)   
    def animate(self):

        # Controla a animação do jogador
        self.contador_frames += 1
        if self.contador_frames >= self.velocidade_animacao:
            self.contador_frames = 0
            self.animacao_index += 1
            if self.animacao_index >= len(self.sprites):
                self.animacao_index = 0  # Volta para o início da animação

            self.image = self.sprites[self.animacao_index]    

    def set_gravidade(self, nova_gravidade):
        self.gravidade = nova_gravidade

    def draw(self,janela):
        janela.fill((0, 0, 0))  # Limpa a tela com preto
        janela.blit(self.image,self.rect)
        self.sprites.draw(self.janela)  # Desenha todos os sprites (incluindo o jogador)
        pygame.display.flip()  # Atualiza a tela         
class Menu:    
    def __init__(self, janela):
            self.janela = janela
            self.imagem_de_menu = pygame.image.load('ConfigMenusEtc/MenuSingularity.jpeg')
            self.imagem_menu_transformada = pygame.transform.scale(self.imagem_de_menu, (largura, altura))
            self.musica_menu = 'MusicSingularity/Singularity2200MenuSoundtrack.wav'

    def tocar_musica_menu(self):
            pygame.mixer.music.load(self.musica_menu)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def parar_musica_menu(self):
            pygame.mixer.music.stop()

    def exibir_menu(self):
            self.tocar_musica_menu()
            jogo_ativo = False

            while not jogo_ativo:
                self.janela.fill((255, 255, 255))
                self.janela.blit(self.imagem_menu_transformada, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == K_p:
                            self.parar_musica_menu()
                            jogo_ativo = True
                pygame.display.flip()            

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.info = pygame.display.Info()
        self.largura = self.info.current_w
        self.altura = self.info.current_h
        self.janela = pygame.display.set_mode((self.largura, self.altura), FULLSCREEN)
        self.fps = pygame.time.Clock()
        self.FPS = 60
        self.menu = Menu(self.janela)
        
    def iniciar_jogo(self):
        jogador = Jogador(vida=100, oxigenio=100, velocidadeJogador=5, gravidade=0.8, posicaoX=self.largura//2, posicaoY=self.altura//2)
        todos_sprites = pygame.sprite.Group()
        todos_sprites.add(jogador)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()        

            todos_sprites.update()
            self.janela.fill((0, 0, 0))
            todos_sprites.draw(self.janela)
            pygame.display.flip()
            self.fps.tick(self.FPS)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu.exibir_menu()
    jogo.iniciar_jogo()
