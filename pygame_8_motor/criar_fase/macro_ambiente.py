from __future__ import annotations

from sys import path as caminho
from pathlib import Path as Caminhozão

arquivo = Caminhozão(__file__).resolve()
parente , raiz = arquivo.parent, arquivo.parents[1]
caminho.append(str(raiz))

# PARENTE
try:
    from micro_cena                 import Micro_Cena           as MC
    from rolo_cenas                 import Rolo_Cenas           as RC
    from rodar_cenas                import Rodar_Cenas          as RR
    from ambiente_interativo        import Ambiente_Interativo  as AI
except ModuleNotFoundError:
    from .micro_cena                 import Micro_Cena           as MC
    from .rolo_cenas                 import Rolo_Cenas           as RC
    from .rodar_cenas                import Rodar_Cenas          as RR
    from .ambiente_interativo        import Ambiente_Interativo  as AI

# ESSENCIAIS
from codigo_compartilhado       import Linkzin

# PYGAME
import pygame
from pygame             import Surface          as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER
from pygame.image       import load             as carregar_imagem
from pygame.event       import Event            as Evento 

# IMPORTAÇÕES GERAIS
from os import getcwd


' === CÓDIGO REAL === '


class Macro_ambiente:
    def __init__( _ , *amb_interativos: AI , screen: Superficie , fps: int = 60 , auto_X: bool = True ):
        try:
            _.estoque = list(*amb_interativos) # [ MC(), MC(), ... ]
        except TypeError:
            _.estoque = list(amb_interativos)  # [ MC(), MC(), ... ]

        _.screen            = screen
        _.__fps             = fps
        _.__auto_X          = auto_X

        for ai in _.estoque:
            ai: AI

            ai.fps_limit    = _.__fps
            ai.auto_X       = _.__auto_X

        _.index = 0

    @property
    def ambiente_atual( _ ) -> AI:
        '* retorna o ambiente em foco/index'
        return _.estoque[_.index]

    @property
    def ambientes_rodaveis( _ ):
        '* retorna todos os ambientes que ainda não foram rodados/estão rodando'
        return [ amb for amb in _.estoque if amb.running == True ]

    @property
    def fps( _ ) -> int:
        '* retorna o fps compartilhado para todos os ambientes'
        return _.__fps

    @fps.setter
    def fps( _ , novo_fps : int):
        _.__fps = novo_fps

        for ai in _.estoque:
            ai.fps_limit = _.__fps

        return _.__fps

    @property
    def auto_X( _ ) -> bool:
        '* retorna o bool compartilhado que define se as fases vão prover(ou não) um sistema de auto-fechamento'
        return _.__auto_X

    @auto_X.setter
    def auto_X( _ , novo : bool ):
        _.__auto_X = novo

        for ai in _.estoque:
            ai.auto_X = _.__auto_X

        return _.__auto_X

    def running_geral( _ , qualquer = True):
        '* retorna o running de todos os ambientes'
        e = any if qualquer else all

        return e([ ai.running for ai in _.estoque ])

    def reativar_amb_solo( _ , index ):
        '* ativa um dos ambientes'
        _.estoque[index].running = True

    def reativar_ambientes( _ ):
        '* ativa todos os runnings dos ambientes'
        for ai in _.estoque:
            ai.running = True

    def rodar_ambiente( _ , info_extra : ... = None ):
        '* roda o ambiente que está em foco'
        return _.ambiente_atual( _.screen , info_extra )

    def __getitem__( _ , posicao : int ):
        return _.estoque[posicao]

    def __call__( _ , info_extra : ... = None , index = None ):
        if type(index) == int:
            _.index = index

        return _.rodar_ambiente( info_extra )

    
' === TESTES === '


if __name__ == '__main__':
    import pygame
    from os                     import getcwd
    from pygame.event           import get      as capturar_evento
    from pygame.time            import Clock    as Relogio
    from codigo_compartilhado.linkzin  import Linkzin
    from pygame.image           import load     as carregar_imagem 
    from pygame                 import Surface  as Superficie , KEYDOWN as TECLA_SEGURADA , KEYUP as TECLA_APERTADA , K_LEFT as ESQUERDA , K_RIGHT as DIREITA , K_RETURN as ENTER

    from ambiente_interativo        import Criar_Fase

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    @Criar_Fase( "salão" )
    def fase(
        screen :Superficie, 
            info_extra : ...     = None ,
                parente : AI     = None ,
                    eventos:list = None ):
        
        for evento in eventos:
            if evento.type == TECLA_SEGURADA:
                if evento.key == ENTER:
                    print('Entrou na fase 2')
                    'parente.index = 1'

                    return False
        return True

    @Criar_Fase( "salão" )
    def fase_2(
        screen :Superficie, 
            info_extra : ...     = None ,
                parente : AI     = None ,
                    eventos:list = None ):
        
        for evento in eventos:
            if evento.type == TECLA_SEGURADA:
                if evento.key == ENTER:
                    print('Entrou na fase 2')
                    'parente.index = 1'

                    return False
        return True

    A = Macro_ambiente( fase , fase_2 , screen= screen)

    A.estoque[1].running = False

    print(A.ambientes_rodaveis)