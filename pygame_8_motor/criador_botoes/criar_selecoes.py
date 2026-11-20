from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COPIADO
from codigo_compartilhado   import Cor_Opcoes
from codigo_compartilhado   import Imagem_Opcoes

# PARENTE
try:
    from botao                  import Botao
    from conjunto_botoes        import Conjunto_Botoes
except ModuleNotFoundError:
    from .botao                  import Botao
    from .conjunto_botoes        import Conjunto_Botoes

# PYGAME
from pygame                 import Color    as Cor , Rect as Retangulo
from pygame                 import Surface  as Superficie 
from pygame                 import K_RETURN as ENTER


"=== CÓDIGO REAL ==="


class Seleção_Horizontal(Conjunto_Botoes):
    def __init__( _ , 
        *textos                             : tuple[str] | Retangulo ,
            dimensao_geral                  : Retangulo  | tuple , 
                base                        : Cor_Opcoes | Imagem_Opcoes , 
                    ev_gravado              : int   = ENTER,
                        espaçamento         : int   = 0 , 
                            cor_texto       : tuple = ( 255 , 255 , 255 ) ,
                                fixar_cor_texto = False ):

        _.__espaçamento = espaçamento

        conjunto = _.conjunto_retangulos( textos , dimensao_geral )

        super().__init__( textos , conjunto , base , ev_gravado , cor_texto , fixar_cor_texto)

    def conjunto_retangulos( _ , textos , dimensao ):
        conjunto = []
        distancia_entre_bt = 0
        for numero in range(len(textos)):
            pos_x   = dimensao[0] + distancia_entre_bt
            pos_y   = dimensao[1]

            if type(dimensao) == Retangulo:
                '( dimensao[2] * numero ) + espaçamento*numero'

                largura = dimensao[2]
                altura  = dimensao[3]
                
            elif type(dimensao) == tuple:
                tamanho = Botao.fonte().size(textos[numero])

                largura = 50 + tamanho[0]
                altura  = tamanho[1] * 2.5

            conjunto.append( Retangulo( pos_x , pos_y , largura , altura ) )

            distancia_entre_bt += conjunto[-1][2] + _.espaçamento

        return conjunto
        
    @property
    def espaçamento( _ ) -> int:
        return _.__espaçamento

    @espaçamento.setter
    def espaçamento( _ , novo: int ):
        diferença =  novo - _.__espaçamento 

        ddd = diferença
        for bt in _.botoes[1:]:
            bt.x += ddd

            ddd = ddd + diferença

        _.__espaçamento = novo

class Seleção_Vertical(Conjunto_Botoes):
    def __init__( _ , 
            *textos                             : tuple[str] | Retangulo ,
                dimensao_geral                  : Retangulo  | tuple , 
                    base                        : Cor_Opcoes | Imagem_Opcoes , 
                        ev_gravado              : int   = ENTER,
                            espaçamento         : int   = 0 , 
                                cor_texto       : tuple = ( 255 , 255 , 255 ) ,
                                    fixar_cor_texto = False ):
    
        _.__espaçamento = espaçamento

        conjunto = _.conjunto_retangulos( textos , dimensao_geral )

        super().__init__( textos , conjunto , base , ev_gravado , cor_texto , fixar_cor_texto)

    def conjunto_retangulos( _ , textos , dimensao ):
        conjunto = []
        distancia_entre_bt = 0
        for numero in range(len(textos)):
            pos_x   = dimensao[0] 
            pos_y   = dimensao[1] + distancia_entre_bt

            if type(dimensao) == Retangulo:
                '( dimensao[2] * numero ) + espaçamento*numero'

                largura = dimensao[2]
                altura  = dimensao[3]
                
            elif type(dimensao) == tuple:
                tamanho = Botao.fonte().size(textos[numero])

                largura = 50 + tamanho[0]
                altura  = tamanho[1] * 2.5

            conjunto.append( Retangulo( pos_x , pos_y , largura , altura ) )

            distancia_entre_bt += conjunto[-1][3] + _.espaçamento

        return conjunto
            
    @property
    def espaçamento( _ ) -> int:
        return _.__espaçamento

    @espaçamento.setter
    def espaçamento( _ , novo: int ):
        diferença =  novo - _.__espaçamento 

        ddd = diferença
        for bt in _.botoes[1:]:
            bt.y += ddd

            ddd = ddd + diferença

        _.__espaçamento = novo


'=== TESTES ==='


if __name__ == "__main__":
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from codigo_compartilhado   import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER , K_SPACE as SPACE
    from pygame                 import Event as Evento

    # pygame setup
    pygame.init()
    screen      = pygame.display.set_mode((1280, 720))
    clock       = pygame.time.Clock()
    running     = True

    imagem      = Imagem_Opcoes( carregar_imagem( Linkzin('banco_dados','Cenarios','introcomp_menu.png', act_dir= True) ) )
    cores       = Cor_Opcoes( Cor( 100 , 100 , 100 ) ) 

    base_cor    = Cor(100,100,100)
    
    conteudo = Seleção_Vertical( "A",  "BB" , 'CCC' ,
                                dimensao_geral  = (1000,100) , 
                                base            = cores     ,
                                ev_gravado      = SPACE     ,
                                espaçamento     = 10        ,
                                cor_texto       = (100,0,0) )

    '''extra    = Conjunto_Botoes( "ENTRAR" ,'HAHAHAHA',
                                dimensao_geral = Retangulo(200,300,300,100) , 
                                    base = base_cor ,
                                    espaçamento=50)'''

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
                    conteudo.foco += 1
                    'extra.foco += 1'
                if event.key == pygame.K_LEFT:
                    conteudo.foco -= 1
                    'extra.foco -=1'

                if event.key == SPACE:
                    'conteudo.espaçamento += 1'

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        conteudo( screen , eventos )
        'extra(screen , eventos)'

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
        
    