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

class Cenario:
    def __init__(self, imagem_fundo, gravidade, velocidade_jogador_max):
        self.imagem_fundo = pygame.image.load('Entidades/scenarios/mercury1.jpeg').convert()
        self.gravidade = gravidade
        self.velocidade_jogador_max = velocidade_jogador_max
        self.largura = self.imagem_fundo.get_width()
        self.altura = self.imagem_fundo.get_height()

    def desenhar(self, janela):
        janela.blit(self.imagem_fundo, (0, 0))

class GerenciadorCenario:
    def __init__(self, janela):
        self.janela = janela
        self.cenarios = []  # Lista de cenários do planeta
        self.index_cenario_atual = 0

    def adicionar_cenario(self, cenario):
        self.cenarios.append(cenario)

    def atualizar_cenario(self, jogador):
        # Se o jogador chega ao fim da tela, passar para o próximo cenário
        if jogador.rect.right >= self.janela.get_width():
            self.index_cenario_atual += 1
            if self.index_cenario_atual >= len(self.cenarios):
                self.index_cenario_atual = 0  # Reinicia ou pode terminar a fase
            jogador.rect.x = 0  # Reposicionar o jogador no início da nova tela

    def obter_gravidade(self):
        return self.cenarios[self.index_cenario_atual].gravidade

    def obter_velocidade_max(self):
        return self.cenarios[self.index_cenario_atual].velocidade_jogador_max

    def desenhar_cenario(self):
        self.cenarios[self.index_cenario_atual].desenhar(self.janela)



class Jogador(pygame.sprite.Sprite):

    def __init__(self,vida,oxigenio,velocidadeJogador,gravidade,posicaoX,posicaoY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        heightPlayer = 100 ; widthPlayer = 100
        self.sprites.append(pygame.transform.scale(pygame.image.load('Entidades/SpritesJogador/argonaut.png'), (heightPlayer, widthPlayer)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('Entidades/SpritesJogador/jogador2.png'), (heightPlayer, widthPlayer)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('Entidades/SpritesJogador/jogador3.png'), (heightPlayer, widthPlayer)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('Entidades/SpritesJogador/jogador4.png'), (heightPlayer, widthPlayer)))
        self.sprites.append(pygame.transform.scale(pygame.image.load('Entidades/SpritesJogador/jogador5.png'), (heightPlayer, widthPlayer)))
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
        jogador = Jogador(vida=100, oxigenio=100, velocidadeJogador=5, gravidade=2, posicaoX=self.largura//2 - 100, posicaoY=self.altura*8)
        todos_sprites = pygame.sprite.Group()
        todos_sprites.add(jogador)
        cenario_merc1 = Cenario('planetas/mercurio_cenario1.png', gravidade=0.98, velocidade_jogador_max=5)
        gerenciador_cenario = GerenciadorCenario(self.janela)
        gerenciador_cenario.adicionar_cenario(cenario_merc1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()  

            gerenciador_cenario.atualizar_cenario(jogador)
            jogador.gravidade = gerenciador_cenario.obter_gravidade()
            jogador.velocidade_max = gerenciador_cenario.obter_velocidade_max()                  

            todos_sprites.update()

            self.janela.fill((0,0,0))

            gerenciador_cenario.desenhar_cenario()

            todos_sprites.draw(self.janela)

            pygame.display.flip()

            self.fps.tick(self.FPS)

if __name__ == "__main__":
    jogo = Jogo()
    jogo.menu.exibir_menu()
    jogo.iniciar_jogo()
