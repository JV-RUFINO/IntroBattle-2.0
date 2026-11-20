from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# PYGAME
from pygame          import Rect    as Retangulo
from pygame.font     import Font    as Fonte


"=== CÓDIGO REAL ==="


class Dimensoes:
    def __init__( _ , retangulo : Retangulo | tuple[int,int,int,int] ):
        if type( retangulo ) == tuple:
            retangulo = Retangulo( *retangulo )

        _.__dimensao_original = retangulo

        _.dimensoes = _.original_reproduzida

    @property
    def original_reproduzida( _ ) -> Retangulo:
        return Retangulo( _.__dimensao_original[0] , _.__dimensao_original[1] , _.__dimensao_original[2] , _.__dimensao_original[3] )

    @property
    def x( _ ) -> int:
        return _.dimensoes.x

    @x.setter
    def x( _ , novo : int ):    
        _.dimensoes.x = novo

    @property
    def y( _ ) -> int:
        return _.dimensoes.y

    @y.setter
    def y( _ , novo : int ):
        _.dimensoes.y = novo

    @property
    def altura( _ ) -> int:
        return _.dimensoes.height

    @altura.setter
    def altura( _ , novo : int ):
        _.dimensoes.height = novo

    @property
    def largura( _ ) -> int:
        return _.dimensoes.width

    @largura.setter
    def largura( _ , novo : int ):
        _.dimensoes.width = novo

    @property
    def ponto_inicial( _ ) -> tuple:
        return _.x , _.y

    def pos_frase( _ , fonte: Fonte , texto : str ) -> tuple[ int , int ]:
        tt2 = fonte.size( texto )

        return _.ponto_inicial[0] + (_.largura / 2) - (tt2[0] / 2) , _.ponto_inicial[1] + _.altura / 4

    def resetar( _ ) -> None:
        _.dimensoes = _.original_reproduzida


"=== TESTES ==="


if __name__ == "__main__":
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from codigo_compartilhado  import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
    from pygame                 import Event as Evento

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    conteudo = Dimensoes( (100,100,100,100) )

    print(conteudo.altura)

    pygame.quit()
      
    