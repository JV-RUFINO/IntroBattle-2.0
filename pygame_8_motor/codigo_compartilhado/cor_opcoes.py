from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# PARENTES
try:
    from opcoes_gerais                      import Opcoes_Geral as OG
except ModuleNotFoundError:
    from codigo_compartilhado.opcoes_gerais import Opcoes_Geral as OG

# PYGAME
from pygame          import Color   as Cor 


"=== CÓDIGO REAL ==="


class Cor_Opcoes(OG):
    def __init__( _ , cor : Cor | tuple[int,int,int] ):
        if type( cor ) == tuple:
            cor = Cor( *cor )

        super().__init__( cor )

        _.original      : Cor
        _.moldavel      : Cor 
        _.alternativo   : bool

    def __mudar_cor( _ , nova_cor : int ):
        if nova_cor > 255:
            nova_cor = 255
        elif nova_cor < 0:
            nova_cor = 0

        return nova_cor

    def __cor_alternativa( _ , numero_mudança : int ) -> Cor:
        r = _.__mudar_cor( _.vermelho   + numero_mudança )
        g = _.__mudar_cor( _.verde      + numero_mudança )
        b = _.__mudar_cor( _.azul       + numero_mudança )

        return Cor( r , g , b )

    @property
    def original_reproduzida( _ ) -> Cor:
        return Cor( _.original.r , _.original.g , _.original.b )

    @property
    def vermelho( _ ) -> int:
        return _.moldavel.r

    @vermelho.setter
    def vermelho( _ , novo : int ):
        _.moldavel.r = _.__mudar_cor( novo )

    @property
    def verde( _ ) -> int:
        return _.moldavel.g

    @verde.setter
    def verde( _ , novo : int ):
        _.moldavel.g = _.__mudar_cor( novo )

    @property
    def azul( _ ) -> int:
        return _.moldavel.b

    @azul.setter
    def azul( _ , novo : int ):
        _.moldavel.b = _.__mudar_cor( novo )

    @property
    def cor_alternativa( _ ) -> Cor:
        return _.__cor_alternativa( 80 )

    @property
    def cor_foco( _ ) -> Cor:
        return _.__cor_alternativa( 40 ) if _.alternativo == False else _.cor_alternativa

    @property
    def cor_borda( _ ) -> Cor:
        return _.__cor_alternativa( 20 ) if _.alternativo == False else _.__cor_alternativa(60)

    @property
    def cor( _ ) -> Cor:
        return _.moldavel if _.alternativo == False else _.cor_alternativa

    def resetar( _ ):
        _.moldavel = _.original_reproduzida


"=== TESTES ==="


if __name__ == "__main__":
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from codigo_compartilhado.linkzin  import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
    from pygame                 import Event as Evento

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    conteudo = Cor_Opcoes( (100,100,100) )

    print(conteudo.cor)

    pygame.quit()
      
    