from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# PARENTE
try:
    from opcoes_gerais                      import Opcoes_Geral as OG
except ModuleNotFoundError:
    from codigo_compartilhado.opcoes_gerais import Opcoes_Geral as OG

# PYGAME
from pygame             import Surface as Superficie 
from pygame.transform   import scale   as escalar_imagem
from pygame.image       import load     as carregar_imagem


"=== CÓDIGO REAL ==="


class Imagem_Opcoes(OG):
    def __init__( _ , imagem : Superficie , imagem_alternativa : Superficie | None = None ):        
        if type(imagem) == str:
            imagem = carregar_imagem( imagem )

        super().__init__( imagem )

        _.original      : Superficie
        _.moldavel      : Superficie
        _.alternativo   : bool

        if type(imagem_alternativa) == str:
            imagem_alternativa = carregar_imagem( imagem_alternativa )
        elif type( imagem_alternativa ) == None:
            imagem_alternativa = imagem

        _.imagem_alternativa  = imagem
        _.alt_moldavel        = _.alternativa_reproduzida

    def __escalar_imagem( _ , nova_largura : int | None , nova_altura : int | None ):
        larg = _.dimensoes[0] if nova_largura   is None else nova_largura
        alt  = _.dimensoes[1] if nova_altura    is None else nova_altura

        return escalar_imagem( _.moldavel , ( larg , alt ) )

    @property
    def original_reproduzida( _ ) -> Superficie:
        return _.original.copy()

    @property
    def alternativa_reproduzida( _ ) -> Superficie | None:
        return _.imagem_alternativa.copy()

    @property
    def dimensoes( _ ):
        return _.moldavel.get_size()

    @dimensoes.setter
    def dimensoes( _ , nova_dimensao : tuple[int,int] ):
        _.moldavel      = _.__escalar_imagem( nova_dimensao[0] , nova_dimensao[1] )
        _.alt_moldavel  = _.__escalar_imagem( nova_dimensao[0] , nova_dimensao[1] )
    
    @property
    def altura( _ ) -> int:
        return _.moldavel.get_height()

    @altura.setter
    def altura( _ , novo : int ):
        _.moldavel      = _.__escalar_imagem( None , novo )
        _.alt_moldavel  = _.__escalar_imagem( None , novo )
    
    @property
    def largura( _ ) -> int:
        return _.moldavel.get_width()

    @largura.setter
    def largura( _ , novo : int ):
        _.moldavel      = _.__escalar_imagem( novo , None )
        _.alt_moldavel  = _.__escalar_imagem( novo , None )

    def resetar( _ ):
        _.moldavel      = _.original_reproduzida
        _.alt_moldavel  = _.alternativa_reproduzida

    def tela_cheia( _ , superficie : Superficie ):
        tamanho = superficie.size

        _.moldavel      = _.__escalar_imagem( tamanho[0] , tamanho[1] )
        _.alt_moldavel  = _.__escalar_imagem( tamanho[0] , tamanho[1] )

    def printar_imagem( _ , superficie : Superficie , posicao : tuple[int,int] = (0,0) ):
        superficie.blit( _.moldavel, posicao ) # texto da caixa

    def __call__( _ , superficie : Superficie , posicao : tuple[int,int] = (0,0) ):
        _.printar_imagem( superficie, posicao )


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

    imagem      = carregar_imagem( 'introcomp_menu.png' )

    conteudo    = Imagem_Opcoes( imagem )

    conteudo.dimensoes = ( 200 , 200 )

    print(conteudo)

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
                if event.key == pygame.K_RIGHT:
                    conteudo.largura += 1
                if event.key == pygame.K_LEFT:
                    conteudo.altura += 1 
                if event.key == pygame.K_RETURN:
                    conteudo.resetar( )

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        conteudo( screen , (100,100) )

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
      
    