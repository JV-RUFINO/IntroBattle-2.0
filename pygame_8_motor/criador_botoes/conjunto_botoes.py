from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# CODIGO COPIADO
from codigo_compartilhado   import repetidor_de_func
from codigo_compartilhado   import Cor_Opcoes
from codigo_compartilhado   import Imagem_Opcoes

# PARENTE
try:
    from botao                  import Botao
except ModuleNotFoundError:
    from .botao                  import Botao

# PYGAME
from pygame                 import Color    as Cor , Rect as Retangulo
from pygame                 import Surface  as Superficie 
from pygame                 import K_RETURN as ENTER 


"=== CÓDIGO REAL ==="


@repetidor_de_func()
def repetir_valores( classe , funcao , *args, **kwargs ):
    return classe

class Conjunto_Botoes:
    __foco = 0

    def __init__( _ , textos : tuple[str], dimensoes: tuple[Retangulo] , base : Retangulo | tuple , ev_gravado : int = ENTER , cor_texto : tuple = ( 255 , 255 , 255 ) , fixar_cor_texto = False ):
        _.botoes = []
        
        _.__ev_gravado      = ev_gravado
        _.__cor_texto       = Botao.transformador(cor_texto)
        _.__fixar_cor_texto = fixar_cor_texto
        _.__base            = base

        _.adcionar_botoes( textos , dimensoes )

        _.botoes : list[Botao]
                
        _.resetar_foco()

    def resetar_foco( _ ):
        for bt in range(len(_.botoes)):
            _.botoes[bt].foco = True if bt == _.foco else False

    def adcionar_botoes( _ , textos : tuple[str] , dimensoes : Retangulo  | tuple ) -> list[Botao]:                            
        for numero in range(len(dimensoes)):
            novo = Botao( dimensoes[numero] , _.base , _.ev_gravado , textos[numero] , _.cor_texto , _.fixar_cor_texto )

            _.botoes.append( novo )

        return _.botoes
    
    def repetir_valores( _ , funcao : function ):
        return repetir_valores( _.botoes , funcao )
    
    @property
    def foco( _ ):
        return _.__foco

    @foco.getter
    def botao_focado( _ ) -> Botao:
        return _.botoes[_.__foco] 

    @foco.setter
    def foco( _ , novo : int ):
        _.botao_focado : Botao

        _.botao_focado.foco         = False
        _.botao_focado.alternativo  = False

        if novo >= len(_.todos_focos):
            novo = 0
        elif novo < 0:
            novo = len(_.todos_focos) - 1

        _.__foco = novo

        _.botao_focado.foco = True

    @property
    def ev_gravado( _ ):
        return _.__ev_gravado

    @ev_gravado.setter
    def ev_gravado( _ , novo_evento: int):
        for bt in _.botoes:
            bt.ev_gravado  = novo_evento
            bt.alternativo = False

        _.__ev_gravado = novo_evento

    @property
    def cor_texto( _ ) -> Cor_Opcoes:
        return _.__cor_texto

    @cor_texto.setter
    def cor_texto( _ , nova_cor : Cor | Cor_Opcoes ):
        n = Botao.transformador( nova_cor )

        for bt in _.botoes:
            bt.cor_texto = n

        _.__cor_texto = n

    @property
    def fixar_cor_texto( _ ):
        return _.__fixar_cor_texto

    @fixar_cor_texto.setter
    def fixar_cor_texto( _ , definicao: bool ):
        for bt in _.botoes:
            bt.cor_texto_fixo = definicao

        _.__fixar_cor_texto = definicao

    @property
    def base( _ ):
        return _.__base

    @base.setter
    def base( _ , novo : ...):
        for bt in _.botoes:
            bt.botao = bt.transformador(novo)

        _.__base = novo

    @property
    def todas_dimensoes( _ ) -> list[Retangulo]:
        return _.repetir_valores( lambda botao: botao.dimensoes )

    @property
    def todos_textos( _ ) -> list[str]:
        return _.repetir_valores( lambda botao: botao.texto )

    @property
    def todos_eventos( _ ) -> list[int]:
        return [ bt.ev_gravado for bt in _.botoes]

    @property
    def todos_focos( _ ) -> list[bool]:
        return [ bt.foco for bt in _.botoes ]

    def rodar_atual( _ , screen : Superficie , evs: list ):
        _.botao_focado( screen , evs )

    def rodar_todos( _ , screen : Superficie , evs: list ):
        for botao in _.botoes:
            botao( screen , evs )

    def __call__( _ , screen : Superficie , evs: list ):
        _.rodar_todos( screen , evs )


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
    
    conteudo = Conjunto_Botoes( textos          = ("A", "B") ,
                                dimensoes       = (Retangulo(100,100,100,100),Retangulo(200,200,100,100)) , 
                                base            = cores     ,
                                ev_gravado      = SPACE     ,
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
                    'print("bang")'
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
        
    