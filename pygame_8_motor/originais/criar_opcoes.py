from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COPIADO
from compartilhado.linkzin import Linkzin

# PYGAME
from pygame          import Color   as Cor , Surface as Superficie , Rect as Retangulo
from pygame.draw     import rect    as desenhar_retangulo
from pygame.font     import Font    as Fonte
from pygame.event    import Event

from pygame          import K_LEFT  as ESQUERDA , K_RIGHT as DIREITA

# IMPORTAÇÕES GERAIS
from dataclasses     import dataclass


"=== CÓDIGO REAL ==="


@dataclass
class Printar_Opções:
    cor_geral       : Cor
    opcoes          : tuple = ("LUTAR","MAGIA","FALAR","PULAR")

    __dimenções     : Retangulo = Retangulo( 100 , 550 , 200 , 100 )
    __espaçamento   : int   = 300
    __CONTAGEM      : int   = 0
        
    @staticmethod
    def fonte():
        return Fonte(Linkzin('fonte_jogo',"fontePygame.ttf", act_dir= True),32)

    @property
    def dimenções( _ ):
        return Retangulo( _.__dimenções.left , _.__dimenções.top , _.__dimenções.width , _.__dimenções.height )

    @property
    def opcao_escolhida( _ ):
        return _.opcoes[_.contagem]

    @property
    def contagem( _ ):
        return _.__CONTAGEM

    def mudar_selecionado( _ , evento : Event ):
        if evento == DIREITA:
            resultado = 1
        elif evento == ESQUERDA:
            resultado = -1
        
        _.__CONTAGEM += resultado

        maximo = len( _.opcoes ) - 1

        if _.__CONTAGEM > maximo:
            _.__CONTAGEM = 0
        elif _.__CONTAGEM < 0:
            _.__CONTAGEM = maximo

    @property
    def cor( _ ):
        return _.cor_geral

    @cor.getter
    def cor_borda( _ ):
        return Cor( _.cor_geral.r + 20 , _.cor_geral.b + 20, _.cor_geral.b + 20 )

    @cor.getter
    def cor_borda_alt( _ ):
        return Cor( _.cor_geral.r + 60 , _.cor_geral.b + 60, _.cor_geral.b + 60 )
    
    @property
    def pos_frase( _ ): # posicao da frase
        novo = _.dimenções
        novo.left += 30
        novo.top  += 30

        return novo

    def __call__( _ , screen : Superficie ):
        carregar_fonte  = _.fonte()
        dim_extra       = _.dimenções
        pos_frase       = _.pos_frase
        numero          = 0

        for opcao in _.opcoes:
            cor_borda = _.cor_borda if numero != _.contagem else _.cor_borda_alt

            desenhar_retangulo( screen , _.cor     , dim_extra )
            desenhar_retangulo( screen , cor_borda , dim_extra , width= 14 )

            screen.blit( carregar_fonte.render( opcao, False , (255, 255, 255) ) , 
                            pos_frase ) # texto da caixa
            
            dim_extra.left += _.__espaçamento
            pos_frase.left += _.__espaçamento

            numero += 1


"=== TESTES ==="


if __name__ == "__main__":
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from compartilhado.linkzin  import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
    from pygame                 import Event as Evento

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    conteudo = Printar_Opções(Cor(125,125,125),("VOLTAR",), Retangulo(500,550,220,100))

    # Example file showing a basic pygame "game loop"
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        eventos = pygame.event.get()
        
        for event in eventos:
            event : Evento

            if event.type == pygame.QUIT:
                running = False

                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    conteudo.mudar_selecionado( event.key )
                if event.key == pygame.K_RIGHT:
                    conteudo.mudar_selecionado( event.key )

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        'C( screen , novo_evento = eventos ,index= C.estoque_elos)'

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
      
    